<template>
  <EditorialPage tone="mist">
    <view class="auth-page">
      <view class="auth-page__brand st-panel-raise">
        <text class="st-kicker">REGISTER</text>
        <text class="st-display auth-page__headline">Create your resident access</text>
        <text class="st-subtitle auth-page__subtitle">注册页只保留当前后端真实支持的字段，界面则保持同一套白蓝语言。</text>
      </view>

      <view class="auth-card st-panel-raise">
        <view class="auth-card__topline"></view>

        <view class="auth-card__field-group">
          <text class="auth-card__label">Username</text>
          <input
            v-model="username"
            class="st-field auth-card__field"
            type="text"
            placeholder="New resident"
            placeholder-class="st-field-placeholder"
          />
        </view>

        <view class="auth-card__field-group">
          <text class="auth-card__label">Password</text>
          <input
            v-model="password"
            class="st-field auth-card__field"
            password
            placeholder="Create a password"
            placeholder-class="st-field-placeholder"
          />
        </view>

        <view class="auth-card__field-group">
          <text class="auth-card__label">Room</text>
          <input
            v-model="roomNumber"
            class="st-field auth-card__field"
            type="text"
            placeholder="B-302"
            placeholder-class="st-field-placeholder"
          />
        </view>

        <view class="auth-card__actions">
          <view class="st-button auth-card__action" @tap="handleRegister">
            {{ loading ? 'Creating...' : 'Create account' }}
          </view>
          <view class="st-button st-button--soft auth-card__action" @tap="goToLogin">Back to sign in</view>
        </view>

        <text v-if="message" class="auth-card__message" :class="{ 'auth-card__message--error': !isSuccess }">
          {{ message }}
        </text>
      </view>
    </view>
  </EditorialPage>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import EditorialPage from '@/components/EditorialPage.vue';
import { registerUser } from '@/api/index';

const username = ref('');
const password = ref('');
const roomNumber = ref('');
const message = ref('');
const isSuccess = ref(false);
const loading = ref(false);

async function handleRegister() {
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' });
    return;
  }

  if (!password.value.trim()) {
    uni.showToast({ title: '请输入密码', icon: 'none' });
    return;
  }

  if (!roomNumber.value.trim()) {
    uni.showToast({ title: '请输入房间号', icon: 'none' });
    return;
  }

  loading.value = true;
  message.value = '';

  try {
    const result = await registerUser(username.value.trim(), password.value, roomNumber.value.trim());
    message.value = `账号 ${result.username} 已创建，请返回登录。`;
    isSuccess.value = true;
    uni.showToast({ title: '注册成功', icon: 'success' });

    setTimeout(() => {
      uni.navigateTo({ url: '/pages/login/index' });
    }, 460);
  } catch (error: any) {
    message.value = error?.message || '注册失败，请稍后再试。';
    isSuccess.value = false;
    uni.showToast({ title: message.value, icon: 'none' });
  } finally {
    loading.value = false;
  }
}

function goToLogin() {
  uni.navigateTo({ url: '/pages/login/index' });
}
</script>

<style scoped>
.auth-page {
  padding-top: 28rpx;
}

.auth-page__brand {
  padding: 26rpx 8rpx 28rpx;
}

.auth-page__headline {
  margin-top: 14rpx;
  max-width: 480rpx;
  font-size: 62rpx;
}

.auth-page__subtitle {
  margin-top: 18rpx;
  max-width: 540rpx;
}

.auth-card {
  position: relative;
  margin-top: 28rpx;
  padding: 34rpx 28rpx 30rpx;
  border-radius: var(--st-radius-xl);
  background: rgba(255, 255, 255, 0.92);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow);
  overflow: hidden;
}

.auth-card__topline {
  position: absolute;
  left: 22rpx;
  right: 22rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.auth-card__field-group + .auth-card__field-group {
  margin-top: 22rpx;
}

.auth-card__label {
  display: block;
  margin-bottom: 12rpx;
  font-size: 22rpx;
  color: var(--st-text-soft);
}

.auth-card__field {
  border-radius: 22rpx;
}

.auth-card__actions {
  display: grid;
  gap: 16rpx;
  margin-top: 34rpx;
}

.auth-card__action {
  width: 100%;
}

.auth-card__message {
  display: block;
  margin-top: 20rpx;
  font-size: 24rpx;
  line-height: 1.5;
  color: var(--st-success);
}

.auth-card__message--error {
  color: #b45f59;
}
</style>
