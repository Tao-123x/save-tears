<template>
  <view class="sewage-turbidity-page">
    <view class="header">
        <text class="title">我的污水表</text>
    </view>
    <view v-if="!roomNumber" class="no-login">
        <text>请先登录以查看污水数据。</text>
    </view>
    <view v-else class="content">
      <view class="info-row">
          <text>房间号: {{ roomNumber }}</text>
      </view>
      <button class="refresh-btn" @tap="fetchSewageTurbidityData">刷新数据</button>
      <view v-if="message" :class="['message', { 'error': isError }]">
          <text>{{ message }}</text>
      </view>
      <view v-if="sewageTurbidityData.length" class="data-table">
        <view class="table-header">
          <text class="th">ID</text>
          <text class="th">浊度值 (NTU)</text>
          <text class="th">时间</text>
        </view>
        <view class="table-body">
          <view v-for="data in sewageTurbidityData" :key="data.id" class="table-row">
            <text class="td">{{ data.id }}</text>
            <text class="td">{{ data.turbidity_value }}</text>
            <text class="td">{{ data.timestamp }}</text>
          </view>
        </view>
      </view>
      <view v-else-if="!message" class="no-data">
          <text>暂无污水数据。</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getSewageTurbidity } from '@/api/index';

export default {
  name: 'SewageTurbidityPage',
  data() {
    return {
      roomNumber: '',
      sewageTurbidityData: [],
      message: '',
      isError: false
    };
  },
  onShow() {
    this.loadUserData();
    if (this.roomNumber) {
      this.fetchSewageTurbidityData();
    }
  },
  methods: {
    loadUserData() {
      try {
        const userStr = uni.getStorageSync('user');
        if (userStr) {
            const user = JSON.parse(userStr);
            if (user && user.room_number) {
                this.roomNumber = user.room_number;
            }
        }
      } catch (e) {
          console.error('Error parsing user data', e);
      }
    },
    async fetchSewageTurbidityData() {
      this.message = '';
      this.isError = false;
      try {
        const data = await getSewageTurbidity(this.roomNumber);
        this.sewageTurbidityData = data;
        if (data.length === 0) {
          this.message = '暂无污水数据。请尝试提交一些数据。';
        }
      } catch (error) {
        this.message = `加载污水数据失败: ${error.message}`;
        this.isError = true;
      }
    }
  }
};
</script>

<style scoped>
.sewage-turbidity-page {
  padding: 20px;
}

.title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 20px;
    display: block;
    text-align: center;
}

.table-header {
    display: flex;
    background-color: #f2f2f2;
    padding: 10px 0;
}

.table-row {
    display: flex;
    border-bottom: 1px solid #ddd;
    padding: 10px 0;
}

.th, .td {
    flex: 1;
    text-align: center;
    font-size: 14px;
}

.refresh-btn {
  background-color: #42b983;
  color: white;
  margin-bottom: 20px;
}

.error {
  color: red;
}
</style>
