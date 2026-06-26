import test from 'node:test';
import assert from 'node:assert/strict';

import * as insights from '../src/utils/insights.ts';
import {
  isAdminUser,
  normalizeUserRole,
  parseStoredUser,
} from '../src/utils/session.ts';
import { encodeRoomPath, resolveApiBaseUrl } from '../src/utils/api-base.ts';
import {
  buildAdminOverview,
  buildHomeDigest,
  buildSavingAdminOverview,
  buildSavingOverview,
  buildWaterBillInsights,
  buildWaterFlowInsights,
  buildWaterQualityInsights,
} from '../src/utils/insights.ts';
import {
  getResidentPreferences,
  saveResidentPreferences,
} from '../src/utils/preferences.ts';

test('parseStoredUser handles invalid JSON and missing roles safely', () => {
  assert.equal(parseStoredUser(''), null);
  assert.equal(parseStoredUser('{bad json'), null);
  assert.equal(parseStoredUser('{"username":"Lin","room_number":"3-202"}'), null);
  assert.deepEqual(parseStoredUser('{"username":"Lin","room_number":"3-202","token":"signed-token"}'), {
    username: 'Lin',
    room_number: '3-202',
    role: 'user',
    token: 'signed-token',
  });
  assert.equal(normalizeUserRole('ADMIN'), 'admin');
  assert.equal(normalizeUserRole(undefined), 'user');
});

test('isAdminUser only returns true for admin users', () => {
  assert.equal(isAdminUser(null), false);
  assert.equal(isAdminUser({ username: 'Guest', role: 'user' }), false);
  assert.equal(isAdminUser({ username: 'Manager', role: 'admin' }), true);
});

test('buildWaterFlowInsights sorts records, computes totals and detects spikes', () => {
  const insights = buildWaterFlowInsights([
    { id: 3, flow_rate: 42, timestamp: '2026-04-06T08:00:00' },
    { id: 1, flow_rate: 18, timestamp: '2026-04-01T08:00:00' },
    { id: 4, flow_rate: 24, timestamp: '2026-04-07T08:00:00' },
    { id: 2, flow_rate: 54, timestamp: '2026-04-04T08:00:00' },
  ]);

  assert.equal(insights.total, 138);
  assert.equal(insights.latest, 24);
  assert.equal(insights.peak, 54);
  assert.equal(insights.anomalyCount, 1);
  assert.deepEqual(
    insights.points.map((point) => point.label),
    ['04/01', '04/04', '04/06', '04/07'],
  );
});

test('bill, water quality, and home digest produce editorial summaries', () => {
  const billInsights = buildWaterBillInsights([
    { id: 1, amount: 86, month: '2026-02' },
    { id: 2, amount: 73, month: '2026-03' },
    { id: 3, amount: 69, month: '2026-04' },
  ]);
  const qualityInsights = buildWaterQualityInsights([
    { id: 1, turbidity_value: 18, timestamp: '2026-04-01T08:00:00' },
    { id: 2, turbidity_value: 14, timestamp: '2026-04-06T08:00:00' },
    { id: 3, turbidity_value: 9, timestamp: '2026-04-07T08:00:00' },
  ]);
  const digest = buildHomeDigest({
    username: 'Lin',
    flowRecords: [
      { id: 1, flow_rate: 18, timestamp: '2026-04-01T08:00:00' },
      { id: 2, flow_rate: 54, timestamp: '2026-04-04T08:00:00' },
      { id: 3, flow_rate: 42, timestamp: '2026-04-06T08:00:00' },
      { id: 4, flow_rate: 24, timestamp: '2026-04-07T08:00:00' },
    ],
    billRecords: [
      { id: 1, amount: 86, month: '2026-02' },
      { id: 2, amount: 73, month: '2026-03' },
      { id: 3, amount: 69, month: '2026-04' },
    ],
    qualityRecords: [
      { id: 1, turbidity_value: 18, timestamp: '2026-04-01T08:00:00' },
      { id: 2, turbidity_value: 14, timestamp: '2026-04-06T08:00:00' },
      { id: 3, turbidity_value: 9, timestamp: '2026-04-07T08:00:00' },
    ],
  });

  assert.equal(billInsights.latest, 69);
  assert.equal(billInsights.deltaFromPrevious, -4);
  assert.equal(qualityInsights.statusTone, 'excellent');
  assert.equal(digest.heroMetric.value, '138L');
  assert.equal(digest.alerts.length, 1);
  assert.match(digest.editorNote, /Lin/);
});

test('buildAdminOverview summarizes existing users without exposing sensitive fields', () => {
  const overview = buildAdminOverview([
    { username: 'admin', room_number: 'HQ-01', role: 'admin' },
    { username: 'lin', room_number: '3-202', role: 'user' },
    { username: 'gao', room_number: '', role: 'user' },
  ]);

  assert.equal(overview.totalUsers, 3);
  assert.equal(overview.adminCount, 1);
  assert.equal(overview.roomsConfigured, 2);
  assert.deepEqual(overview.roomsMissing, ['gao']);
});

test('buildTrendGeometry keeps the latest points and computes even line positions', () => {
  assert.equal(typeof insights.buildTrendGeometry, 'function');

  const geometry = insights.buildTrendGeometry(
    [
      { label: '1', value: 10 },
      { label: '2', value: 14 },
      { label: '3', value: 18 },
      { label: '4', value: 24 },
      { label: '5', value: 20 },
      { label: '6', value: 28 },
      { label: '7', value: 36 },
    ],
    { maxPoints: 6, width: 300, height: 120, topPadding: 12, bottomPadding: 18 },
  );

  assert.deepEqual(
    geometry.nodes.map((node) => node.label),
    ['2', '3', '4', '5', '6', '7'],
  );
  assert.equal(geometry.nodes[0]?.x, 0);
  assert.equal(geometry.nodes.at(-1)?.x, 300);
  assert.equal(geometry.nodes.at(-1)?.isCurrent, true);
  assert.equal(geometry.segments.length, 5);
  assert.ok(geometry.nodes.every((node) => node.y >= 12 && node.y <= 102));
});

test('buildTrendGeometry falls back to a steady baseline when values are empty or zero', () => {
  assert.equal(typeof insights.buildTrendGeometry, 'function');

  const geometry = insights.buildTrendGeometry(
    [
      { label: 'A', value: 0 },
      { label: 'B', value: 0 },
      { label: 'C', value: 0 },
    ],
    { width: 200, height: 100, topPadding: 10, bottomPadding: 20 },
  );

  assert.deepEqual(
    geometry.nodes.map((node) => node.y),
    [80, 80, 80],
  );
  assert.ok(geometry.segments.every((segment) => Math.abs(segment.angle) < 0.001));
});

test('buildSavingOverview computes replacement rate and savings', () => {
  const overview = buildSavingOverview({
    tapWaterLiters: 30,
    greywaterLiters: 12,
    flushCount: 2,
  });

  assert.equal(overview.tapWaterLiters, 30);
  assert.equal(overview.greywaterLiters, 12);
  assert.equal(overview.flushCount, 2);
  assert.equal(overview.estimatedSavingsLiters, 12);
  assert.equal(overview.replacementRate, 12 / 42);
  assert.equal(overview.replacementRateLabel, '29%');
  assert.equal(overview.targetProgressLabel, '0/0');
  assert.equal(overview.summary, '今日灰水已替代约 29% 的总用水。');
});

test('buildSavingOverview returns safe labels for empty saving data', () => {
  const overview = buildSavingOverview({});

  assert.equal(overview.tapWaterLiters, 0);
  assert.equal(overview.greywaterLiters, 0);
  assert.equal(overview.flushCount, 0);
  assert.equal(overview.estimatedSavingsLiters, 0);
  assert.equal(overview.replacementRate, 0);
  assert.equal(overview.replacementRateLabel, '0%');
  assert.equal(overview.targetProgressLabel, '0/0');
  assert.equal(overview.summary, '暂无节水数据，等待设备或手动记录更新。');
});

test('buildSavingOverview reports target progress and latest plan preview', () => {
  const overview = buildSavingOverview({
    tapWaterLiters: 45,
    greywaterLiters: 15,
    flushCount: 3,
    targetFlushCount: 5,
    latestPlanText: '未来 7 天优先使用灰水冲厕，保持每日 5 次以上。',
  });

  assert.equal(overview.targetProgress, 0.6);
  assert.equal(overview.targetProgressLabel, '3/5');
  assert.equal(overview.latestPlanPreview, '未来 7 天优先使用灰水冲厕，保持每日 5 次以上。');
});

test('resident preferences use saving reminder names with true defaults', () => {
  const storage = new Map<string, unknown>();
  (globalThis as any).uni = {
    getStorageSync: (key: string) => storage.get(key) ?? '',
    setStorageSync: (key: string, value: unknown) => storage.set(key, value),
  };

  assert.deepEqual(getResidentPreferences(), {
    savingTargetRemindersEnabled: true,
    deviceAbnormalityAlertsEnabled: true,
  });

  saveResidentPreferences({
    savingTargetRemindersEnabled: false,
    deviceAbnormalityAlertsEnabled: true,
  });

  assert.equal(storage.get('saving_target_reminders_enabled'), false);
  assert.equal(storage.get('device_abnormality_alerts_enabled'), true);
  assert.deepEqual(getResidentPreferences(), {
    savingTargetRemindersEnabled: false,
    deviceAbnormalityAlertsEnabled: true,
  });

  delete (globalThis as any).uni;
});

test('buildSavingAdminOverview prepares room rankings and device warnings', () => {
  const overview = buildSavingAdminOverview(
    [
      {
        roomNumber: 'A101',
        tapWaterLiters: 30,
        greywaterLiters: 12,
        estimatedSavingsLiters: 12,
        replacementRate: 12 / 42,
        flushCount: 2,
      },
      {
        roomNumber: 'B202',
        tapWaterLiters: 50,
        greywaterLiters: 0,
        estimatedSavingsLiters: 0,
        replacementRate: 0,
        flushCount: 0,
      },
    ],
    [
      {
        device_id: 'GW-A101-001',
        room_number: 'A101',
        status: 'online',
      },
      {
        device_id: 'GW-B202-001',
        room_number: 'B202',
        status: 'offline',
      },
    ],
  );

  assert.equal(overview.totalTapWaterLiters, 80);
  assert.equal(overview.totalGreywaterLiters, 12);
  assert.equal(overview.totalEstimatedSavingsLiters, 12);
  assert.equal(overview.averageReplacementRateLabel, '13%');
  assert.deepEqual(
    overview.roomRanking.map((room) => room.roomNumber),
    ['A101', 'B202'],
  );
  assert.deepEqual(
    overview.lowReplacementRooms.map((room) => room.roomNumber),
    ['B202'],
  );
  assert.deepEqual(
    overview.offlineDevices.map((device) => device.device_id),
    ['GW-B202-001'],
  );
});

test('resolveApiBaseUrl prefers explicit config and otherwise uses the current H5 host', () => {
  assert.equal(
    resolveApiBaseUrl({
      customBaseUrl: 'http://10.0.0.8:9000/',
      browserProtocol: 'http:',
      browserHostname: 'localhost',
    }),
    'http://10.0.0.8:9000',
  );

  assert.equal(
    resolveApiBaseUrl({
      browserProtocol: 'http:',
      browserHostname: 'localhost',
    }),
    'http://localhost:8000',
  );

  assert.equal(
    resolveApiBaseUrl({
      browserProtocol: 'http:',
      browserHostname: '192.168.31.5',
    }),
    'http://192.168.31.5:8000',
  );
});

test('encodeRoomPath escapes room numbers before using them in API paths', () => {
  assert.equal(encodeRoomPath('A/101'), 'A%2F101');
  assert.equal(encodeRoomPath('Room 2'), 'Room%202');
});
