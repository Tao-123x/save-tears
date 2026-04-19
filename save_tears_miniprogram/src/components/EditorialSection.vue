<template>
  <view class="editorial-section st-panel-raise" :class="[`editorial-section--${tone}`]">
    <view v-if="tone !== 'bare'" class="editorial-section__topline"></view>
    <view class="editorial-section__header" v-if="kicker || title || subtitle || $slots.actions">
      <view class="editorial-section__copy">
        <text v-if="kicker" class="st-kicker">{{ kicker }}</text>
        <text v-if="title" class="st-title editorial-section__title">{{ title }}</text>
        <text v-if="subtitle" class="st-subtitle editorial-section__subtitle">{{ subtitle }}</text>
      </view>
      <view class="editorial-section__actions" v-if="$slots.actions">
        <slot name="actions" />
      </view>
    </view>
    <slot />
  </view>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    kicker?: string;
    title?: string;
    subtitle?: string;
    tone?: 'light' | 'deep' | 'bare';
  }>(),
  {
    kicker: '',
    title: '',
    subtitle: '',
    tone: 'light',
  },
);
</script>

<style scoped>
.editorial-section {
  position: relative;
  margin-bottom: 24rpx;
  border-radius: var(--st-radius-lg);
  overflow: hidden;
}

.editorial-section--light,
.editorial-section--deep {
  padding: 28rpx;
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow-tight);
}

.editorial-section--light {
  background: rgba(255, 255, 255, 0.9);
}

.editorial-section--deep {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94) 0%, rgba(239, 248, 255, 0.96) 100%);
}

.editorial-section--bare {
  padding: 0;
  margin-bottom: 0;
}

.editorial-section__topline {
  position: absolute;
  left: 28rpx;
  right: 28rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.86);
}

.editorial-section__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20rpx;
  margin-bottom: 22rpx;
}

.editorial-section__copy {
  flex: 1;
}

.editorial-section__title {
  margin-top: 8rpx;
}

.editorial-section__subtitle {
  margin-top: 10rpx;
}

.editorial-section__actions {
  flex-shrink: 0;
}
</style>
