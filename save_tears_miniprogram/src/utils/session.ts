export type UserRole = 'admin' | 'user';

export interface StoredUser {
  username?: string;
  room_number?: string;
  role?: string | null;
  token?: string;
}

const STORAGE_KEY = 'user';

export function normalizeUserRole(role?: string | null): UserRole {
  return String(role || '').trim().toLowerCase() === 'admin' ? 'admin' : 'user';
}

export function parseStoredUser(raw?: string | null): StoredUser | null {
  if (!raw) {
    return null;
  }

  try {
    const parsed = JSON.parse(raw) as StoredUser;
    if (!String(parsed?.token || '').trim()) {
      return null;
    }
    return {
      ...parsed,
      role: normalizeUserRole(parsed?.role),
      token: String(parsed?.token || '').trim(),
    };
  } catch (error) {
    return null;
  }
}

export function getStoredUser(): StoredUser | null {
  if (typeof uni === 'undefined') {
    return null;
  }

  return parseStoredUser(uni.getStorageSync(STORAGE_KEY));
}

export function saveStoredUser(user: StoredUser) {
  if (typeof uni === 'undefined') {
    return;
  }

  uni.setStorageSync(
    STORAGE_KEY,
    JSON.stringify({
      ...user,
      role: normalizeUserRole(user?.role),
      token: String(user?.token || '').trim(),
    }),
  );
}

export function clearStoredUser() {
  if (typeof uni === 'undefined') {
    return;
  }

  uni.removeStorageSync(STORAGE_KEY);
}

export function isAdminUser(user?: StoredUser | null) {
  return normalizeUserRole(user?.role) === 'admin';
}
