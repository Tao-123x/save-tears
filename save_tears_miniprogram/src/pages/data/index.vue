<template>
  <EditorialPage tone="mist">
    <view class="data-page">
      <view class="data-page__header st-panel-raise">
        <text class="st-kicker">Data centre</text>
        <text class="st-display data-page__headline">Clean signals</text>
        <text class="st-subtitle data-page__subline">
          {{ currentUser ? `${currentUser.room_number || 'Room'}` : 'Sign in' }}
        </text>
      </view>

      <EditorialEmptyState
        v-if="!currentUser"
        title="请先登录再查看数据中心"
        message="登录后查看数据"
        action-text="去登录"
        @action="goToLogin"
      />

      <template v-else>
        <SegmentTabs v-model="selectedTab" :options="tabOptions" />

        <view class="data-card st-panel-raise">
          <view class="data-card__topline"></view>
          <view class="data-card__water data-card__water--base"></view>
          <view class="data-card__water data-card__water--crest"></view>
          <view class="data-card__caustic"></view>
          <view class="data-card__head">
            <view>
              <text class="data-card__eyebrow">{{ currentPanel.kicker }}</text>
              <text class="data-card__value">{{ currentPanel.heroValue }}</text>
              <text class="data-card__copy">{{ currentPanel.summary }}</text>
            </view>
          </view>

          <view v-if="loading" class="data-card__loading">正在整理趋势图...</view>
          <EditorialEmptyState
            v-else-if="errorMessage"
            title="暂时无法读取这组数据"
            :message="errorMessage"
            action-text="重新加载"
            @action="loadDataCenter"
          />
          <MiniTrendChart v-else :points="currentPanel.points" :unit="currentPanel.unit" />
        </view>

        <view class="data-page__metrics">
          <MetricCard
            v-for="metric in currentPanel.metrics"
            :key="metric.label"
            :label="metric.label"
            :value="metric.value"
            :tone="metric.tone"
            compact
          />
        </view>

        <view class="data-list st-panel-raise">
          <view class="data-list__topline"></view>
          <text class="data-list__title">Detail log</text>

          <EditorialEmptyState
            v-if="!currentPanel.rows.length && !loading && !errorMessage"
            title="这组数据还没有记录"
            :message="emptyMessage"
          />

          <template v-else>
            <view class="data-list__head">
              <text>{{ currentPanel.columns[0] }}</text>
              <text>{{ currentPanel.columns[1] }}</text>
            </view>
            <view v-for="row in currentPanel.rows" :key="row.id" class="data-list__row">
              <text class="data-list__primary">{{ row.primary }}</text>
              <text class="data-list__secondary">{{ row.secondary }}</text>
            </view>
          </template>
        </view>
      </template>
    </view>
  </EditorialPage>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { onLoad, onShow } from '@dcloudio/uni-app';

import EditorialEmptyState from '@/components/EditorialEmptyState.vue';
import EditorialPage from '@/components/EditorialPage.vue';
import MetricCard from '@/components/MetricCard.vue';
import MiniTrendChart from '@/components/MiniTrendChart.vue';
import SegmentTabs from '@/components/SegmentTabs.vue';
import { getSewageTurbidity, getWaterBill, getWaterFlow } from '@/api/index';
import {
  buildWaterBillInsights,
  buildWaterFlowInsights,
  buildWaterQualityInsights,
  type WaterBillRecord,
  type WaterFlowRecord,
  type WaterQualityRecord,
} from '@/utils/insights';
import { consumeResidentDataTab, type ResidentDataTab } from '@/utils/data-nav';
import { getStoredUser, type StoredUser } from '@/utils/session';

const currentUser = ref<StoredUser | null>(null);
const selectedTab = ref<ResidentDataTab>('flow');
const loading = ref(false);
const errorMessage = ref('');
const flowRecords = ref<WaterFlowRecord[]>([]);
const billRecords = ref<WaterBillRecord[]>([]);
const qualityRecords = ref<WaterQualityRecord[]>([]);

const tabOptions = [
  { label: '用水', value: 'flow', helper: 'Water' },
  { label: '账单', value: 'bill', helper: 'Bills' },
  { label: '水质', value: 'quality', helper: 'Quality' },
];

onLoad((options) => {
  const requestedTab = (options?.tab || '') as ResidentDataTab;
  if (requestedTab === 'flow' || requestedTab === 'bill' || requestedTab === 'quality') {
    selectedTab.value = requestedTab;
  }
});

onShow(() => {
  const queuedTab = consumeResidentDataTab();
  if (queuedTab === 'flow' || queuedTab === 'bill' || queuedTab === 'quality') {
    selectedTab.value = queuedTab;
  }

  void loadDataCenter();
});

const flowInsights = computed(() => buildWaterFlowInsights(flowRecords.value));
const billInsights = computed(() => buildWaterBillInsights(billRecords.value));
const qualityInsights = computed(() => buildWaterQualityInsights(qualityRecords.value));

const currentPanel = computed(() => {
  if (selectedTab.value === 'bill') {
    return {
      kicker: 'Billing ledger',
      heroValue: billInsights.value.latest ? `¥${billInsights.value.latest}` : 'Pending',
      summary: billInsights.value.summary,
      points: billInsights.value.points,
      unit: '',
      metrics: [
        { label: 'Latest', value: billInsights.value.latest ? `¥${billInsights.value.latest}` : 'Pending', tone: 'deep' as const },
        { label: 'Total', value: `¥${billInsights.value.total}`, tone: 'mist' as const },
        {
          label: 'Change',
          value: `${billInsights.value.deltaFromPrevious >= 0 ? '+' : ''}${billInsights.value.deltaFromPrevious}`,
          tone: billInsights.value.deltaFromPrevious > 0 ? 'warning' as const : 'mist' as const,
        },
      ],
      columns: ['Month', 'Amount'],
      rows: [...billRecords.value]
        .sort((left, right) => right.month.localeCompare(left.month))
        .map((record) => ({
          id: `${record.id || record.month}-bill`,
          primary: record.month,
          secondary: `¥${record.amount}`,
        })),
    };
  }

  if (selectedTab.value === 'quality') {
    return {
      kicker: 'Water quality',
      heroValue: qualityInsights.value.latest ? `${qualityInsights.value.latest} NTU` : 'Pending',
      summary: qualityInsights.value.summary,
      points: qualityInsights.value.points,
      unit: '',
      metrics: [
        {
          label: 'Latest',
          value: qualityInsights.value.latest ? `${qualityInsights.value.latest} NTU` : 'Pending',
          tone: qualityInsights.value.statusTone === 'watch' ? 'warning' as const : 'deep' as const,
        },
        { label: 'Average', value: `${qualityInsights.value.average} NTU`, tone: 'mist' as const },
        {
          label: 'Flags',
          value: `${qualityInsights.value.anomalyCount}`,
          tone: qualityInsights.value.anomalyCount ? 'warning' as const : 'mist' as const,
        },
      ],
      columns: ['Timestamp', 'Quality'],
      rows: [...qualityRecords.value]
        .sort((left, right) => right.timestamp.localeCompare(left.timestamp))
        .map((record) => ({
          id: `${record.id || record.timestamp}-quality`,
          primary: record.timestamp.replace('T', ' ').slice(0, 16),
          secondary: `${record.turbidity_value} NTU`,
        })),
    };
  }

  return {
    kicker: 'Water usage',
    heroValue: `${flowInsights.value.total} L`,
    summary: flowInsights.value.summary,
    points: flowInsights.value.points,
    unit: '',
    metrics: [
      { label: 'Peak', value: `${flowInsights.value.peak} L`, tone: 'deep' as const },
      { label: 'Average', value: `${flowInsights.value.average} L`, tone: 'mist' as const },
      {
        label: 'Spikes',
        value: `${flowInsights.value.anomalyCount}`,
        tone: flowInsights.value.anomalyCount ? 'warning' as const : 'mist' as const,
      },
    ],
    columns: ['Timestamp', 'Flow'],
    rows: [...flowRecords.value]
      .sort((left, right) => right.timestamp.localeCompare(left.timestamp))
      .map((record) => ({
        id: `${record.id || record.timestamp}-flow`,
        primary: record.timestamp.replace('T', ' ').slice(0, 16),
        secondary: `${record.flow_rate} L`,
      })),
  };
});

const emptyMessage = computed(() => {
  if (selectedTab.value === 'bill') return '后端还没有同步到账单记录。';
  if (selectedTab.value === 'quality') return '后端还没有同步到浊度记录。';
  return '后端还没有同步到用水记录。';
});

async function loadDataCenter() {
  currentUser.value = getStoredUser();
  errorMessage.value = '';

  if (!currentUser.value?.room_number) {
    flowRecords.value = [];
    billRecords.value = [];
    qualityRecords.value = [];
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
  } catch (error: any) {
    errorMessage.value = error?.message || '数据中心暂时不可用，请稍后再试。';
  } finally {
    loading.value = false;
  }
}

function goToLogin() {
  uni.navigateTo({ url: '/pages/login/index' });
}
</script>

<style scoped>
.data-page__header {
  padding: 18rpx 6rpx 24rpx;
}

.data-page__headline {
  margin-top: 10rpx;
}

.data-page__subline {
  margin-top: 14rpx;
}

.data-card {
  position: relative;
  margin-top: 18rpx;
  padding: 28rpx 24rpx 24rpx;
  border-radius: var(--st-radius-xl);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(236, 247, 255, 0.98) 100%);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow);
  overflow: hidden;
}

.data-card__water {
  position: absolute;
  left: -10%;
  width: 120%;
  border-radius: 50% 50% 0 0;
  pointer-events: none;
}

.data-card__water--base {
  bottom: 22rpx;
  height: 134rpx;
  background: linear-gradient(180deg, rgba(223, 241, 255, 0) 0%, rgba(182, 224, 255, 0.16) 36%, rgba(118, 196, 255, 0.28) 100%);
  filter: blur(2rpx);
  opacity: 0.84;
  animation: st-water-swell-up 6.8s ease-in-out infinite;
}

.data-card__water--crest {
  bottom: 84rpx;
  left: -4%;
  width: 108%;
  height: 56rpx;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.34) 44%, rgba(204, 236, 255, 0.54) 100%);
  filter: blur(5rpx);
  opacity: 0.72;
  animation: st-water-swell-down 5.4s ease-in-out infinite;
}

.data-card__caustic {
  position: absolute;
  left: -8%;
  bottom: 116rpx;
  width: 116%;
  height: 26rpx;
  border-radius: 999rpx;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.28) 26%, rgba(255, 255, 255, 0.58) 50%, rgba(255, 255, 255, 0.28) 74%, rgba(255, 255, 255, 0) 100%);
  filter: blur(6rpx);
  opacity: 0.62;
  transform: rotate(-3deg);
  pointer-events: none;
  animation: st-water-scan 4.8s linear infinite;
}

.data-card__topline,
.data-list__topline {
  position: absolute;
  left: 20rpx;
  right: 20rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.data-card__head {
  margin-bottom: 20rpx;
}

.data-card__eyebrow {
  display: block;
  font-size: 22rpx;
  color: var(--st-accent-deep);
}

.data-card__value {
  display: block;
  margin-top: 10rpx;
  font-family: var(--st-title-font);
  font-size: 60rpx;
  line-height: 1;
  font-weight: 700;
  color: var(--st-text);
}

.data-card__copy {
  display: block;
  margin-top: 16rpx;
  font-size: 24rpx;
  line-height: 1.55;
  color: var(--st-text-soft);
}

.data-card__loading {
  padding: 24rpx 0 20rpx;
  font-size: 26rpx;
  color: var(--st-text-soft);
}

.data-page__metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14rpx;
  margin-top: 18rpx;
}

.data-list {
  position: relative;
  margin-top: 18rpx;
  padding: 28rpx 22rpx 18rpx;
  border-radius: var(--st-radius-xl);
  background: rgba(255, 255, 255, 0.94);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow-tight);
}

.data-list__title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: var(--st-text);
}

.data-list__head,
.data-list__row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 18rpx;
  align-items: center;
}

.data-list__head {
  padding: 18rpx 0 14rpx;
  margin-top: 14rpx;
  border-bottom: 1rpx solid rgba(215, 232, 245, 0.96);
  font-size: 22rpx;
  color: var(--st-text-muted);
}

.data-list__row {
  padding: 20rpx 0;
  border-bottom: 1rpx solid rgba(215, 232, 245, 0.72);
}

.data-list__row:last-child {
  border-bottom: 0;
}

.data-list__primary,
.data-list__secondary {
  font-size: 24rpx;
  line-height: 1.45;
  color: var(--st-text);
}

.data-list__secondary {
  color: var(--st-text-soft);
}
</style>
