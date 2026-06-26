<template>
  <EditorialPage tone="mist">
    <view class="data-page">
      <view class="data-page__header st-panel-raise">
        <text class="st-kicker">数据中心</text>
        <text class="st-display data-page__headline">数据</text>
        <text class="st-subtitle data-page__subline">
          {{ currentUser ? `${currentUser.room_number || '房间'}` : '请登录' }}
        </text>
      </view>

      <EditorialEmptyState
        v-if="!currentUser"
        title="请先登录再查看数据中心"
        message="登录后查看自来水、灰水、趋势和节水计划"
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

          <view v-if="loading" class="data-card__loading">正在加载数据...</view>
          <EditorialEmptyState
            v-else-if="errorMessage"
            title="暂时无法显示数据"
            :message="errorMessage"
            action-text="再试一次"
            @action="loadDataCenter"
          />
          <MiniTrendChart v-else :points="currentPanel.points" :unit="currentPanel.unit" />
          <view
            v-if="selectedTab === 'plan' && !loading"
            class="st-button data-card__action"
            @tap="handleGeneratePlan"
          >
            {{ generatingPlan ? '生成中...' : '生成计划' }}
          </view>
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
          <text class="data-list__title">明细</text>

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
import {
  generateSavingPlan,
  getGreywaterUsage,
  getLatestSavingPlan,
  getSavingStats,
  getWaterFlow,
  type GreywaterUsageRecord,
  type SavingPlan,
  type SavingStats,
} from '@/api/index';
import {
  buildWaterFlowInsights,
  type InsightPoint,
  type WaterFlowRecord,
} from '@/utils/insights';
import { consumeResidentDataTab, type ResidentDataTab } from '@/utils/data-nav';
import { getStoredUser, type StoredUser } from '@/utils/session';

const currentUser = ref<StoredUser | null>(null);
const selectedTab = ref<ResidentDataTab>('tap');
const loading = ref(false);
const generatingPlan = ref(false);
const errorMessage = ref('');
const flowRecords = ref<WaterFlowRecord[]>([]);
const greywaterRecords = ref<GreywaterUsageRecord[]>([]);
const savingStats = ref<SavingStats | null>(null);
const latestPlan = ref<SavingPlan | null>(null);

const tabOptions = [
  { label: '自来水', value: 'tap' },
  { label: '灰水', value: 'greywater' },
  { label: '趋势', value: 'trends' },
  { label: '计划', value: 'plan' },
];

onLoad((options) => {
  const requestedTab = (options?.tab || '') as ResidentDataTab;
  if (isSavingDataTab(requestedTab)) {
    selectedTab.value = requestedTab;
  }
});

onShow(() => {
  const queuedTab = consumeResidentDataTab();
  if (isSavingDataTab(queuedTab)) {
    selectedTab.value = queuedTab;
  }

  void loadDataCenter();
});

const flowInsights = computed(() => buildWaterFlowInsights(flowRecords.value));
const greywaterTotal = computed(() => greywaterRecords.value.reduce((sum, record) => sum + Number(record.volume_liters || 0), 0));
const greywaterFlushCount = computed(() => greywaterRecords.value.reduce((sum, record) => {
  return record.usage_type === 'toilet_flush' ? sum + Number(record.event_count || 0) : sum;
}, 0));
const greywaterPoints = computed<InsightPoint[]>(() => {
  return [...greywaterRecords.value]
    .sort((left, right) => left.timestamp.localeCompare(right.timestamp))
    .map((record) => ({
      label: formatDayLabel(record.timestamp),
      value: Number(record.volume_liters || 0),
    }));
});
const replacementRateLabel = computed(() => `${Math.round(Number(savingStats.value?.replacement_rate || 0) * 100)}%`);
const trendPoints = computed<InsightPoint[]>(() => {
  const trends = savingStats.value?.trends || [];
  if (trends.length) {
    return trends.map((point) => ({
      label: point.label,
      value: Math.round(Number(point.replacement_rate || 0) * 100),
    }));
  }

  return [
    { label: '自来水', value: Number(savingStats.value?.tap_water_liters || 0) },
    { label: '灰水', value: Number(savingStats.value?.greywater_liters || 0) },
  ];
});

const currentPanel = computed(() => {
  if (selectedTab.value === 'greywater') {
    return {
      kicker: '灰水',
      heroValue: `${greywaterTotal.value} L`,
      summary: greywaterRecords.value.length
        ? `已记录 ${greywaterFlushCount.value} 次灰水冲厕。`
        : '暂无灰水记录，等待设备或手动记录更新。',
      points: greywaterPoints.value,
      unit: '',
      metrics: [
        { label: '灰水量', value: `${greywaterTotal.value} L`, tone: 'deep' as const },
        { label: '冲厕', value: `${greywaterFlushCount.value}`, tone: 'mist' as const },
        { label: '替代率', value: replacementRateLabel.value, tone: 'mist' as const },
      ],
      columns: ['场景', '用量'],
      rows: [...greywaterRecords.value]
        .sort((left, right) => right.timestamp.localeCompare(left.timestamp))
        .map((record) => ({
          id: `${record.id || record.timestamp}-greywater`,
          primary: `${usageTypeLabel(record.usage_type)} · ${record.timestamp.replace('T', ' ').slice(0, 16)}`,
          secondary: `${record.volume_liters} L`,
        })),
    };
  }

  if (selectedTab.value === 'trends') {
    return {
      kicker: '替代率趋势',
      heroValue: replacementRateLabel.value,
      summary: savingStats.value
        ? `灰水已替代 ${savingStats.value.estimated_savings_liters} L 自来水。`
        : '暂无趋势数据，等待节水统计更新。',
      points: trendPoints.value,
      unit: '',
      metrics: [
        { label: '自来水', value: `${savingStats.value?.tap_water_liters || 0} L`, tone: 'deep' as const },
        { label: '灰水', value: `${savingStats.value?.greywater_liters || 0} L`, tone: 'mist' as const },
        { label: '替代率', value: replacementRateLabel.value, tone: 'mist' as const },
      ],
      columns: ['指标', '数值'],
      rows: [
        { id: 'trend-tap', primary: '自来水累计', secondary: `${savingStats.value?.tap_water_liters || 0} L` },
        { id: 'trend-greywater', primary: '灰水累计', secondary: `${savingStats.value?.greywater_liters || 0} L` },
        { id: 'trend-rate', primary: '灰水替代率', secondary: replacementRateLabel.value },
      ],
    };
  }

  if (selectedTab.value === 'plan') {
    return {
      kicker: 'AI 节水计划',
      heroValue: latestPlan.value ? `${latestPlan.value.estimated_savings_liters} L` : '待生成',
      summary: latestPlan.value?.plan_text || '暂无计划，点击生成后会基于近期自来水和灰水数据给出建议。',
      points: [
        { label: '目标', value: latestPlan.value?.target_flush_count || 0 },
        { label: '当前', value: savingStats.value?.flush_count || 0 },
      ],
      unit: '',
      metrics: [
        { label: '冲厕目标', value: `${latestPlan.value?.target_flush_count || 0}`, tone: 'deep' as const },
        { label: '替代目标', value: `${Math.round(Number(latestPlan.value?.target_replacement_rate || 0) * 100)}%`, tone: 'mist' as const },
        { label: '模型', value: latestPlan.value?.model_name || '未生成', tone: 'mist' as const },
      ],
      columns: ['计划项', '内容'],
      rows: [
        { id: 'plan-text', primary: '建议', secondary: latestPlan.value?.plan_text || '暂无计划' },
        { id: 'plan-target', primary: '灰水冲厕目标', secondary: `${latestPlan.value?.target_flush_count || 0} 次` },
        { id: 'plan-saving', primary: '预计节省', secondary: `${latestPlan.value?.estimated_savings_liters || 0} L` },
      ],
    };
  }

  return {
    kicker: '自来水',
    heroValue: `${flowInsights.value.total} L`,
    summary: flowInsights.value.summary,
    points: flowInsights.value.points,
    unit: '',
    metrics: [
      { label: '峰值', value: `${flowInsights.value.peak} L`, tone: 'deep' as const },
      { label: '平均', value: `${flowInsights.value.average} L`, tone: 'mist' as const },
      {
        label: '提醒',
        value: `${flowInsights.value.anomalyCount}`,
        tone: flowInsights.value.anomalyCount ? 'warning' as const : 'mist' as const,
      },
    ],
    columns: ['时间', '用量'],
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
  if (selectedTab.value === 'greywater') return '还没有灰水记录。';
  if (selectedTab.value === 'trends') return '还没有趋势记录。';
  if (selectedTab.value === 'plan') return '还没有节水计划。';
  return '还没有自来水记录。';
});

async function loadDataCenter() {
  currentUser.value = getStoredUser();
  errorMessage.value = '';

  if (!currentUser.value?.room_number) {
    flowRecords.value = [];
    greywaterRecords.value = [];
    savingStats.value = null;
    latestPlan.value = null;
    return;
  }

  loading.value = true;

  try {
    const [flowResult, greywaterResult, statsResult, planResult] = await Promise.allSettled([
      getWaterFlow(currentUser.value.room_number),
      getGreywaterUsage(currentUser.value.room_number),
      getSavingStats(currentUser.value.room_number),
      getLatestSavingPlan(currentUser.value.room_number),
    ]);

    flowRecords.value = flowResult.status === 'fulfilled' ? flowResult.value : [];
    greywaterRecords.value = greywaterResult.status === 'fulfilled' ? greywaterResult.value : [];
    savingStats.value = statsResult.status === 'fulfilled' ? statsResult.value : null;
    latestPlan.value = planResult.status === 'fulfilled' ? planResult.value : null;

    if (
      flowResult.status === 'rejected'
      && greywaterResult.status === 'rejected'
      && statsResult.status === 'rejected'
      && planResult.status === 'rejected'
    ) {
      errorMessage.value = '暂时没有加载成功，已显示空状态。';
    }
  } finally {
    loading.value = false;
  }
}

async function handleGeneratePlan() {
  if (!currentUser.value?.room_number || generatingPlan.value) {
    return;
  }

  generatingPlan.value = true;
  try {
    latestPlan.value = await generateSavingPlan(currentUser.value.room_number);
    uni.showToast({ title: '计划已生成', icon: 'success' });
  } catch {
    uni.showToast({ title: '生成失败，请稍后再试', icon: 'none' });
  } finally {
    generatingPlan.value = false;
  }
}

function goToLogin() {
  uni.navigateTo({ url: '/pages/login/index' });
}

function isSavingDataTab(value: string): value is ResidentDataTab {
  return value === 'tap' || value === 'greywater' || value === 'trends' || value === 'plan';
}

function usageTypeLabel(value: string) {
  if (value === 'toilet_flush') return '冲厕';
  if (value === 'cleaning') return '清洁';
  return '其他';
}

function formatDayLabel(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value.slice(5, 10) || value;
  }

  return `${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')}`;
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

.data-card__action {
  position: relative;
  z-index: 1;
  margin-top: 22rpx;
  width: 100%;
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
