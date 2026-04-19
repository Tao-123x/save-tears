import test from 'node:test';
import assert from 'node:assert/strict';

import * as insights from '../src/utils/insights.ts';
import {
  isAdminUser,
  normalizeUserRole,
  parseStoredUser,
} from '../src/utils/session.ts';
import {
  buildAdminOverview,
  buildHomeDigest,
  buildWaterBillInsights,
  buildWaterFlowInsights,
  buildWaterQualityInsights,
} from '../src/utils/insights.ts';

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
