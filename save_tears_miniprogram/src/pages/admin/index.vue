<template>
  <view class="admin-page">
    <!-- 背景图层 -->
    <image class="bg-image" src="/static/images/bg_admin.jpg" mode="aspectFill" />
    
    <!-- 顶部导航栏 -->
    <view class="top-nav-bar">
      <view class="nav-tab" :class="{ 'active': activeTab === 'home' }" @tap="switchTab('home')">
        <text class="nav-tab-text">Home</text>
      </view>
      <view class="nav-tab" :class="{ 'active': activeTab === 'explore' }" @tap="switchTab('explore')">
        <text class="nav-tab-text">Explore</text>
      </view>
      <view class="nav-tab" :class="{ 'active': activeTab === 'settings' }" @tap="switchTab('settings')">
        <text class="nav-tab-text">Settings</text>
      </view>
    </view>

    <!-- 搜索框 -->
    <view class="search-wrapper">
      <view class="search-box">
        <text class="search-icon">🔍</text>
        <input class="search-input" type="text" placeholder="Search……" placeholder-class="search-placeholder" v-model="searchText" @confirm="handleSearch" />
      </view>
    </view>

    <!-- 统计卡片区域 -->
    <view class="stats-section">
      <view class="stat-card">
        <text class="stat-title">Awaiting approval</text>
        <text class="stat-value red">{{ awaitingApproval }}</text>
      </view>
      <view class="stat-card">
        <text class="stat-title">Submitted today</text>
        <text class="stat-value red">{{ submittedToday }}</text>
      </view>
    </view>

    <!-- 申请人列表区域 -->
    <view class="applicants-section">
      <view class="table-header">
        <text class="header-cell applicant">Applicant</text>
        <text class="header-cell consumption">Water consumption</text>
        <text class="header-cell operation">Operation</text>
      </view>
      <view class="divider thick"></view>
      <scroll-view class="applicants-list" scroll-y :show-scrollbar="false">
        <view class="applicant-row" v-for="(item, index) in applicantsList" :key="index">
          <view class="applicant-cell">
            <view class="avatar-placeholder"><text class="avatar-text">👤</text></view>
            <text class="applicant-name">{{ item.name || 'xxxx' }}</text>
          </view>
          <text class="consumption-cell">{{ item.consumption || 'xx' }} L</text>
          <text class="operation-cell" @tap="handleOperation(item)">⋯</text>
        </view>
      </scroll-view>
    </view>

    <!-- 底部帮助中心 -->
    <view class="help-center">
      <text class="help-icon">❓</text>
      <text class="help-text">Helping center</text>
    </view>

    <view class="safe-area-bottom"></view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const activeTab = ref('home');
const searchText = ref('');
const awaitingApproval = ref(5);
const submittedToday = ref(12);

const applicantsList = ref([
  { id: 1, name: 'xxxx', consumption: 'xx', status: 'pending' },
  { id: 2, name: 'xxxx', consumption: 'xx', status: 'pending' },
  { id: 3, name: 'xxxx', consumption: 'xx', status: 'pending' },
  { id: 4, name: 'xxxx', consumption: 'xx', status: 'pending' },
  { id: 5, name: 'xxxx', consumption: 'xx', status: 'pending' },
]);

const switchTab = (tab: string) => { activeTab.value = tab; };
const handleSearch = () => { if (searchText.value.trim()) uni.showToast({ title: `搜索: ${searchText.value}`, icon: 'none' }); };
const handleOperation = (item: any) => {
  uni.showActionSheet({
    itemList: ['审批通过', '审批拒绝', '查看详情'],
    success: (res) => {
      const actions = ['已通过审批', '已拒绝申请', '查看详情'];
      uni.showToast({ title: actions[res.tapIndex], icon: res.tapIndex === 0 ? 'success' : 'none' });
    }
  });
};
</script>

<style scoped>
.admin-page { position: relative; width: 100%; min-height: 100vh; background: #FFFFFF; overflow: hidden; }
.bg-image { position: absolute; width: 2632rpx; height: 3250rpx; left: -984rpx; top: -652rpx; opacity: 0.3; }
.top-nav-bar { position: relative; z-index: 20; display: flex; justify-content: space-between; align-items: center; height: 110rpx; background: #D8E5E6; padding: 0 20rpx; margin-top: 100rpx; }
.nav-tab { width: 212rpx; height: 84rpx; background: #FFFFFF; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); border-radius: 34rpx; display: flex; align-items: center; justify-content: center; }
.nav-tab.active { background: #95BEDA; }
.nav-tab-text { font-weight: 400; font-size: 36rpx; text-align: center; color: #000000; }
.search-wrapper { position: relative; z-index: 10; padding: 20rpx 48rpx; }
.search-box { display: flex; align-items: center; width: 100%; height: 64rpx; background: rgba(239, 239, 239, 0.65); border: 2rpx solid #534242; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); padding: 0 20rpx; }
.search-icon { font-size: 40rpx; opacity: 0.5; }
.search-input { flex: 1; height: 100%; font-size: 32rpx; color: #000000; margin-left: 10rpx; }
.search-placeholder { font-size: 32rpx; color: #000000; opacity: 0.35; }
.stats-section { position: relative; z-index: 10; display: flex; justify-content: space-between; padding: 0 72rpx; margin-bottom: 30rpx; }
.stat-card { width: 280rpx; height: 196rpx; background: #FFFFFF; border: 6rpx solid #000000; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); border-radius: 34rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20rpx; }
.stat-title { font-size: 32rpx; text-align: center; color: #000000; }
.stat-value { font-size: 48rpx; text-align: center; margin-top: 10rpx; }
.stat-value.red { color: #B80F0F; }
.applicants-section { position: relative; z-index: 10; margin: 0 26rpx; background: #FFFFFF; border: 4rpx solid #000000; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); border-radius: 20rpx; overflow: hidden; }
.table-header { display: flex; align-items: center; height: 90rpx; padding: 0 20rpx; }
.header-cell { font-size: 32rpx; text-align: center; color: #000000; }
.header-cell.applicant { flex: 2; }
.header-cell.consumption { flex: 2; }
.header-cell.operation { flex: 1; }
.divider { height: 2rpx; background: #000000; margin: 0 20rpx; }
.divider.thick { height: 4rpx; }
.applicants-list { height: 600rpx; padding: 0 20rpx; }
.applicant-row { display: flex; align-items: center; height: 120rpx; border-bottom: 2rpx solid #000000; }
.applicant-cell { flex: 2; display: flex; align-items: center; }
.avatar-placeholder { width: 60rpx; height: 60rpx; background: #D9D9D9; border: 4rpx solid #888888; display: flex; align-items: center; justify-content: center; margin-right: 16rpx; }
.avatar-text { font-size: 30rpx; }
.applicant-name { font-size: 36rpx; color: #787878; }
.consumption-cell { flex: 2; font-size: 36rpx; text-align: center; color: #676161; }
.operation-cell { flex: 1; font-size: 40rpx; text-align: center; color: #5F5252; }
.help-center { position: fixed; left: 42rpx; bottom: 80rpx; display: flex; align-items: center; z-index: 20; }
.help-icon { font-size: 50rpx; opacity: 0.5; }
.help-text { margin-left: 10rpx; font-size: 30rpx; color: #AEB4B5; text-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); }
.safe-area-bottom { height: 200rpx; }
</style>
