<template>
  <view class="admin-stat-card st-panel-raise" :class="{ 'admin-stat-card--minimal': !helper }">
    <view class="admin-stat-card__topline"></view>
    <view class="admin-stat-card__dot"></view>
    <text class="admin-stat-card__label">{{ label }}</text>
    <text class="admin-stat-card__value">{{ value }}</text>
    <text v-if="helper" class="admin-stat-card__helper">{{ helper }}</text>
  </view>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  label: string;
  value: string;
  helper?: string;
}>(), {
  helper: '',
});
</script>

<style scoped>
.admin-stat-card {
  position: relative;
  min-height: 132rpx;
  padding: 22rpx 20rpx;
  border-radius: 24rpx;
  border: 1rpx solid var(--st-line);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--st-shadow-tight);
  overflow: hidden;
}

.admin-stat-card--minimal {
  min-height: 112rpx;
}

.admin-stat-card__topline {
  position: absolute;
  left: 16rpx;
  right: 16rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.admin-stat-card__dot {
  position: absolute;
  top: 16rpx;
  right: 16rpx;
  width: 14rpx;
  height: 14rpx;
  border-radius: 50%;
  background: rgba(139, 212, 255, 0.52);
  box-shadow: 0 0 14rpx rgba(139, 212, 255, 0.42);
}

.admin-stat-card__label {
  display: block;
  font-size: 20rpx;
  letter-spacing: 0.08em;
  color: var(--st-text-soft);
}

.admin-stat-card__value {
  display: block;
  margin-top: 12rpx;
  font-family: var(--st-title-font);
  font-size: 40rpx;
  line-height: 1;
  font-weight: 700;
  color: var(--st-text);
}

.admin-stat-card__helper {
  display: block;
  margin-top: 12rpx;
  font-size: 20rpx;
  line-height: 1.4;
  color: var(--st-text-muted);
}
</style>
