<template>
  <view class="home-page">
    <!-- 背景图层 -->
    <image class="bg-image" src="/static/images/bg_login.jpg" mode="aspectFill" /> <!-- TODO: Replace background image here -->
    
    <!-- 主内容区域 -->
    <view class="content-wrapper">
      <!-- 头部区域 -->
      <view class="header-section">
        <view class="header-row">
          <text class="welcome-text">welcome back, {{ username }}</text>
          <image class="avatar-small" src="/static/images/logo_avatar.jpg" mode="aspectFill" /> <!-- TODO: Replace small avatar here -->
        </view>
        <text class="title-text">Today's challenges</text>
      </view>

      <!-- 影响卡片区域 -->
      <view class="impact-card">
        <view class="impact-badge">
          <text class="impact-badge-text">your impact</text>
        </view>
        <view class="impact-content">
          <view class="impact-stats">
            <text class="liters-text">250 Liters</text>
            <text class="saved-text">total water saved this month</text>
          </view>
          <view class="impact-icon">
            <text class="water-emoji">💧</text>
          </view>
        </view>
        <view class="equivalent-row">
          <text class="bottle-emoji">🍶</text>
          <view class="equivalent-text-wrapper">
            <text class="equivalent-label">Equivalent to</text>
            <text class="equivalent-value">Filling 500 water bottles.</text>
          </view>
          <text class="keep-up-text">Keep it up!</text>
        </view>
      </view>

      <!-- 每日生态任务区域 -->
      <view class="tasks-section">
        <view class="tasks-header">
          <text class="tasks-title">Daily Eco-Tasks</text>
          <text class="view-all">View All</text>
        </view>

        <!-- 任务卡片1 -->
        <view class="task-card">
          <view class="task-icon-wrapper">
            <text class="task-emoji">🚿</text>
          </view>
          <view class="task-content">
            <text class="task-name">2-Minute Shower</text>
            <text class="task-desc">Save up to……</text>
            <view class="progress-bar">
              <view class="progress-fill" style="width: 60%"></view>
            </view>
          </view>
          <view class="xp-badge">
            <text class="xp-text">+10XP</text>
          </view>
        </view>

        <!-- 任务卡片2 -->
        <view class="task-card">
          <view class="task-icon-wrapper">
            <text class="task-emoji">🪥</text>
          </view>
          <view class="task-content">
            <text class="task-name">Tap Off While Brushing</text>
            <text class="task-desc">Don't let it run!</text>
            <view class="progress-bar">
              <view class="progress-fill" style="width: 30%"></view>
            </view>
          </view>
          <view class="xp-badge">
            <text class="xp-text">+5XP</text>
          </view>
        </view>

        <!-- 任务卡片3 (已完成) -->
        <view class="task-card completed">
          <view class="task-icon-wrapper small">
            <text class="task-emoji">👕</text>
          </view>
          <view class="task-content">
            <text class="task-name">Full Load Laundry</text>
            <text class="task-completed">completed</text>
          </view>
        </view>
      </view>

      <!-- 底部快捷入口 -->
      <view class="shortcuts-section">
        <view class="shortcut-card blue">
          <text class="shortcut-text">Weekly challenge</text>
        </view>
        <view class="shortcut-card pink">
          <text class="shortcut-text">Consumption</text>
        </view>
        <view class="shortcut-card teal">
          <text class="shortcut-text">More tips</text>
        </view>
      </view>
    </view>

    <!-- 底部安全区域 -->
    <view class="safe-area-bottom"></view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const username = ref('xxx');

onMounted(() => {
  const userInfo = uni.getStorageSync('user');
  if (userInfo) {
    try {
      const user = JSON.parse(userInfo);
      username.value = user.username || 'xxx';
    } catch (e) {
      console.error('解析用户信息失败', e);
    }
  }
});
</script>

<style scoped>
.home-page { position: relative; width: 100%; min-height: 100vh; background: #FFFFFF; overflow: hidden; }
.bg-image { position: absolute; width: 1752rpx; height: 3144rpx; left: -468rpx; top: -1048rpx; opacity: 0.3; }
.content-wrapper { position: relative; z-index: 10; padding-top: 120rpx; padding-bottom: 160rpx; }
.header-section { padding: 0 44rpx; margin-bottom: 30rpx; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20rpx; }
.welcome-text { font-size: 26rpx; color: #3E4346; }
.avatar-small { width: 64rpx; height: 60rpx; border-radius: 50%; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); }
.title-text { font-style: italic; font-weight: 600; font-size: 64rpx; color: #3886CB; text-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); }
.impact-card { margin: 0 44rpx; height: 354rpx; background: linear-gradient(135deg, #E8F4FD 0%, #D4E9F7 100%); box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); border-radius: 34rpx; padding: 30rpx; margin-bottom: 40rpx; }
.impact-badge { display: inline-block; background: rgba(4, 66, 84, 0.2); border-radius: 72rpx; padding: 8rpx 24rpx; margin-bottom: 20rpx; }
.impact-badge-text { font-weight: 800; font-size: 26rpx; color: #044254; }
.impact-content { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20rpx; }
.impact-stats { flex: 1; }
.liters-text { display: block; font-weight: 800; font-size: 48rpx; color: #000000; }
.saved-text { display: block; font-weight: 500; font-size: 28rpx; color: #827979; }
.impact-icon { width: 126rpx; height: 126rpx; background: rgba(255, 255, 255, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.water-emoji { font-size: 60rpx; }
.equivalent-row { display: flex; align-items: center; }
.bottle-emoji { font-size: 50rpx; }
.equivalent-text-wrapper { flex: 1; margin-left: 16rpx; }
.equivalent-label { display: block; font-weight: 800; font-size: 28rpx; color: #000000; }
.equivalent-value { display: block; font-size: 28rpx; color: #3783D9; }
.keep-up-text { font-size: 28rpx; color: #000000; }
.tasks-section { padding: 0 44rpx; }
.tasks-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20rpx; }
.tasks-title { font-weight: 500; font-size: 40rpx; color: #000000; }
.view-all { font-weight: 500; font-size: 26rpx; color: #004EB3; }
.task-card { display: flex; align-items: center; background: linear-gradient(135deg, #E8F0E8 0%, #D4E4D8 100%); box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); border-radius: 34rpx; padding: 24rpx; margin-bottom: 20rpx; min-height: 140rpx; }
.task-card.completed { min-height: 100rpx; }
.task-icon-wrapper { width: 98rpx; height: 90rpx; background: rgba(255, 255, 255, 0.8); border-radius: 34rpx; display: flex; align-items: center; justify-content: center; margin-right: 20rpx; }
.task-icon-wrapper.small { width: 62rpx; height: 58rpx; }
.task-emoji { font-size: 50rpx; }
.task-content { flex: 1; }
.task-name { display: block; font-weight: 600; font-size: 32rpx; color: #000000; }
.task-desc { display: block; font-size: 26rpx; color: #012F37; margin-top: 6rpx; }
.task-completed { display: block; font-weight: 500; font-size: 32rpx; color: #0E7022; margin-top: 6rpx; }
.progress-bar { width: 100%; height: 22rpx; background: #D9D9D9; border-radius: 44rpx; margin-top: 12rpx; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%); border-radius: 44rpx; }
.xp-badge { background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%); border-radius: 34rpx; padding: 10rpx 20rpx; }
.xp-text { font-weight: 600; font-size: 32rpx; color: #0D5B24; }
.shortcuts-section { display: flex; justify-content: space-between; padding: 0 44rpx; margin-top: 30rpx; }
.shortcut-card { width: 184rpx; height: 166rpx; border-radius: 34rpx; display: flex; align-items: center; justify-content: center; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); }
.shortcut-card.blue { background: rgba(119, 166, 226, 0.62); }
.shortcut-card.pink { background: rgba(209, 190, 190, 0.6); }
.shortcut-card.teal { background: rgba(138, 189, 190, 0.51); }
.shortcut-text { font-weight: 500; font-size: 28rpx; text-align: center; color: #333131; }
.safe-area-bottom { height: 200rpx; }
</style>
