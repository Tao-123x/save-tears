<template>
  <view class="login-page">
    <!-- 背景图层 -->
    <image 
      class="bg-image" 
      src="/static/images/bg_login.jpg" 
      mode="aspectFill"
    />
    
    <!-- 主内容区域 -->
    <view class="content-wrapper">
      <!-- Logo 头像区域 -->
      <view class="logo-section">
        <image 
          class="logo-avatar" 
          src="/static/images/logo_avatar.jpg" 
          mode="aspectFill"
        />
        <text class="welcome-text">Welcome to log in!</text>
      </view>

      <!-- 表单区域 -->
      <view class="form-section">
        <!-- 邮箱/用户名输入框 -->
        <view class="input-wrapper">
          <input 
            class="input-field"
            type="text"
            placeholder="Email……"
            placeholder-class="placeholder-text"
            v-model="username"
          />
        </view>

        <!-- 密码输入框 -->
        <view class="input-wrapper">
          <input 
            class="input-field"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Password……"
            placeholder-class="placeholder-text"
            v-model="password"
          />
        </view>

        <!-- 记住我 & 忘记密码 -->
        <view class="options-row">
          <view class="remember-me" @tap="toggleRemember">
            <view class="checkbox" :class="{ 'checked': rememberMe }">
              <text v-if="rememberMe" class="check-icon">✓</text>
            </view>
            <text class="remember-text">Remember me</text>
          </view>
          <text class="forget-password" @tap="handleForgetPassword">Forget password?</text>
        </view>

        <!-- 登录按钮 -->
        <view class="login-btn" @tap="handleLogin">
          <text class="login-btn-text">Log in</text>
          <text class="arrow-icon">→</text>
        </view>

        <!-- 错误/成功提示 -->
        <view v-if="message" class="message-wrapper">
          <text :class="['message', isSuccess ? 'success' : 'error']">{{ message }}</text>
        </view>

        <!-- 注册引导 -->
        <view class="register-section">
          <text class="register-hint">Don't have an account?</text>
          <text class="register-link" @tap="goToRegister">Register</text>
        </view>
      </view>
    </view>

    <!-- 底部安全区域 -->
    <view class="safe-area-bottom"></view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { loginUser } from '@/api/index';

// 响应式数据
const username = ref('');
const password = ref('');
const message = ref('');
const isSuccess = ref(false);
const rememberMe = ref(false);
const showPassword = ref(false);

// 切换记住我
const toggleRemember = () => {
  rememberMe.value = !rememberMe.value;
};

// 忘记密码
const handleForgetPassword = () => {
  uni.showToast({
    title: '请联系管理员重置密码',
    icon: 'none',
    duration: 2000
  });
};

// 登录处理
const handleLogin = async () => {
  // 表单验证
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' });
    return;
  }
  
  if (!password.value.trim()) {
    uni.showToast({ title: '请输入密码', icon: 'none' });
    return;
  }

  message.value = '';
  isSuccess.value = false;

  uni.showLoading({ title: '登录中...' });

  try {
    const result = await loginUser(username.value, password.value);
    
    uni.hideLoading();
    
    message.value = `登录成功，欢迎 ${result.username}！`;
    isSuccess.value = true;
    
    // 使用微信小程序的存储方式
    uni.setStorageSync('user', JSON.stringify(result));
    
    // 如果勾选了记住我，存储用户名
    if (rememberMe.value) {
      uni.setStorageSync('remembered_username', username.value);
    } else {
      uni.removeStorageSync('remembered_username');
    }

    // 跳转到首页
    setTimeout(() => {
      uni.switchTab({ url: '/pages/home/index' });
    }, 1000);
    
  } catch (error: any) {
    uni.hideLoading();
    message.value = `登录失败: ${error.message || '网络错误'}`;
    isSuccess.value = false;
    
    uni.showToast({
      title: error.message || '登录失败',
      icon: 'none',
      duration: 2000
    });
  }
};

// 跳转注册页
const goToRegister = () => {
  uni.navigateTo({ url: '/pages/register/index' });
};

// 页面加载时检查是否有记住的用户名
onMounted(() => {
  const rememberedUsername = uni.getStorageSync('remembered_username');
  if (rememberedUsername) {
    username.value = rememberedUsername;
    rememberMe.value = true;
  }
});
</script>

<style scoped>
/* ==================== 页面容器 ==================== */
.login-page {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: #FFFFFF;
  overflow: hidden;
}

/* ==================== 背景图片 ==================== */
.bg-image {
  position: absolute;
  width: 1752rpx;
  height: 3144rpx;
  left: -546rpx;
  top: -1068rpx;
  opacity: 0.6;
}

/* ==================== 内容包装器 ==================== */
.content-wrapper {
  position: relative;
  z-index: 10;
  padding-top: 200rpx;
  padding-bottom: env(safe-area-inset-bottom);
}

/* ==================== Logo区域 ==================== */
.logo-section {
  display: flex;
  align-items: center;
  padding: 0 70rpx;
  margin-bottom: 100rpx;
}

.logo-avatar {
  width: 196rpx;
  height: 196rpx;
  border-radius: 50%;
  box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25);
}

.welcome-text {
  margin-left: 30rpx;
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 48rpx;
  line-height: 60rpx;
  text-align: center;
  color: #000000;
}

/* ==================== 表单区域 ==================== */
.form-section {
  padding: 0 74rpx;
}

.input-wrapper {
  margin-bottom: 40rpx;
}

.input-field {
  width: 100%;
  height: 90rpx;
  background: rgba(217, 217, 217, 0.5);
  border: 1rpx solid #605F5F;
  box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25);
  border-radius: 46rpx;
  padding: 0 40rpx;
  box-sizing: border-box;
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-size: 32rpx;
  color: #000000;
}

.placeholder-text {
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 32rpx;
  line-height: 40rpx;
  color: #000000;
  opacity: 0.5;
}

/* ==================== 选项行 ==================== */
.options-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 50rpx;
  padding: 0 10rpx;
}

.remember-me {
  display: flex;
  align-items: center;
}

.checkbox {
  width: 36rpx;
  height: 34rpx;
  background: #D9D9D9;
  border: 4rpx solid #6B6767;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox.checked {
  background: #3884F5;
  border-color: #3884F5;
}

.check-icon {
  color: #FFFFFF;
  font-size: 24rpx;
  font-weight: bold;
}

.remember-text {
  margin-left: 16rpx;
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 28rpx;
  line-height: 36rpx;
  color: #4E4949;
}

.forget-password {
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 28rpx;
  line-height: 36rpx;
  color: #236DB3;
}

/* ==================== 登录按钮 ==================== */
.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 344rpx;
  height: 100rpx;
  margin: 0 auto;
  background: rgba(56, 132, 245, 0.8);
  box-shadow: 0 8rpx 8rpx rgba(0, 0, 0, 0.25);
  border-radius: 34rpx;
}

.login-btn:active {
  opacity: 0.8;
  transform: scale(0.98);
}

.login-btn-text {
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 48rpx;
  line-height: 60rpx;
  color: #000000;
}

.arrow-icon {
  margin-left: 20rpx;
  font-size: 40rpx;
  color: #000000;
  font-weight: bold;
}

/* ==================== 消息提示 ==================== */
.message-wrapper {
  margin-top: 30rpx;
  text-align: center;
}

.message {
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-size: 28rpx;
  line-height: 36rpx;
}

.message.success {
  color: #0E7022;
}

.message.error {
  color: #B80F0F;
}

/* ==================== 注册引导 ==================== */
.register-section {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 80rpx;
}

.register-hint {
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 28rpx;
  line-height: 36rpx;
  color: #998E8E;
}

.register-link {
  margin-left: 10rpx;
  font-family: 'Inder', 'PingFang SC', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 28rpx;
  line-height: 36rpx;
  color: #000000;
  text-decoration: underline;
}

/* ==================== 底部安全区域 ==================== */
.safe-area-bottom {
  height: constant(safe-area-inset-bottom);
  height: env(safe-area-inset-bottom);
}
</style>
