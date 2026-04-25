<template>
  <EditorialPage tone="mist">
    <view class="redirect-page">
      <text class="st-kicker">数据中心</text>
      <text class="st-title">正在前往水质记录。</text>
    </view>
  </EditorialPage>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app';

import EditorialPage from '@/components/EditorialPage.vue';
import { queueResidentDataTab } from '@/utils/data-nav';

onLoad(() => {
  queueResidentDataTab('quality');
  setTimeout(() => {
    uni.switchTab({ url: '/pages/data/index' });
  }, 40);
});
</script>

<style scoped>
.redirect-page {
  padding-top: 120rpx;
}
</style>
