<template>
  <view class="metric-card st-panel-raise" :class="[`metric-card--${tone}`, compact ? 'metric-card--compact' : '', !helper ? 'metric-card--minimal' : '']">
    <view class="metric-card__topline"></view>
    <view class="metric-card__dot"></view>
    <text class="metric-card__label">{{ label }}</text>
    <text class="metric-card__value">{{ value }}</text>
    <text v-if="helper" class="metric-card__helper">{{ helper }}</text>
  </view>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string;
    value: string;
    helper?: string;
    tone?: 'mist' | 'deep' | 'warning';
    compact?: boolean;
  }>(),
  {
    helper: '',
    tone: 'mist',
    compact: false,
  },
);
</script>

<style scoped>
.metric-card {
  position: relative;
  min-height: 166rpx;
  padding: 24rpx 22rpx 22rpx;
  border-radius: 24rpx;
  overflow: hidden;
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow-tight);
}

.metric-card--mist {
  background: rgba(255, 255, 255, 0.94);
}

.metric-card--deep {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(223, 241, 255, 0.98) 100%);
}

.metric-card--warning {
  background: var(--st-warning-soft);
  border-color: rgba(242, 164, 74, 0.16);
}

.metric-card--compact {
  min-height: 128rpx;
  padding-bottom: 18rpx;
}

.metric-card--minimal {
  min-height: 116rpx;
}

.metric-card--compact.metric-card--minimal {
  min-height: 104rpx;
  padding-bottom: 14rpx;
}

.metric-card__topline {
  position: absolute;
  left: 18rpx;
  right: 18rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.metric-card__dot {
  position: absolute;
  top: 16rpx;
  right: 18rpx;
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: rgba(139, 212, 255, 0.48);
  box-shadow: 0 0 18rpx rgba(139, 212, 255, 0.46);
  animation: st-pulse-soft 3.8s ease-in-out infinite;
}

.metric-card__label {
  display: block;
  font-size: 22rpx;
  letter-spacing: 0.06em;
  color: var(--st-text-soft);
}

.metric-card__value {
  display: block;
  margin-top: 14rpx;
  font-family: var(--st-title-font);
  font-size: 42rpx;
  line-height: 1;
  font-weight: 700;
  color: var(--st-text);
}

.metric-card--compact .metric-card__value {
  font-size: 38rpx;
}

.metric-card__helper {
  display: block;
  margin-top: 12rpx;
  font-size: 22rpx;
  line-height: 1.5;
  color: var(--st-text-soft);
}

.metric-card--warning .metric-card__label,
.metric-card--warning .metric-card__helper {
  color: #9e6c3b;
}

.metric-card--warning .metric-card__value {
  color: #8e5a2d;
}
</style>
