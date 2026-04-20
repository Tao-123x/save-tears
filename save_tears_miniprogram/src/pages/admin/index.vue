<template>
  <EditorialPage tone="deep" compact>
    <view class="admin-page">
      <view class="admin-page__header st-panel-raise">
        <text class="st-kicker">Admin</text>
        <text class="st-display admin-page__headline">Admin</text>
      </view>

      <view v-if="loading" class="admin-page__loading st-panel-raise">正在整理住户列表...</view>
      <EditorialEmptyState
        v-else-if="errorMessage"
        title="管理员数据暂时不可用"
        :message="errorMessage"
        action-text="重新加载"
        @action="loadAdminDesk"
      />

      <template v-else>
        <view class="admin-page__stats">
          <AdminStatCard label="Residents" :value="String(overview.totalUsers)" />
          <AdminStatCard label="Flags" :value="String(overview.roomsMissing.length)" />
          <AdminStatCard label="Active" :value="activeRate" />
        </view>

        <view class="admin-search st-panel-raise">
          <view class="admin-search__topline"></view>
          <input
            v-model="searchText"
            class="admin-search__field"
            type="text"
            placeholder="Search room or user"
            placeholder-class="admin-search__placeholder"
          />
          <view class="admin-search__dot"></view>
        </view>

        <view class="admin-list st-panel-raise">
          <view class="admin-list__topline"></view>
          <text class="admin-list__title">Resident list</text>

          <EditorialEmptyState
            v-if="!filteredUsers.length"
            title="没有匹配的住户"
            message="换一个用户名或房间号关键词试试。"
          />

          <template v-else>
            <view v-for="user in filteredUsers" :key="`${user.username}-${user.room_number || 'none'}`" class="admin-list__row">
              <view class="admin-list__identity">
                <view class="admin-list__avatar">{{ user.username.slice(0, 1).toUpperCase() }}</view>
                <view class="admin-list__copy">
                  <text class="admin-list__name">{{ user.username }}</text>
                </view>
              </view>
              <view class="admin-list__tag" :class="tagClass(user)">
                {{ tagText(user) }}
              </view>
            </view>
          </template>
        </view>

        <view class="admin-note st-panel-raise">
          <view class="admin-note__topline"></view>
          <text class="admin-note__title">Watchlist</text>
          <text class="admin-note__copy">
            {{ overview.roomsMissing.length ? `缺失房间号：${overview.roomsMissing.join('、')}` : '当前没有缺失房间号的账号。' }}
          </text>
        </view>
      </template>
    </view>
  </EditorialPage>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { onShow } from '@dcloudio/uni-app';

import AdminStatCard from '@/components/AdminStatCard.vue';
import EditorialEmptyState from '@/components/EditorialEmptyState.vue';
import EditorialPage from '@/components/EditorialPage.vue';
import { getUsers, type UserRecord } from '@/api/index';
import { buildAdminOverview } from '@/utils/insights';
import { getStoredUser, isAdminUser } from '@/utils/session';

const loading = ref(false);
const errorMessage = ref('');
const searchText = ref('');
const users = ref<UserRecord[]>([]);

const filteredUsers = computed(() => {
  const keyword = searchText.value.trim().toLowerCase();
  const sorted = [...users.value].sort((left, right) => {
    if (isAdminRole(left.role) && !isAdminRole(right.role)) return -1;
    if (!isAdminRole(left.role) && isAdminRole(right.role)) return 1;
    return left.username.localeCompare(right.username);
  });

  if (!keyword) {
    return sorted;
  }

  return sorted.filter((user) => {
    return (
      user.username.toLowerCase().includes(keyword) ||
      String(user.room_number || '').toLowerCase().includes(keyword)
    );
  });
});

const overview = computed(() => buildAdminOverview(users.value));
const activeRate = computed(() => {
  if (!overview.value.totalUsers) {
    return '0%';
  }

  return `${Math.round((overview.value.roomsConfigured / overview.value.totalUsers) * 100)}%`;
});

onShow(() => {
  const user = getStoredUser();
  if (!isAdminUser(user)) {
    uni.showToast({ title: '普通住户无法查看管理员页', icon: 'none' });
    setTimeout(() => {
      uni.switchTab({ url: '/pages/home/index' });
    }, 120);
    return;
  }

  void loadAdminDesk();
});

async function loadAdminDesk() {
  loading.value = true;
  errorMessage.value = '';

  try {
    const data = await getUsers();
    users.value = data.map((user) => ({
      username: user.username,
      room_number: user.room_number,
      role: user.role,
    }));
  } catch (error: any) {
    errorMessage.value = error?.message || '用户列表加载失败，请检查后端服务。';
  } finally {
    loading.value = false;
  }
}

function isAdminRole(role?: string | null) {
  return String(role || '').toLowerCase() === 'admin';
}

function tagText(user: UserRecord) {
  if (isAdminRole(user.role)) return 'Admin';
  if (!String(user.room_number || '').trim()) return 'Flagged';
  return `Room ${user.room_number}`;
}

function tagClass(user: UserRecord) {
  return {
    'admin-list__tag--admin': isAdminRole(user.role),
    'admin-list__tag--flagged': !isAdminRole(user.role) && !String(user.room_number || '').trim(),
  };
}
</script>

<style scoped>
.admin-page__header {
  padding: 16rpx 6rpx 24rpx;
}

.admin-page__headline {
  margin-top: 10rpx;
}

.admin-page__subline {
  margin-top: 14rpx;
}

.admin-page__loading,
.admin-search,
.admin-list,
.admin-note {
  position: relative;
  margin-top: 18rpx;
  padding: 24rpx;
  border-radius: var(--st-radius-xl);
  background: rgba(255, 255, 255, 0.94);
  border: 1rpx solid var(--st-line);
  box-shadow: var(--st-shadow-tight);
  overflow: hidden;
}

.admin-page__loading {
  font-size: 26rpx;
  color: var(--st-text-soft);
}

.admin-page__stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14rpx;
}

.admin-search__topline,
.admin-list__topline,
.admin-note__topline {
  position: absolute;
  left: 18rpx;
  right: 18rpx;
  top: 12rpx;
  height: 1rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.84);
}

.admin-search__field {
  width: 100%;
  min-height: 92rpx;
  padding: 0 58rpx 0 24rpx;
  border-radius: 22rpx;
  border: 1rpx solid var(--st-line);
  background: rgba(247, 251, 255, 0.96);
  color: var(--st-text);
  font-size: 28rpx;
}

.admin-search__placeholder {
  color: var(--st-text-muted);
}

.admin-search__dot {
  position: absolute;
  right: 40rpx;
  top: 50%;
  width: 18rpx;
  height: 18rpx;
  border-radius: 50%;
  background: rgba(47, 140, 255, 0.2);
  box-shadow: 0 0 14rpx rgba(47, 140, 255, 0.2);
  transform: translateY(-50%);
}

.admin-list__title,
.admin-note__title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: var(--st-text);
}

.admin-list__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
  padding: 20rpx 0;
  border-bottom: 1rpx solid rgba(215, 232, 245, 0.72);
}

.admin-list__row:first-of-type {
  margin-top: 14rpx;
}

.admin-list__row:last-child {
  border-bottom: 0;
}

.admin-list__identity {
  display: flex;
  align-items: center;
  gap: 14rpx;
  min-width: 0;
}

.admin-list__avatar {
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, rgba(215, 238, 255, 1) 0%, rgba(196, 228, 255, 1) 100%);
  color: var(--st-accent-deep);
  font-size: 24rpx;
  font-weight: 700;
}

.admin-list__copy {
  min-width: 0;
}

.admin-list__name {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: var(--st-text);
}

.admin-list__meta,
.admin-note__copy {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  line-height: 1.5;
  color: var(--st-text-soft);
}

.admin-list__tag {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52rpx;
  padding: 0 18rpx;
  border-radius: 999rpx;
  background: #e9fbf5;
  color: var(--st-success);
  font-size: 22rpx;
  font-weight: 600;
}

.admin-list__tag--admin {
  background: #eef6ff;
  color: var(--st-accent-deep);
}

.admin-list__tag--flagged {
  background: #fff5e9;
  color: var(--st-warning);
}

.admin-note__copy {
  margin-top: 10rpx;
}
</style>
