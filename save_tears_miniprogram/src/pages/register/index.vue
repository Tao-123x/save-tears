<template>
  <view class="register-page">
    <!-- 背景图层 -->
    <image class="bg-image" src="/static/images/bg_login.jpg" mode="aspectFill" />
    
    <!-- 主内容区域 -->
    <view class="content-wrapper">
      <!-- Logo 头像区域 -->
      <view class="logo-section">
        <image class="logo-avatar" src="/static/images/logo_avatar.jpg" mode="aspectFill" />
        <text class="welcome-text">Create Account</text>
      </view>

      <!-- 表单区域 -->
      <view class="form-section">
        <view class="input-wrapper">
          <input class="input-field" type="text" placeholder="Username……" placeholder-class="placeholder-text" v-model="username" />
        </view>
        <view class="input-wrapper">
          <input class="input-field" type="text" placeholder="Email……" placeholder-class="placeholder-text" v-model="email" />
        </view>
        <view class="input-wrapper">
          <input class="input-field" type="password" placeholder="Password……" placeholder-class="placeholder-text" v-model="password" />
        </view>
        <view class="input-wrapper">
          <input class="input-field" type="password" placeholder="Confirm Password……" placeholder-class="placeholder-text" v-model="confirmPassword" />
        </view>
        <view class="input-wrapper">
          <input class="input-field" type="text" placeholder="Room Number……" placeholder-class="placeholder-text" v-model="roomNumber" />
        </view>

        <!-- 同意条款 -->
        <view class="agree-row" @tap="toggleAgree">
          <view class="checkbox" :class="{ 'checked': agreeTerms }">
            <text v-if="agreeTerms" class="check-icon">✓</text>
          </view>
          <text class="agree-text">I agree to the Terms & Conditions</text>
        </view>

        <!-- 注册按钮 -->
        <view class="register-btn" @tap="handleRegister">
          <text class="register-btn-text">Register</text>
          <text class="arrow-icon">→</text>
        </view>

        <!-- 错误/成功提示 -->
        <view v-if="message" class="message-wrapper">
          <text :class="['message', isSuccess ? 'success' : 'error']">{{ message }}</text>
        </view>

        <!-- 登录引导 -->
        <view class="login-section">
          <text class="login-hint">Already have an account?</text>
          <text class="login-link" @tap="goToLogin">Log in</text>
        </view>
      </view>
    </view>
    <view class="safe-area-bottom"></view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { registerUser } from '@/api/index';

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const roomNumber = ref('');
const message = ref('');
const isSuccess = ref(false);
const agreeTerms = ref(false);

const toggleAgree = () => { agreeTerms.value = !agreeTerms.value; };

const handleRegister = async () => {
  if (!username.value.trim()) { uni.showToast({ title: '请输入用户名', icon: 'none' }); return; }
  if (!email.value.trim()) { uni.showToast({ title: '请输入邮箱', icon: 'none' }); return; }
  if (!password.value.trim()) { uni.showToast({ title: '请输入密码', icon: 'none' }); return; }
  if (password.value !== confirmPassword.value) { uni.showToast({ title: '两次密码不一致', icon: 'none' }); return; }
  if (!roomNumber.value.trim()) { uni.showToast({ title: '请输入房间号', icon: 'none' }); return; }
  if (!agreeTerms.value) { uni.showToast({ title: '请同意服务条款', icon: 'none' }); return; }

  uni.showLoading({ title: '注册中...' });
  try {
    const result = await registerUser(username.value, password.value, roomNumber.value);
    uni.hideLoading();
    message.value = `注册成功，用户名: ${result.username}`;
    isSuccess.value = true;
    uni.showToast({ title: '注册成功！', icon: 'success', duration: 1500 });
    setTimeout(() => { uni.navigateTo({ url: '/pages/login/index' }); }, 1500);
  } catch (error: any) {
    uni.hideLoading();
    message.value = `注册失败: ${error.message || '网络错误'}`;
    isSuccess.value = false;
    uni.showToast({ title: error.message || '注册失败', icon: 'none', duration: 2000 });
  }
};

const goToLogin = () => { uni.navigateTo({ url: '/pages/login/index' }); };
</script>

<style scoped>
.register-page { position: relative; width: 100%; min-height: 100vh; background: #FFFFFF; overflow: hidden; }
.bg-image { position: absolute; width: 1752rpx; height: 3144rpx; left: -546rpx; top: -1068rpx; opacity: 0.6; }
.content-wrapper { position: relative; z-index: 10; padding-top: 150rpx; padding-bottom: env(safe-area-inset-bottom); }
.logo-section { display: flex; align-items: center; padding: 0 70rpx; margin-bottom: 60rpx; }
.logo-avatar { width: 160rpx; height: 160rpx; border-radius: 50%; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); }
.welcome-text { margin-left: 30rpx; font-size: 44rpx; line-height: 56rpx; color: #000000; }
.form-section { padding: 0 74rpx; }
.input-wrapper { margin-bottom: 30rpx; }
.input-field { width: 100%; height: 86rpx; background: rgba(217, 217, 217, 0.5); border: 1rpx solid #605F5F; box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); border-radius: 46rpx; padding: 0 40rpx; box-sizing: border-box; font-size: 30rpx; color: #000000; }
.placeholder-text { font-size: 30rpx; color: #000000; opacity: 0.5; }
.agree-row { display: flex; align-items: center; margin-bottom: 40rpx; padding: 0 10rpx; }
.checkbox { width: 36rpx; height: 34rpx; background: #D9D9D9; border: 4rpx solid #6B6767; display: flex; align-items: center; justify-content: center; }
.checkbox.checked { background: #3884F5; border-color: #3884F5; }
.check-icon { color: #FFFFFF; font-size: 24rpx; font-weight: bold; }
.agree-text { margin-left: 16rpx; font-size: 26rpx; color: #4E4949; }
.register-btn { display: flex; align-items: center; justify-content: center; width: 344rpx; height: 100rpx; margin: 0 auto; background: rgba(56, 132, 245, 0.8); box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25); border-radius: 34rpx; }
.register-btn:active { opacity: 0.8; transform: scale(0.98); }
.register-btn-text { font-size: 44rpx; color: #000000; }
.arrow-icon { margin-left: 20rpx; font-size: 40rpx; color: #000000; font-weight: bold; }
.message-wrapper { margin-top: 30rpx; text-align: center; }
.message { font-size: 28rpx; }
.message.success { color: #0E7022; }
.message.error { color: #B80F0F; }
.login-section { display: flex; justify-content: center; align-items: center; margin-top: 60rpx; }
.login-hint { font-size: 28rpx; color: #998E8E; }
.login-link { margin-left: 10rpx; font-size: 28rpx; color: #236DB3; text-decoration: underline; }
.safe-area-bottom { height: env(safe-area-inset-bottom); }
</style>
