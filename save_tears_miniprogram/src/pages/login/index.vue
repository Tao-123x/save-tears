<template>
  <EditorialPage tone="mist">
    <view class="auth-page">
      <view class="auth-page__brand st-panel-raise">
        <text class="st-kicker">SAVE TEARS</text>
        <text class="st-display auth-page__headline">Quiet water management</text>
      </view>

      <view class="auth-card st-panel-raise">
        <view class="auth-card__topline"></view>

        <view class="auth-card__field-group">
          <text class="auth-card__label">Username</text>
          <input
            v-model="username"
            class="st-field auth-card__field"
            type="text"
            placeholder="Room 302"
            placeholder-class="st-field-placeholder"
          />
        </view>

        <view class="auth-card__field-group">
          <text class="auth-card__label">Password</text>
          <view class="auth-card__password">
            <input
              v-model="password"
              class="st-field auth-card__field"
              :password="!showPassword"
              placeholder="••••••••"
              placeholder-class="st-field-placeholder"
            />
            <text class="auth-card__toggle" @tap="showPassword = !showPassword">
              {{ showPassword ? 'Hide' : 'Show' }}
            </text>
          </view>
        </view>

        <view class="auth-card__row" @tap="rememberMe = !rememberMe">
          <view class="auth-card__remember">
            <view class="auth-card__check" :class="{ 'auth-card__check--active': rememberMe }"></view>
            <text class="auth-card__remember-text">Remember me</text>
          </view>
        </view>

        <view class="auth-card__actions">
          <view class="st-button auth-card__action" @tap="handleLogin">
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </view>
          <view class="st-button st-button--soft auth-card__action" @tap="goToRegister">Create account</view>
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
import { onShow } from '@dcloudio/uni-app';

import EditorialPage from '@/components/EditorialPage.vue';
import { loginUser } from '@/api/index';
import { getStoredUser, saveStoredUser } from '@/utils/session';

const username = ref('');
const password = ref('');
const rememberMe = ref(false);
const showPassword = ref(false);
const loading = ref(false);
const message = ref('');
const isSuccess = ref(false);

onShow(() => {
  const rememberedUsername = uni.getStorageSync('remembered_username');
  if (rememberedUsername) {
    username.value = rememberedUsername;
    rememberMe.value = true;
  }

  const existingUser = getStoredUser();
  if (existingUser?.username) {
    uni.switchTab({ url: '/pages/home/index' });
  }
});

async function handleLogin() {
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' });
    return;
  }

  if (!password.value.trim()) {
    uni.showToast({ title: '请输入密码', icon: 'none' });
    return;
  }

  loading.value = true;
  message.value = '';
  isSuccess.value = false;

  try {
    const result = await loginUser(username.value.trim(), password.value);
    saveStoredUser(result);

    if (rememberMe.value) {
      uni.setStorageSync('remembered_username', username.value.trim());
    } else {
      uni.removeStorageSync('remembered_username');
    }

    message.value = `欢迎回来，${result.username}。`;
    isSuccess.value = true;
    uni.showToast({ title: '登录成功', icon: 'success' });

    setTimeout(() => {
      uni.switchTab({ url: '/pages/home/index' });
    }, 420);
  } catch (error: any) {
    message.value = error?.message || '登录失败，请检查网络或账号信息。';
    isSuccess.value = false;
    uni.showToast({ title: message.value, icon: 'none' });
  } finally {
    loading.value = false;
  }
}

function goToRegister() {
  uni.navigateTo({ url: '/pages/register/index' });
}
</script>

<style scoped>
.auth-page {
  padding-top: 28rpx;
}

.auth-page__brand {
  padding: 26rpx 8rpx 30rpx;
}

.auth-page__headline {
  margin-top: 14rpx;
  max-width: 440rpx;
  font-size: 66rpx;
}

.auth-page__subtitle {
  margin-top: 18rpx;
  max-width: 520rpx;
}

.auth-card {
  position: relative;
  margin-top: 30rpx;
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

.auth-card__password {
  position: relative;
}

.auth-card__toggle {
  position: absolute;
  right: 22rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 24rpx;
  color: var(--st-accent-deep);
}

.auth-card__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20rpx;
  margin-top: 24rpx;
}

.auth-card__remember {
  display: flex;
  align-items: center;
  gap: 14rpx;
}

.auth-card__check {
  width: 22rpx;
  height: 22rpx;
  border-radius: 50%;
  background: rgba(47, 140, 255, 0.14);
  box-shadow: inset 0 0 0 2rpx rgba(47, 140, 255, 0.28);
  transition: background 180ms ease, box-shadow 180ms ease, transform 180ms ease;
}

.auth-card__check--active {
  background: var(--st-accent);
  box-shadow: 0 0 18rpx rgba(47, 140, 255, 0.3);
  transform: scale(1.04);
}

.auth-card__remember-text,
.auth-card__row-note {
  font-size: 24rpx;
  color: var(--st-text-soft);
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
