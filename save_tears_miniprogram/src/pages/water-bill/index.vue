<template>
  <view class="water-bill-page">
    <view class="header">
        <text class="title">我的水费账单</text>
    </view>
    <view v-if="!roomNumber" class="no-login">
        <text>请先登录以查看水费账单。</text>
    </view>
    <view v-else class="content">
      <view class="info-row">
          <text>房间号: {{ roomNumber }}</text>
      </view>
      <button class="refresh-btn" @tap="fetchWaterBillData">刷新数据</button>
      <view v-if="message" :class="['message', { 'error': isError }]">
          <text>{{ message }}</text>
      </view>
      <view v-if="waterBillData.length" class="data-table">
        <view class="table-header">
          <text class="th">ID</text>
          <text class="th">金额 (RMB)</text>
          <text class="th">月份</text>
        </view>
        <view class="table-body">
          <view v-for="data in waterBillData" :key="data.id" class="table-row">
            <text class="td">{{ data.id }}</text>
            <text class="td">{{ data.amount }}</text>
            <text class="td">{{ data.month }}</text>
          </view>
        </view>
      </view>
      <view v-else-if="!message" class="no-data">
          <text>暂无水费账单数据。</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getWaterBill } from '@/api/index';

export default {
  name: 'WaterBillPage',
  data() {
    return {
      roomNumber: '',
      waterBillData: [],
      message: '',
      isError: false
    };
  },
  onShow() {
    this.loadUserData();
    if (this.roomNumber) {
      this.fetchWaterBillData();
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
    async fetchWaterBillData() {
      this.message = '';
      this.isError = false;
      try {
        const data = await getWaterBill(this.roomNumber);
        this.waterBillData = data;
        if (data.length === 0) {
          this.message = '暂无水费账单数据。请尝试提交一些数据。';
        }
      } catch (error) {
        this.message = `加载水费账单失败: ${error.message}`;
        this.isError = true;
      }
    }
  }
};
</script>

<style scoped>
.water-bill-page {
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
