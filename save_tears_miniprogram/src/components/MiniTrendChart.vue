<template>
  <view class="mini-trend-chart">
    <view class="mini-trend-chart__plot">
      <view class="mini-trend-chart__sheen"></view>
      <view class="mini-trend-chart__grid mini-trend-chart__grid--top"></view>
      <view class="mini-trend-chart__grid mini-trend-chart__grid--mid"></view>
      <view class="mini-trend-chart__grid mini-trend-chart__grid--base"></view>

      <view
        v-for="(segment, index) in geometry.segments"
        :key="`${index}-${segment.left}-${segment.top}`"
        class="mini-trend-chart__segment"
        :style="{
          left: `${(segment.left / PLOT_WIDTH) * 100}%`,
          top: `${(segment.top / PLOT_HEIGHT) * 100}%`,
          width: `${(segment.width / PLOT_WIDTH) * 100}%`,
          transform: `translateY(-50%) rotate(${segment.angle}deg)`,
          animationDelay: `${index * 60}ms`,
        }"
      ></view>

      <view
        v-for="(node, index) in geometry.nodes"
        :key="`${node.label}-${index}`"
        class="mini-trend-chart__node-shell"
        :style="{
          left: `${(node.x / PLOT_WIDTH) * 100}%`,
          top: `${(node.y / PLOT_HEIGHT) * 100}%`,
          animationDelay: `${index * 70 + 120}ms`,
        }"
      >
        <view class="mini-trend-chart__node" :class="{ 'mini-trend-chart__node--current': node.isCurrent }"></view>
      </view>
    </view>

    <view class="mini-trend-chart__labels">
      <view v-for="(node, index) in geometry.nodes" :key="`${node.label}-label-${index}`" class="mini-trend-chart__label-item">
        <text class="mini-trend-chart__label">{{ node.label }}</text>
        <text class="mini-trend-chart__value">{{ node.value }}{{ unit }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';

import { buildTrendGeometry } from '@/utils/insights';

const PLOT_WIDTH = 300;
const PLOT_HEIGHT = 120;

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

const geometry = computed(() => {
  return buildTrendGeometry(props.points, {
    maxPoints: 6,
    width: PLOT_WIDTH,
    height: PLOT_HEIGHT,
    topPadding: 12,
    bottomPadding: 18,
  });
});
</script>

<style scoped>
.mini-trend-chart {
  padding-top: 6rpx;
}

.mini-trend-chart__plot {
  position: relative;
  height: 220rpx;
  overflow: hidden;
}

.mini-trend-chart__sheen {
  position: absolute;
  top: 18rpx;
  bottom: 34rpx;
  left: -18%;
  width: 34%;
  border-radius: 999rpx;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.42) 55%, rgba(255, 255, 255, 0) 100%);
  filter: blur(10rpx);
  animation: st-water-scan 3.4s linear infinite;
  pointer-events: none;
}

.mini-trend-chart__grid {
  position: absolute;
  left: 0;
  right: 0;
  height: 2rpx;
  border-radius: 999rpx;
}

.mini-trend-chart__grid--top {
  top: 30rpx;
  background: rgba(232, 244, 255, 0.92);
}

.mini-trend-chart__grid--mid {
  top: 100rpx;
  background: rgba(221, 239, 253, 0.92);
}

.mini-trend-chart__grid--base {
  bottom: 34rpx;
  background: rgba(215, 232, 245, 0.92);
}

.mini-trend-chart__segment {
  position: absolute;
  height: 8rpx;
  border-radius: 999rpx;
  transform-origin: 0 50%;
  background: linear-gradient(90deg, var(--st-accent) 0%, var(--st-accent-deep) 100%);
  box-shadow: 0 6rpx 16rpx rgba(47, 140, 255, 0.18);
  animation: mini-trend-build 480ms ease both;
}

.mini-trend-chart__node-shell {
  position: absolute;
  width: 24rpx;
  height: 24rpx;
  transform: translate(-50%, -50%);
  animation: mini-trend-fade 360ms ease both;
}

.mini-trend-chart__node {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #ffffff;
  border: 4rpx solid var(--st-accent);
  box-shadow: 0 0 0 8rpx rgba(47, 140, 255, 0.06);
}

.mini-trend-chart__node--current {
  border-color: var(--st-accent-deep);
  box-shadow: 0 0 0 12rpx rgba(47, 140, 255, 0.12);
}

.mini-trend-chart__labels {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14rpx 18rpx;
}

.mini-trend-chart__label-item {
  min-width: 0;
}

.mini-trend-chart__label {
  display: block;
  font-size: 22rpx;
  color: var(--st-text-muted);
}

.mini-trend-chart__value {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  color: var(--st-text-soft);
}

@keyframes mini-trend-build {
  0% {
    opacity: 0;
    width: 0;
  }

  100% {
    opacity: 1;
  }
}

@keyframes mini-trend-fade {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.7);
  }

  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}
</style>
