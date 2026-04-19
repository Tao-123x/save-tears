<template>
  <EditorialPage tone="mist">
    <view class="home-page">
      <view class="home-page__header st-panel-raise">
        <text class="st-kicker">Overview</text>
        <text class="st-display home-page__headline">Good morning</text>
        <text class="st-subtitle home-page__subline">
          {{ currentUser ? `${currentUser.room_number || 'Room'}` : 'Sign in' }}
        </text>
      </view>

      <EditorialEmptyState
        v-if="!currentUser"
        title="请先登录"
        message="登录后查看首页"
        action-text="去登录"
        @action="goToLogin"
      />

      <template v-else>
        <view class="home-hero st-panel-raise">
          <view class="home-hero__topline"></view>
          <text class="home-hero__kicker">Today</text>
          <text class="home-hero__value">{{ digest.flow.total }} L</text>
          <text class="home-hero__delta">{{ heroDeltaLabel }}</text>

          <view class="home-hero__peak">
            <text class="home-hero__peak-label">Peak</text>
            <view class="home-hero__peak-pill">{{ peakTimeLabel }}</view>
          </view>

          <view class="home-hero__reservoir">
            <view class="home-hero__reservoir-glow"></view>
            <view class="home-hero__reflection home-hero__reflection--one"></view>
            <view class="home-hero__reflection home-hero__reflection--two"></view>
            <view class="home-hero__liquid" :style="{ height: waterLevelHeight }">
              <view class="home-hero__undertow"></view>
              <view class="home-hero__surface">
                <view class="home-hero__surface-line home-hero__surface-line--main"></view>
                <view class="home-hero__surface-line home-hero__surface-line--accent"></view>
                <view class="home-hero__surface-line home-hero__surface-line--edge"></view>
              </view>
              <view class="home-hero__caustic"></view>
            </view>
            <view class="home-hero__depth-pill">
              <text class="home-hero__depth-label">Synced</text>
              <text class="home-hero__depth-value">{{ digest.flow.points.length }}</text>
            </view>
          </view>
        </view>

        <view class="home-page__metrics">
          <MetricCard label="Bill" :value="billValue" compact />
          <MetricCard label="Quality" :value="qualityValue" compact />
          <MetricCard label="Month" :value="monthValue" compact />
        </view>

        <view class="home-alert st-panel-raise">
          <view class="home-alert__dot"></view>
          <text class="home-alert__label">Alert</text>
          <text class="home-alert__copy">{{ primaryAlert }}</text>
        </view>

        <view class="home-page__quick-grid">
          <view class="home-quick-card st-panel-raise" @tap="goToDataCenter('flow')">
            <view class="home-quick-card__glow"></view>
            <text class="home-quick-card__title">Data centre</text>
            <view class="home-quick-card__action">Open</view>
          </view>

          <view class="home-quick-card st-panel-raise" @tap="goToDataCenter('bill')">
            <view class="home-quick-card__glow home-quick-card__glow--wide"></view>
            <text class="home-quick-card__title">Bill notes</text>
            <view class="home-quick-card__action">View bill</view>
          </view>
        </view>

        <EditorialEmptyState
          v-if="errorMessage"
          title="数据暂时不可用"
          :message="errorMessage"
          action-text="重新加载"
          @action="loadDigest"
        />
      </template>
    </view>
  </EditorialPage>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { onShow } from '@dcloudio/uni-app';

import EditorialEmptyState from '@/components/EditorialEmptyState.vue';
import EditorialPage from '@/components/EditorialPage.vue';
import MetricCard from '@/components/MetricCard.vue';
import { getSewageTurbidity, getWaterBill, getWaterFlow } from '@/api/index';
import {
  buildHomeDigest,
  type WaterBillRecord,
  type WaterFlowRecord,
  type WaterQualityRecord,
} from '@/utils/insights';
import { queueResidentDataTab, type ResidentDataTab } from '@/utils/data-nav';
import { getStoredUser, type StoredUser } from '@/utils/session';

const currentUser = ref<StoredUser | null>(null);
const loading = ref(false);
const errorMessage = ref('');
const flowRecords = ref<WaterFlowRecord[]>([]);
const billRecords = ref<WaterBillRecord[]>([]);
const qualityRecords = ref<WaterQualityRecord[]>([]);
const digest = ref(
  buildHomeDigest({
    username: '',
    flowRecords: [],
    billRecords: [],
    qualityRecords: [],
  }),
);

const orderedFlowRecords = computed(() => {
  return [...flowRecords.value].sort((left, right) => left.timestamp.localeCompare(right.timestamp));
});

const heroDeltaLabel = computed(() => {
  const ordered = orderedFlowRecords.value;
  if (ordered.length < 2) {
    return loading.value ? 'Syncing latest reading...' : 'Waiting for another reading';
  }

  const latest = Number(ordered[ordered.length - 1]?.flow_rate || 0);
  const previous = Number(ordered[ordered.length - 2]?.flow_rate || 0);
  if (!previous) {
    return `${latest} L in the latest reading`;
  }

  const delta = latest - previous;
  const ratio = Math.round((Math.abs(delta) / previous) * 100);
  return `${delta >= 0 ? '+' : '-'}${ratio}% vs previous reading`;
});

const peakTimeLabel = computed(() => {
  if (!flowRecords.value.length) {
    return '--:--';
  }

  const peakRecord = [...flowRecords.value].sort((left, right) => Number(right.flow_rate || 0) - Number(left.flow_rate || 0))[0];
  const source = String(peakRecord?.timestamp || '');
  const matched = source.match(/T(\d{2}:\d{2})/);
  return matched?.[1] || source.slice(11, 16) || '--:--';
});

const flowLevelRatio = computed(() => {
  const total = Number(digest.value.flow.total || 0);
  const peak = Number(digest.value.flow.peak || 0);
  const ratio = total && peak ? total / Math.max(peak * 3, 1) : 0.5;
  return Math.min(0.78, Math.max(0.44, ratio));
});
const waterLevelHeight = computed(() => `${Math.round(flowLevelRatio.value * 100)}%`);

const billValue = computed(() => (digest.value.bill.latest ? `¥${digest.value.bill.latest}` : 'Pending'));
const qualityValue = computed(() => {
  if (digest.value.quality.statusTone === 'watch') return 'Watch';
  if (digest.value.quality.statusTone === 'steady') return 'Steady';
  return 'Safe';
});
const monthValue = computed(() => `${(digest.value.flow.total / 1000).toFixed(1)} m3`);
const primaryAlert = computed(() => {
  return digest.value.alerts[0] || 'No anomalies';
});

onShow(() => {
  void loadDigest();
});

async function loadDigest() {
  currentUser.value = getStoredUser();
  errorMessage.value = '';

  if (!currentUser.value?.room_number) {
    flowRecords.value = [];
    billRecords.value = [];
    qualityRecords.value = [];
    digest.value = buildHomeDigest({
      username: currentUser.value?.username || '',
      flowRecords: [],
      billRecords: [],
      qualityRecords: [],
    });
    return;
  }

  loading.value = true;

  try {
    const [flow, bills, quality] = await Promise.all([
      getWaterFlow(currentUser.value.room_number),
      getWaterBill(currentUser.value.room_number),
      getSewageTurbidity(currentUser.value.room_number),
    ]);

    flowRecords.value = flow;
    billRecords.value = bills;
    qualityRecords.value = quality;
    digest.value = buildHomeDigest({
      username: currentUser.value.username || '',
      flowRecords: flow,
      billRecords: bills,
      qualityRecords: quality,
    });
  } catch (error: any) {
    errorMessage.value = error?.message || '数据暂时不可用，请稍后再试。';
  } finally {
    loading.value = false;
  }
}

function goToDataCenter(tab: ResidentDataTab) {
  queueResidentDataTab(tab);
  uni.switchTab({ url: '/pages/data/index' });
}

function goToLogin() {
  uni.navigateTo({ url: '/pages/login/index' });
}
</script>

<style scoped>
.home-page__header {
  padding: 18rpx 6rpx 26rpx;
}

.home-page__headline {
  margin-top: 10rpx;
}

.home-page__subline {
  margin-top: 14rpx;
}

.home-hero {
  position: relative;
  margin-top: 16rpx;
  min-height: 432rpx;
  padding: 30rpx 26rpx;
  border-radius: var(--st-radius-xl);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(223, 241, 255, 0.98) 100%);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow);
  overflow: hidden;
}

.home-hero::before,
.home-hero::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.home-hero::before {
  right: -86rpx;
  top: -54rpx;
  width: 280rpx;
  height: 280rpx;
  background: radial-gradient(circle, rgba(165, 214, 255, 0.26) 0%, rgba(165, 214, 255, 0) 68%);
  filter: blur(8rpx);
  animation: st-orb-float 7.8s ease-in-out infinite;
}

.home-hero::after {
  left: -92rpx;
  bottom: 24rpx;
  width: 320rpx;
  height: 220rpx;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.42) 0%, rgba(255, 255, 255, 0) 74%);
  filter: blur(10rpx);
  animation: st-orb-float 8.4s ease-in-out infinite reverse;
}

.home-hero__reservoir {
  position: absolute;
  left: 26rpx;
  right: 26rpx;
  bottom: 28rpx;
  height: 184rpx;
  border-radius: 34rpx;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.52) 0%, rgba(255, 255, 255, 0.2) 100%);
  border: 1rpx solid rgba(188, 220, 243, 0.92);
  box-shadow:
    inset 0 1rpx 0 rgba(255, 255, 255, 0.82),
    inset 0 -20rpx 36rpx rgba(57, 142, 219, 0.1);
  overflow: hidden;
}

.home-hero__reservoir-glow {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 22% 18%, rgba(255, 255, 255, 0.52) 0%, rgba(255, 255, 255, 0) 32%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0) 34%);
  pointer-events: none;
}

.home-hero__liquid {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  min-height: 96rpx;
  background: linear-gradient(180deg, rgba(175, 225, 255, 0.14) 0%, rgba(121, 199, 255, 0.42) 34%, rgba(54, 152, 239, 0.82) 100%);
  animation: st-liquid-heave 4.9s ease-in-out infinite;
  transform-origin: center bottom;
}

.home-hero__undertow {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0) 26%),
    radial-gradient(circle at 50% 120%, rgba(24, 112, 199, 0.52) 0%, rgba(24, 112, 199, 0) 52%);
}

.home-hero__surface {
  position: absolute;
  left: -6%;
  right: -6%;
  top: -12rpx;
  height: 64rpx;
  pointer-events: none;
}

.home-hero__surface-line {
  position: absolute;
  height: 22rpx;
  border-radius: 999rpx;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.94) 26%, rgba(221, 243, 255, 0.82) 62%, rgba(255, 255, 255, 0) 100%);
  filter: blur(4rpx);
  pointer-events: none;
}

.home-hero__surface-line--main {
  left: 4%;
  top: 10rpx;
  width: 62%;
  opacity: 0.9;
  animation: st-surface-drift 6.6s ease-in-out infinite;
}

.home-hero__surface-line--accent {
  right: 8%;
  top: 22rpx;
  width: 38%;
  height: 18rpx;
  opacity: 0.76;
  animation: st-surface-drift-reverse 5.2s ease-in-out infinite;
}

.home-hero__surface-line--edge {
  left: 10%;
  top: 4rpx;
  width: 74%;
  height: 10rpx;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.88) 30%, rgba(255, 255, 255, 0.58) 70%, rgba(255, 255, 255, 0.08) 100%);
  filter: blur(1rpx);
  opacity: 0.92;
  animation: st-surface-drift 8.4s ease-in-out infinite reverse;
}

.home-hero__caustic {
  position: absolute;
  left: -12%;
  top: 28rpx;
  width: 126%;
  height: 30rpx;
  border-radius: 999rpx;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.34) 28%, rgba(255, 255, 255, 0.66) 50%, rgba(255, 255, 255, 0.34) 72%, rgba(255, 255, 255, 0) 100%);
  filter: blur(8rpx);
  opacity: 0.82;
  transform: rotate(-2deg);
  pointer-events: none;
  animation: st-water-scan 3.4s linear infinite;
}

.home-hero__topline {
  position: absolute;
  left: 20rpx;
  right: 20rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.home-hero__kicker {
  display: block;
  font-size: 22rpx;
  color: var(--st-accent-deep);
}

.home-hero__value {
  display: block;
  margin-top: 14rpx;
  font-family: var(--st-title-font);
  font-size: 72rpx;
  line-height: 1;
  font-weight: 700;
  color: var(--st-text);
}

.home-hero__delta {
  display: block;
  margin-top: 14rpx;
  font-size: 26rpx;
  color: var(--st-text-soft);
}

.home-hero__peak {
  position: absolute;
  top: 28rpx;
  right: 24rpx;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
  align-items: flex-start;
}

.home-hero__peak-label {
  font-size: 20rpx;
  color: var(--st-text-soft);
}

.home-hero__peak-pill {
  min-width: 120rpx;
  padding: 18rpx 26rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.9);
  border: 1rpx solid var(--st-line);
  font-size: 34rpx;
  font-weight: 700;
  color: var(--st-text);
  box-shadow: var(--st-shadow-tight);
}

.home-hero__depth-pill {
  position: absolute;
  right: 22rpx;
  bottom: 20rpx;
  display: flex;
  align-items: baseline;
  gap: 10rpx;
  padding: 14rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.72);
  border: 1rpx solid rgba(255, 255, 255, 0.66);
  backdrop-filter: blur(8rpx);
  box-shadow: 0 14rpx 24rpx rgba(42, 118, 191, 0.12);
}

.home-hero__depth-label {
  font-size: 20rpx;
  color: rgba(18, 50, 74, 0.62);
  letter-spacing: 0.08em;
}

.home-hero__depth-value {
  font-size: 28rpx;
  font-weight: 700;
  color: var(--st-text);
}

.home-hero__reflection {
  position: absolute;
  height: 26rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.46);
  filter: blur(8rpx);
  pointer-events: none;
}

.home-hero__reflection--one {
  left: 30rpx;
  top: 38rpx;
  width: 220rpx;
  animation: st-water-scan 3.9s linear infinite;
}

.home-hero__reflection--two {
  right: 46rpx;
  top: 72rpx;
  width: 140rpx;
  opacity: 0.78;
  animation: st-water-scan 4.8s linear infinite 1s;
}

.home-page__metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14rpx;
  margin-top: 18rpx;
}

.home-alert {
  position: relative;
  margin-top: 18rpx;
  padding: 20rpx 22rpx 18rpx 56rpx;
  border-radius: 26rpx;
  background: var(--st-warning-soft);
  border: 1rpx solid rgba(242, 164, 74, 0.12);
  box-shadow: var(--st-shadow-tight);
}

.home-alert__dot {
  position: absolute;
  left: 22rpx;
  top: 26rpx;
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: rgba(242, 164, 74, 0.86);
  box-shadow: 0 0 18rpx rgba(242, 164, 74, 0.28);
}

.home-alert__label {
  display: block;
  font-size: 22rpx;
  color: var(--st-warning);
}

.home-alert__copy {
  display: block;
  margin-top: 8rpx;
  font-size: 26rpx;
  line-height: 1.5;
  color: var(--st-text);
}

.home-page__quick-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18rpx;
  margin-top: 18rpx;
}

.home-quick-card {
  position: relative;
  min-height: 214rpx;
  padding: 28rpx 22rpx 24rpx;
  border-radius: 28rpx;
  background: rgba(255, 255, 255, 0.95);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow-tight);
  overflow: hidden;
}

.home-quick-card__glow {
  position: absolute;
  right: 18rpx;
  bottom: 40rpx;
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  background: rgba(139, 212, 255, 0.26);
  filter: blur(8rpx);
  animation: st-wave-slide-reverse 4.4s ease-in-out infinite;
}

.home-quick-card__glow--wide {
  width: 88rpx;
  height: 20rpx;
  border-radius: 999rpx;
  right: 8rpx;
  bottom: 52rpx;
  animation-duration: 4.2s;
}

.home-quick-card__title {
  display: block;
  font-size: 32rpx;
  font-weight: 700;
  color: var(--st-text);
}

.home-quick-card__copy {
  display: block;
  margin-top: 18rpx;
  font-size: 24rpx;
  line-height: 1.6;
  color: var(--st-text-soft);
}

.home-quick-card__action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 56rpx;
  padding: 0 26rpx;
  margin-top: 30rpx;
  border-radius: 999rpx;
  background: #eaf5ff;
  color: var(--st-accent-deep);
  font-size: 24rpx;
  font-weight: 600;
}
</style>
