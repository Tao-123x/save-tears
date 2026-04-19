<template>
  <view class="mini-chart">
    <view class="mini-chart__bars">
      <view v-for="point in normalizedPoints" :key="point.label" class="mini-chart__item">
        <view class="mini-chart__bar-rail">
          <view class="mini-chart__bar" :style="{ height: `${point.height}%` }"></view>
        </view>
        <text class="mini-chart__value">{{ point.value }}{{ unit }}</text>
        <text class="mini-chart__label">{{ point.label }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    points: Array<{
      label: string;
      value: number;
    }>;
    unit?: string;
  }>(),
  {
    unit: '',
  },
);

const normalizedPoints = computed(() => {
  const safePoints = props.points.slice(-6);
  const maxValue = Math.max(...safePoints.map((point) => point.value), 1);

  return safePoints.map((point) => ({
    ...point,
    height: Math.max(18, Math.round((point.value / maxValue) * 100)),
  }));
});
</script>

<style scoped>
.mini-chart {
  padding: 16rpx 0 6rpx;
}

.mini-chart__bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 14rpx;
}

.mini-chart__item {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mini-chart__bar-rail {
  width: 100%;
  height: 168rpx;
  padding: 0 8rpx;
  display: flex;
  align-items: flex-end;
}

.mini-chart__bar {
  width: 100%;
  min-height: 20rpx;
  border-radius: 999rpx 999rpx 18rpx 18rpx;
  background: linear-gradient(180deg, rgba(141, 174, 184, 0.62) 0%, var(--st-accent-deep) 100%);
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.28);
}

.mini-chart__value {
  display: block;
  margin-top: 8rpx;
  font-size: 22rpx;
  color: var(--st-text);
}

.mini-chart__label {
  display: block;
  margin-top: 4rpx;
  font-size: 20rpx;
  color: var(--st-text-muted);
}
</style>
