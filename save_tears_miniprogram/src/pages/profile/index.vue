<template>
  <view class="profile-page">
    <!-- 顶部分隔线 -->
    <view class="top-divider"></view>

    <!-- 头部用户信息区域 -->
    <view class="header-section">
      <view class="user-info-row">
        <image class="user-avatar" src="/static/images/logo_avatar.jpg" mode="aspectFill" />
        <view class="user-details">
          <text class="welcome-text">Welcome back.</text>
          <text class="username-text">{{ username }}.</text>
        </view>
        <text class="notification-icon">🔔</text>
      </view>
    </view>

    <!-- 公告栏 -->
    <view class="announcement-bar">
      <text class="announcement-text">📢 Announcement</text>
    </view>

    <!-- 功能入口区域 -->
    <view class="features-section">
      <view class="feature-card" @tap="goToPage('operation')">
        <text class="feature-emoji">⚙️</text>
        <text class="feature-text">Operation</text>
      </view>
      <view class="feature-card" @tap="goToPage('target')">
        <text class="feature-emoji">🎯</text>
        <text class="feature-text">Target</text>
      </view>
      <view class="feature-card" @tap="goToPage('points')">
        <text class="feature-emoji">🏆</text>
        <text class="feature-text">Point Center</text>
      </view>
    </view>

    <!-- 圆形图标区域 -->
    <view class="icons-section">
      <view class="icon-item" @tap="goToPage('attendance')">
        <view class="icon-circle"><text class="icon-emoji">📅</text></view>
        <text class="icon-text">Attendance</text>
      </view>
      <view class="icon-item" @tap="goToPage('chart')">
        <view class="icon-circle"><text class="icon-emoji">📊</text></view>
        <text class="icon-text">Chart</text>
      </view>
      <view class="icon-item" @tap="goToPage('device')">
        <view class="icon-circle"><text class="icon-emoji">📱</text></view>
        <text class="icon-text">Device</text>
      </view>
      <view class="icon-item" @tap="goToPage('personalization')">
        <view class="icon-circle"><text class="icon-emoji">🎨</text></view>
        <text class="icon-text">Personalization</text>
      </view>
    </view>

    <!-- 分隔线 -->
    <view class="section-divider"></view>

    <!-- 水源切换区域 -->
    <view class="water-switch-section">
      <view class="switch-card" :class="{ active: waterType === 'government' }" @tap="waterType = 'government'">
        <text class="switch-text">Government Water</text>
      </view>
      <view class="switch-card grey" :class="{ active: waterType === 'grey' }" @tap="waterType = 'grey'">
        <text class="switch-text white">Grey Water</text>
      </view>
    </view>

    <!-- 数据展示区域 -->
    <view class="data-section">
      <text class="data-title">💧 Water Usage Chart</text>
      <view class="chart-placeholder">
        <text class="chart-text">📈 Chart visualization here</text>
      </view>
    </view>

    <!-- 底部安全区域 -->
    <view class="safe-area-bottom"></view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const username = ref('xxxxxxx');
const waterType = ref('government');

onMounted(() => {
  const userInfo = uni.getStorageSync('user');
  if (userInfo) {
    try {
      const user = JSON.parse(userInfo);
      username.value = user.username || 'xxxxxxx';
    } catch (e) {
      console.error('解析用户信息失败', e);
    }
  }
});

const goToPage = (page: string) => {
  uni.showToast({ title: '功能开发中...', icon: 'none' });
};
</script>

<style scoped>
.profile-page { position: relative; width: 100%; min-height: 100vh; background: #FFFFFF; }
.top-divider { height: 14rpx; background: #D9D9D9; margin-top: 160rpx; }
.header-section { padding: 30rpx 56rpx; }
.user-info-row { display: flex; align-items: center; }
.user-avatar { width: 118rpx; height: 112rpx; border-radius: 50%; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); }
.user-details { flex: 1; margin-left: 28rpx; }
.welcome-text { display: block; font-size: 30rpx; color: rgba(67, 61, 61, 0.81); }
.username-text { display: block; font-size: 32rpx; color: rgba(75, 66, 66, 0.95); margin-top: 6rpx; }
.notification-icon { font-size: 50rpx; }
.announcement-bar { height: 52rpx; background: #FFE2C1; display: flex; align-items: center; padding: 0 30rpx; }
.announcement-text { font-size: 24rpx; color: #FF7124; text-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); }
.features-section { display: flex; justify-content: space-between; padding: 40rpx 56rpx; }
.feature-card { width: 174rpx; height: 164rpx; border-radius: 34rpx; background: linear-gradient(135deg, #E8F4FD 0%, #D4E9F7 100%); box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); display: flex; flex-direction: column; align-items: center; justify-content: center; }
.feature-emoji { font-size: 60rpx; }
.feature-text { margin-top: 10rpx; font-weight: 500; font-size: 26rpx; color: #000000; }
.icons-section { display: flex; justify-content: space-between; padding: 0 56rpx; margin-bottom: 30rpx; }
.icon-item { display: flex; flex-direction: column; align-items: center; }
.icon-circle { width: 126rpx; height: 126rpx; border-radius: 50%; background: linear-gradient(135deg, #F0F4F8 0%, #E4E8EC 100%); box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); display: flex; align-items: center; justify-content: center; }
.icon-emoji { font-size: 50rpx; }
.icon-text { margin-top: 12rpx; font-size: 22rpx; text-align: center; color: #000000; }
.section-divider { height: 14rpx; background: #D9D9D9; }
.water-switch-section { display: flex; justify-content: center; padding: 30rpx 52rpx; }
.switch-card { width: 266rpx; height: 106rpx; background: #FFFFFF; border-radius: 34rpx; display: flex; align-items: center; justify-content: center; border: 2rpx solid #ccc; }
.switch-card.active { background: rgba(91, 152, 242, 0.5); border-color: #5B98F2; }
.switch-card.grey { background: #0F528D; margin-left: 20rpx; border-color: #0F528D; }
.switch-card.grey.active { background: #3886CB; }
.switch-text { font-weight: 500; font-size: 28rpx; text-align: center; color: #000000; }
.switch-text.white { color: #FFFFFF; }
.data-section { padding: 30rpx 56rpx; }
.data-title { font-weight: 600; font-size: 32rpx; color: #000000; }
.chart-placeholder { margin-top: 20rpx; height: 300rpx; background: linear-gradient(135deg, #E8F4FD 0%, #D4E9F7 100%); border-radius: 20rpx; display: flex; align-items: center; justify-content: center; }
.chart-text { font-size: 28rpx; color: #666; }
.safe-area-bottom { height: 200rpx; }
</style>
