<template>
  <view class="empty-state st-panel-raise">
    <view class="empty-state__topline"></view>
    <text class="st-kicker">{{ kicker }}</text>
    <text class="st-title empty-state__title">{{ title }}</text>
    <text class="st-subtitle empty-state__message">{{ message }}</text>
    <view v-if="actionText" class="empty-state__action">
      <view class="st-button st-button--soft" @tap="$emit('action')">{{ actionText }}</view>
    </view>
  </view>
</template>

<script setup lang="ts">
defineEmits<{
  (event: 'action'): void;
}>();

withDefaults(
  defineProps<{
    kicker?: string;
    title: string;
    message: string;
    actionText?: string;
  }>(),
  {
    kicker: '提示',
    actionText: '',
  },
);
</script>

<style scoped>
.empty-state {
  position: relative;
  padding: 30rpx 26rpx;
  border-radius: 26rpx;
  background: rgba(255, 255, 255, 0.94);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow-tight);
  overflow: hidden;
}

.empty-state__topline {
  position: absolute;
  left: 18rpx;
  right: 18rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.empty-state__title {
  margin-top: 10rpx;
}

.empty-state__message {
  margin-top: 10rpx;
}

.empty-state__action {
  margin-top: 22rpx;
}
</style>
