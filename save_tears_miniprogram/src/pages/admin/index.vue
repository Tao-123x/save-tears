<template>
  <EditorialPage tone="deep" compact>
    <view class="admin-page">
      <view class="admin-page__header st-panel-raise">
        <text class="st-kicker">管理</text>
        <text class="st-display admin-page__headline">节水管理</text>
        <text class="st-subtitle admin-page__subline">跨房间查看灰水替代、自来水节省和设备状态。</text>
      </view>

      <view v-if="loading" class="admin-page__loading st-panel-raise">正在加载节水数据...</view>
      <EditorialEmptyState
        v-else-if="errorMessage"
        title="节水管理暂时不可用"
        :message="errorMessage"
        action-text="再试一次"
        @action="loadAdminDesk"
      />

      <template v-else>
        <view class="admin-page__stats">
          <AdminStatCard label="自来水" :value="formatLiters(overview.totalTapWaterLiters)" helper="所有房间累计" />
          <AdminStatCard label="灰水" :value="formatLiters(overview.totalGreywaterLiters)" helper="已用于替代" />
          <AdminStatCard label="节省" :value="formatLiters(overview.totalEstimatedSavingsLiters)" helper="估算少用自来水" />
          <AdminStatCard label="替代率" :value="overview.averageReplacementRateLabel" helper="灰水 / 总用水" />
          <AdminStatCard label="冲厕" :value="String(overview.totalFlushCount)" helper="灰水冲厕次数" />
          <AdminStatCard label="设备异常" :value="String(overview.offlineDevices.length)" helper="离线或告警设备" />
        </view>

        <view class="admin-section st-panel-raise">
          <view class="admin-section__topline"></view>
          <view class="admin-section__header">
            <text class="admin-section__title">房间排行</text>
            <text class="admin-section__meta">{{ roomSummaries.length }} 个房间</text>
          </view>

          <EditorialEmptyState
            v-if="!overview.roomRanking.length"
            title="暂无房间节水数据"
            message="等待房间绑定和节水统计接口返回后，这里会显示替代率排行。"
          />

          <template v-else>
            <view
              v-for="(room, index) in overview.roomRanking"
              :key="room.roomNumber"
              class="ranking-row"
            >
              <view class="ranking-row__rank">{{ index + 1 }}</view>
              <view class="ranking-row__body">
                <view class="ranking-row__main">
                  <text class="ranking-row__room">{{ room.roomNumber }}</text>
                  <text class="ranking-row__rate">{{ room.replacementRateLabel }}</text>
                </view>
                <view class="ranking-row__bar">
                  <view class="ranking-row__fill" :style="{ width: rankBarWidth(room.replacementRate) }"></view>
                </view>
                <text class="ranking-row__copy">
                  自来水 {{ formatLiters(room.tapWaterLiters) }} · 灰水 {{ formatLiters(room.greywaterLiters) }} · 冲厕 {{ room.flushCount }} 次
                </text>
              </view>
            </view>
          </template>
        </view>

        <view class="admin-section st-panel-raise">
          <view class="admin-section__topline"></view>
          <view class="admin-section__header">
            <text class="admin-section__title">设备状态</text>
            <text class="admin-section__meta">{{ devices.length }} 台设备</text>
          </view>

          <EditorialEmptyState
            v-if="!devices.length"
            title="暂无设备"
            message="设备接入后会显示在线状态、绑定房间和最后上传时间。"
          />

          <template v-else>
            <view
              v-for="device in devices"
              :key="device.device_id"
              class="device-row"
            >
              <view class="device-row__main">
                <text class="device-row__name">{{ device.device_id }}</text>
                <text class="device-row__meta">
                  {{ device.room_number || '未绑定房间' }} · {{ formatDeviceTime(device.last_seen_at) }}
                </text>
              </view>
              <view class="device-row__status" :class="deviceStatusClass(device.status)">
                {{ deviceStatusText(device.status) }}
              </view>
            </view>
          </template>
        </view>

        <view class="admin-section st-panel-raise">
          <view class="admin-section__topline"></view>
          <view class="admin-section__header">
            <text class="admin-section__title">异常提醒</text>
            <text class="admin-section__meta">{{ alerts.length }} 条</text>
          </view>

          <view v-if="!alerts.length" class="alert-empty">
            <text class="alert-empty__title">暂无异常</text>
            <text class="alert-empty__copy">当前没有低替代率房间或离线设备。</text>
          </view>

          <view v-else class="alert-list">
            <view v-for="alert in alerts" :key="alert" class="alert-row">
              <view class="alert-row__dot"></view>
              <text class="alert-row__copy">{{ alert }}</text>
            </view>
          </view>
        </view>
      </template>
    </view>
  </EditorialPage>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { onShow } from '@dcloudio/uni-app';

import AdminStatCard from '@/components/AdminStatCard.vue';
import EditorialEmptyState from '@/components/EditorialEmptyState.vue';
import EditorialPage from '@/components/EditorialPage.vue';
import {
  getDevices,
  getSavingStats,
  getUsers,
  type Device,
  type SavingStats,
  type UserRecord,
} from '@/api/index';
import {
  buildSavingAdminOverview,
  type SavingDeviceSummary,
  type SavingRoomSummary,
} from '@/utils/insights';
import { getStoredUser, isAdminUser } from '@/utils/session';

const loading = ref(false);
const errorMessage = ref('');
const roomSummaries = ref<SavingRoomSummary[]>([]);
const devices = ref<Device[]>([]);

const overview = computed(() => buildSavingAdminOverview(roomSummaries.value, devices.value));
const alerts = computed(() => {
  const messages: string[] = [];

  overview.value.lowReplacementRooms.forEach((room) => {
    messages.push(`${room.roomNumber} 灰水替代率仅 ${room.replacementRateLabel}，建议检查使用习惯或设备数据。`);
  });

  overview.value.offlineDevices.forEach((device) => {
    messages.push(`${device.device_id} 当前${deviceStatusText(device.status)}，最后上传：${formatDeviceTime(device.last_seen_at)}。`);
  });

  return messages;
});

onShow(() => {
  const user = getStoredUser();
  if (!isAdminUser(user)) {
    uni.showToast({ title: '普通住户无法查看管理员页', icon: 'none' });
    setTimeout(() => {
      uni.switchTab({ url: '/pages/home/index' });
    }, 120);
    return;
  }

  void loadAdminDesk();
});

async function loadAdminDesk() {
  loading.value = true;
  errorMessage.value = '';

  try {
    const users = await getUsers();
    const roomNumbers = collectRoomNumbers(unwrapData<UserRecord[]>(users));
    const [statsList, deviceList] = await Promise.all([
      Promise.all(roomNumbers.map((roomNumber) => getSavingStats(roomNumber))),
      getDevices(),
    ]);

    roomSummaries.value = statsList.map((stats, index) => toRoomSummary(roomNumbers[index], unwrapData<SavingStats>(stats)));
    devices.value = unwrapData<Device[]>(deviceList).map(normalizeDevice);
  } catch (error) {
    roomSummaries.value = [];
    devices.value = [];
    errorMessage.value = getErrorMessage(error);
  } finally {
    loading.value = false;
  }
}

function collectRoomNumbers(users: UserRecord[]) {
  return Array.from(
    new Set(
      users
        .map((user) => String(user.room_number || '').trim())
        .filter(Boolean),
    ),
  ).sort((left, right) => left.localeCompare(right));
}

function toRoomSummary(roomNumber: string, stats: SavingStats): SavingRoomSummary {
  return {
    roomNumber,
    tapWaterLiters: Number(stats?.tap_water_liters || 0),
    greywaterLiters: Number(stats?.greywater_liters || 0),
    estimatedSavingsLiters: Number(stats?.estimated_savings_liters || 0),
    replacementRate: Number(stats?.replacement_rate || 0),
    flushCount: Number(stats?.flush_count || 0),
  };
}

function normalizeDevice(device: Device): Device & SavingDeviceSummary {
  return {
    ...device,
    device_id: String(device?.device_id || 'unknown-device'),
    status: String(device?.status || 'offline'),
  };
}

function unwrapData<T>(value: unknown): T {
  if (value && typeof value === 'object' && 'data' in value) {
    return (value as { data: T }).data;
  }

  return value as T;
}

function getErrorMessage(error: unknown) {
  if (error instanceof Error && error.message) {
    return `${error.message}。请检查网络或稍后重试。`;
  }

  return '节水数据暂时没有加载成功，请稍后再试。';
}

function formatLiters(value: number) {
  const safeValue = Number.isFinite(Number(value)) ? Number(value) : 0;
  if (safeValue >= 1000) {
    return `${(safeValue / 1000).toFixed(1)} m3`;
  }

  return `${Math.round(safeValue * 10) / 10} L`;
}

function rankBarWidth(rate: number) {
  const safeRate = Number.isFinite(Number(rate)) ? Math.max(0, Math.min(Number(rate), 1)) : 0;
  return `${Math.max(Math.round(safeRate * 100), 4)}%`;
}

function deviceStatusText(status?: string | null) {
  const normalized = String(status || '').toLowerCase();
  if (normalized === 'online') return '在线';
  if (normalized === 'warning') return '告警';
  return '离线';
}

function deviceStatusClass(status?: string | null) {
  const normalized = String(status || '').toLowerCase();
  return {
    'device-row__status--online': normalized === 'online',
    'device-row__status--warning': normalized === 'warning',
    'device-row__status--offline': normalized !== 'online' && normalized !== 'warning',
  };
}

function formatDeviceTime(value?: string | null) {
  const source = String(value || '').trim();
  if (!source) {
    return '暂无上传';
  }

  const date = new Date(source);
  if (Number.isNaN(date.getTime())) {
    return source;
  }

  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hour = String(date.getHours()).padStart(2, '0');
  const minute = String(date.getMinutes()).padStart(2, '0');
  return `${month}/${day} ${hour}:${minute}`;
}
</script>

<style scoped>
.admin-page__header {
  padding: 16rpx 6rpx 24rpx;
}

.admin-page__headline {
  margin-top: 10rpx;
}

.admin-page__subline {
  margin-top: 14rpx;
}

.admin-page__loading,
.admin-section {
  position: relative;
  margin-top: 18rpx;
  padding: 24rpx;
  border-radius: var(--st-radius-xl);
  background: rgba(255, 255, 255, 0.94);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow-tight);
  overflow: hidden;
}

.admin-page__loading {
  font-size: 26rpx;
  color: var(--st-text-soft);
}

.admin-page__stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14rpx;
}

.admin-section__topline {
  position: absolute;
  left: 18rpx;
  right: 18rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.admin-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  margin-bottom: 18rpx;
}

.admin-section__title {
  font-size: 30rpx;
  font-weight: 700;
  color: var(--st-text);
}

.admin-section__meta {
  flex-shrink: 0;
  font-size: 22rpx;
  color: var(--st-text-muted);
}

.ranking-row,
.device-row,
.alert-row {
  display: flex;
  align-items: center;
  gap: 18rpx;
  padding: 20rpx 0;
  border-bottom: 1rpx solid rgba(215, 232, 245, 0.72);
}

.ranking-row:last-child,
.device-row:last-child,
.alert-row:last-child {
  border-bottom: 0;
}

.ranking-row__rank {
  flex-shrink: 0;
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eef6ff;
  color: var(--st-accent-deep);
  font-size: 24rpx;
  font-weight: 700;
}

.ranking-row__body,
.device-row__main {
  min-width: 0;
  flex: 1;
}

.ranking-row__main,
.device-row {
  justify-content: space-between;
}

.ranking-row__main {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.ranking-row__room,
.device-row__name {
  display: block;
  font-size: 28rpx;
  font-weight: 700;
  color: var(--st-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ranking-row__rate {
  flex-shrink: 0;
  font-size: 28rpx;
  font-weight: 700;
  color: var(--st-success);
}

.ranking-row__bar {
  height: 12rpx;
  margin-top: 14rpx;
  border-radius: 999rpx;
  background: rgba(211, 227, 240, 0.72);
  overflow: hidden;
}

.ranking-row__fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #21b879 0%, #2f8cff 100%);
}

.ranking-row__copy,
.device-row__meta,
.alert-empty__copy {
  display: block;
  margin-top: 8rpx;
  font-size: 22rpx;
  line-height: 1.5;
  color: var(--st-text-soft);
}

.device-row__status {
  flex-shrink: 0;
  min-width: 92rpx;
  min-height: 48rpx;
  padding: 0 16rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: 700;
}

.device-row__status--online {
  background: #e9fbf5;
  color: var(--st-success);
}

.device-row__status--warning {
  background: #fff5e9;
  color: var(--st-warning);
}

.device-row__status--offline {
  background: #f1f4f8;
  color: var(--st-text-muted);
}

.alert-empty {
  padding: 18rpx 0 4rpx;
}

.alert-empty__title {
  display: block;
  font-size: 26rpx;
  font-weight: 700;
  color: var(--st-text);
}

.alert-row {
  align-items: flex-start;
}

.alert-row__dot {
  flex-shrink: 0;
  width: 14rpx;
  height: 14rpx;
  margin-top: 10rpx;
  border-radius: 50%;
  background: var(--st-warning);
  box-shadow: 0 0 12rpx rgba(255, 168, 74, 0.32);
}

.alert-row__copy {
  flex: 1;
  font-size: 24rpx;
  line-height: 1.5;
  color: var(--st-text);
}
</style>
