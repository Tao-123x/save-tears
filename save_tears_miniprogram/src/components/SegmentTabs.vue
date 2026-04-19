<template>
  <view class="segment-tabs">
    <view class="segment-tabs__rail">
      <view class="segment-tabs__indicator" :style="indicatorStyle"></view>
      <view
        v-for="option in options"
        :key="option.value"
        class="segment-tabs__item"
        :class="{ 'segment-tabs__item--active': option.value === modelValue }"
        @tap="handleSelect(option.value)"
      >
        <text class="segment-tabs__label">{{ option.label }}</text>
        <text v-if="option.helper" class="segment-tabs__helper">{{ option.helper }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  modelValue: string;
  options: Array<{
    label: string;
    value: string;
    helper?: string;
  }>;
}>();

const emit = defineEmits<{
  (event: 'update:modelValue', value: string): void;
}>();

const activeIndex = computed(() => {
  const index = props.options.findIndex((option) => option.value === props.modelValue);
  return index >= 0 ? index : 0;
});

const indicatorStyle = computed(() => {
  const width = props.options.length ? 100 / props.options.length : 100;
  return {
    width: `${width}%`,
    transform: `translateX(${activeIndex.value * 100}%)`,
  };
});

function handleSelect(value: string) {
  if (value !== props.modelValue) {
    emit('update:modelValue', value);
  }
}
</script>

<style scoped>
.segment-tabs {
  position: relative;
}

.segment-tabs__rail {
  position: relative;
  display: flex;
  border-radius: 24rpx;
  border: 1rpx solid var(--st-line);
  background: rgba(255, 255, 255, 0.84);
  box-shadow: var(--st-shadow-tight);
  overflow: hidden;
}

.segment-tabs__indicator {
  position: absolute;
  left: 0;
  top: 6rpx;
  bottom: 6rpx;
  border-radius: 18rpx;
  background: #eaf5ff;
  box-shadow: 0 10rpx 24rpx rgba(47, 140, 255, 0.12);
  transition: transform 240ms ease, width 240ms ease;
}

.segment-tabs__indicator::before {
  content: "";
  position: absolute;
  left: 20rpx;
  top: 8rpx;
  width: 60rpx;
  height: 18rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.28);
  filter: blur(8rpx);
}

.segment-tabs__item {
  position: relative;
  z-index: 1;
  flex: 1;
  min-height: 88rpx;
  padding: 16rpx 14rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4rpx;
  transition: color 220ms ease;
}

.segment-tabs__label,
.segment-tabs__helper {
  text-align: center;
}

.segment-tabs__label {
  font-size: 26rpx;
  font-weight: 600;
  color: var(--st-text-soft);
}

.segment-tabs__helper {
  font-size: 20rpx;
  color: var(--st-text-muted);
}

.segment-tabs__item--active .segment-tabs__label {
  color: var(--st-accent-deep);
}

.segment-tabs__item--active .segment-tabs__helper {
  color: rgba(27, 111, 215, 0.72);
}
</style>
