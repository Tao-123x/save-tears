<template>
  <EditorialPage tone="mist">
    <view class="profile-page">
      <view class="profile-page__header st-panel-raise">
        <text class="st-kicker">Account</text>
        <text class="st-display profile-page__headline">Resident profile</text>
      </view>

      <view class="profile-hero st-panel-raise">
        <view class="profile-hero__topline"></view>
        <view class="profile-hero__avatar">{{ avatarLabel }}</view>
        <view class="profile-hero__copy">
          <text class="profile-hero__name">{{ currentUser?.username || 'Guest' }}</text>
          <text class="profile-hero__meta">
            {{ currentUser?.room_number ? `Room ${currentUser.room_number}` : 'No room linked yet' }}
            <text v-if="isAdmin"> · admin access</text>
          </text>
        </view>
        <view v-if="isAdmin" class="profile-hero__admin" @tap="goToAdmin">Admin entry</view>
      </view>

      <view class="profile-setting st-panel-raise">
        <view class="profile-setting__topline"></view>
        <view class="profile-setting__row">
          <view class="profile-setting__copy">
            <text class="profile-setting__title">Billing alerts</text>
            <text class="profile-setting__desc">Monthly and due-date reminders</text>
          </view>
          <switch :checked="dailyDigestEnabled" color="#2f8cff" @change="handleToggle('dailyDigestEnabled', $event)" />
        </view>
      </view>

      <view class="profile-setting st-panel-raise">
        <view class="profile-setting__topline"></view>
        <view class="profile-setting__row">
          <view class="profile-setting__copy">
            <text class="profile-setting__title">Quality alerts</text>
            <text class="profile-setting__desc">Only show unusual readings</text>
          </view>
          <switch :checked="anomalyAlertsEnabled" color="#2f8cff" @change="handleToggle('anomalyAlertsEnabled', $event)" />
        </view>
      </view>

      <view class="profile-system st-panel-raise">
        <view class="profile-system__topline"></view>
        <text class="profile-system__title">{{ isAdmin ? 'System' : 'Support' }}</text>
        <template v-if="isAdmin">
          <text class="profile-system__label">Service endpoint</text>
          <input
            v-model="apiBaseUrl"
            class="st-field profile-system__field"
            type="text"
            placeholder="https://internal.save-tears.local"
            placeholder-class="st-field-placeholder"
          />
          <text class="profile-system__resolved">Current connection: {{ resolvedApiBaseUrl }}</text>
          <view class="profile-system__actions">
            <view class="st-button profile-system__action" @tap="handleSaveApiBaseUrl">Save connection</view>
            <view class="st-button st-button--soft profile-system__action" @tap="handleHelp">Help centre</view>
          </view>
          <view class="profile-system__actions profile-system__actions--secondary">
            <view class="st-button st-button--soft profile-system__action" @tap="handleResetApiBaseUrl">Reset connection</view>
            <view class="st-button st-button--soft profile-system__action" @tap="handleLogout">Log out</view>
          </view>
        </template>
        <view v-else class="profile-system__actions profile-system__actions--single">
          <view class="st-button st-button--soft profile-system__action" @tap="handleHelp">Help centre</view>
          <view class="st-button st-button--soft profile-system__action" @tap="handleLogout">Log out</view>
        </view>
      </view>
    </view>
  </EditorialPage>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { onShow } from '@dcloudio/uni-app';

import EditorialPage from '@/components/EditorialPage.vue';
import { getResolvedApiBaseUrl, getStoredApiBaseUrl, setApiBaseUrl } from '@/api/index';
import { getResidentPreferences, saveResidentPreferences } from '@/utils/preferences';
import { clearStoredUser, getStoredUser, isAdminUser, type StoredUser } from '@/utils/session';

const currentUser = ref<StoredUser | null>(null);
const apiBaseUrl = ref('');
const resolvedApiBaseUrl = ref(getResolvedApiBaseUrl());
const dailyDigestEnabled = ref(true);
const anomalyAlertsEnabled = ref(true);

const isAdmin = computed(() => isAdminUser(currentUser.value));
const avatarLabel = computed(() => (currentUser.value?.username || 'G').slice(0, 1).toUpperCase());

onShow(() => {
  currentUser.value = getStoredUser();
  apiBaseUrl.value = getStoredApiBaseUrl();
  resolvedApiBaseUrl.value = getResolvedApiBaseUrl();

  const preferences = getResidentPreferences();
  dailyDigestEnabled.value = preferences.dailyDigestEnabled;
  anomalyAlertsEnabled.value = preferences.anomalyAlertsEnabled;
});

function handleToggle(key: 'dailyDigestEnabled' | 'anomalyAlertsEnabled', event: any) {
  if (key === 'dailyDigestEnabled') {
    dailyDigestEnabled.value = event.detail.value;
  } else {
    anomalyAlertsEnabled.value = event.detail.value;
  }

  saveResidentPreferences({
    dailyDigestEnabled: dailyDigestEnabled.value,
    anomalyAlertsEnabled: anomalyAlertsEnabled.value,
  });
}

function handleSaveApiBaseUrl() {
  setApiBaseUrl(apiBaseUrl.value.trim());
  resolvedApiBaseUrl.value = getResolvedApiBaseUrl();
  uni.showToast({ title: '连接设置已保存', icon: 'success' });
}

function handleResetApiBaseUrl() {
  setApiBaseUrl('');
  apiBaseUrl.value = '';
  resolvedApiBaseUrl.value = getResolvedApiBaseUrl();
  uni.showToast({ title: '已恢复默认连接', icon: 'success' });
}

function handleHelp() {
  uni.showToast({
    title: '请联系管理员或项目维护人',
    icon: 'none',
  });
}

function handleLogout() {
  clearStoredUser();
  uni.showToast({ title: '已退出登录', icon: 'success' });
  setTimeout(() => {
    uni.navigateTo({ url: '/pages/login/index' });
  }, 280);
}

function goToAdmin() {
  uni.navigateTo({ url: '/pages/admin/index' });
}
</script>

<style scoped>
.profile-page__header {
  padding: 18rpx 6rpx 24rpx;
}

.profile-page__headline {
  margin-top: 10rpx;
}

.profile-page__subline {
  margin-top: 14rpx;
}

.profile-hero,
.profile-setting,
.profile-system {
  position: relative;
  margin-top: 18rpx;
  border-radius: var(--st-radius-xl);
  background: rgba(255, 255, 255, 0.94);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow-tight);
  overflow: hidden;
}

.profile-hero {
  display: grid;
  grid-template-columns: 88rpx minmax(0, 1fr) auto;
  gap: 18rpx;
  align-items: center;
  padding: 28rpx 24rpx;
}

.profile-setting {
  padding: 24rpx;
}

.profile-system {
  padding: 28rpx 24rpx 24rpx;
}

.profile-hero__topline,
.profile-setting__topline,
.profile-system__topline {
  position: absolute;
  left: 18rpx;
  right: 18rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.profile-hero__avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, rgba(215, 238, 255, 1) 0%, rgba(196, 228, 255, 1) 100%);
  color: var(--st-accent-deep);
  font-family: var(--st-title-font);
  font-size: 40rpx;
  font-weight: 700;
  box-shadow: 0 12rpx 24rpx rgba(47, 140, 255, 0.14);
}

.profile-hero__name {
  display: block;
  font-size: 38rpx;
  font-weight: 700;
  color: var(--st-text);
}

.profile-hero__meta {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  line-height: 1.5;
  color: var(--st-text-soft);
}

.profile-hero__admin {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 56rpx;
  padding: 0 24rpx;
  border-radius: 999rpx;
  background: #eaf5ff;
  color: var(--st-accent-deep);
  font-size: 24rpx;
  font-weight: 600;
}

.profile-setting__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24rpx;
}

.profile-setting__copy {
  flex: 1;
}

.profile-setting__title,
.profile-system__title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: var(--st-text);
}

.profile-setting__desc,
.profile-system__resolved {
  display: block;
  margin-top: 8rpx;
  font-size: 22rpx;
  line-height: 1.5;
  color: var(--st-text-soft);
}

.profile-system__label {
  display: block;
  margin-top: 18rpx;
  font-size: 22rpx;
  color: var(--st-text-soft);
}

.profile-system__field {
  margin-top: 12rpx;
  border-radius: 22rpx;
}

.profile-system__actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14rpx;
  margin-top: 20rpx;
}

.profile-system__actions--secondary {
  margin-top: 14rpx;
}

.profile-system__actions--single {
  margin-top: 20rpx;
}

.profile-system__action {
  width: 100%;
}
</style>
