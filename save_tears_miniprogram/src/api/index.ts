import { getStoredUser } from '@/utils/session';
import { encodeRoomPath, resolveApiBaseUrl } from '@/utils/api-base';

export interface LoginResponse {
    msg: string;
    username: string;
    room_number: string;
    role: string;
    token: string;
}

export interface UserRecord {
    username: string;
    room_number?: string;
    role?: string;
    id?: number;
}

export type GreywaterUsageType = 'toilet_flush' | 'cleaning' | 'other';
export type GreywaterSource = 'device' | 'manual' | 'mock';
export type DeviceStatus = 'online' | 'offline' | 'warning';
export type SavingPlanStatus = 'active' | 'archived';

export interface GreywaterUsageRecord {
    id?: number;
    room_number?: string;
    device_id?: string;
    usage_type: GreywaterUsageType;
    event_count: number;
    volume_liters: number;
    source: GreywaterSource;
    timestamp: string;
    raw_payload_json?: string | null;
}

export interface GreywaterQualityRecord {
    id?: number;
    room_number?: string;
    device_id?: string;
    ph_value?: number | null;
    turbidity_value?: number | null;
    source: GreywaterSource;
    timestamp: string;
    raw_payload_json?: string | null;
}

export interface SavingTrendPoint {
    label: string;
    tap_water_liters: number;
    greywater_liters: number;
    replacement_rate: number;
}

export interface SavingStats {
    room_number?: string;
    tap_water_liters: number;
    greywater_liters: number;
    estimated_savings_liters: number;
    replacement_rate: number;
    flush_count: number;
    trends?: SavingTrendPoint[];
}

export interface SavingPlan {
    id?: number;
    room_number?: string;
    period_start?: string;
    period_end?: string;
    plan_text: string;
    target_flush_count: number;
    target_replacement_rate: number;
    estimated_savings_liters: number;
    model_name: string;
    created_at?: string;
    status?: SavingPlanStatus | string;
}

export interface Device {
    id?: number;
    device_id: string;
    room_number?: string;
    device_type?: string;
    status: DeviceStatus | string;
    last_seen_at?: string;
    source_platform?: string;
    metadata_json?: string;
}

function unwrapApiData<T>(response: T | { data: T }): T {
    if (response && typeof response === 'object' && 'data' in response) {
        return (response as { data: T }).data;
    }
    return response as T;
}

function getBaseUrl() {
    const customBaseUrl = uni.getStorageSync('api_base_url');
    const browserLocation = typeof window !== 'undefined' ? window.location : undefined;
    const envBaseUrl = typeof import.meta !== 'undefined' ? import.meta.env?.VITE_API_BASE_URL : '';

    return resolveApiBaseUrl({
        customBaseUrl,
        envBaseUrl,
        browserProtocol: browserLocation?.protocol,
        browserHostname: browserLocation?.hostname,
    });
}

// 辅助函数：处理 API 请求 (适配微信小程序 uni.request)
function callApi(endpoint: string, method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET', data: any = null): Promise<any> {
    return new Promise((resolve, reject) => {
        const options: UniApp.RequestOptions = {
            url: `${getBaseUrl()}${endpoint}`,
            method: method,
            header: {
                'Content-Type': 'application/json',
            },
            success: (response) => {
                if (response.statusCode >= 200 && response.statusCode < 300) {
                    resolve(response.data);
                } else {
                    const error = new Error((response.data as any)?.detail || '请求失败，请稍后再试');
                    (error as any).statusCode = response.statusCode;
                    reject(error);
                }
            },
            fail: (error) => {
                console.error(`Error calling ${endpoint}:`, error);
                const err = new Error(error.errMsg || '网络请求失败');
                reject(err);
            }
        };

        const currentUser = getStoredUser();
        if (currentUser?.token) {
            options.header = {
                ...options.header,
                Authorization: `Bearer ${currentUser.token}`,
            };
        }

        if (data) {
            options.data = data;
        }

        uni.request(options);
    });
}

// ==================== 用户认证 API ====================

/**
 * 注册用户
 */
export const registerUser = (username: string, password: string, roomNumber: string) => {
    return callApi('/register', 'POST', { username, password, room_number: roomNumber });
};

/**
 * 登录用户
 */
export const loginUser = (username: string, password: string) => {
    return callApi('/login', 'POST', { username, password }) as Promise<LoginResponse>;
};

// ==================== 水流量数据 API ====================

/**
 * 提交水流量数据
 */
export const submitWaterFlow = (roomNumber: string, flowRate: number, timestamp: string) => {
    return callApi('/water_flow', 'POST', { room_number: roomNumber, flow_rate: flowRate, timestamp: timestamp });
};

/**
 * 获取某个房间的水流量数据
 */
export const getWaterFlow = (roomNumber: string) => {
    return callApi(`/water_flow/${encodeRoomPath(roomNumber)}`) as Promise<Array<{
        id?: number;
        room_number?: string;
        flow_rate: number;
        timestamp: string;
    }>>;
};

// ==================== 污水浊度数据 API ====================

/**
 * 提交污水浊度数据
 */
export const submitSewageTurbidity = (roomNumber: string, turbidityValue: number, timestamp: string) => {
    return callApi('/sewage_turbidity', 'POST', { room_number: roomNumber, turbidity_value: turbidityValue, timestamp: timestamp });
};

/**
 * 获取某个房间的污水浊度数据
 */
export const getSewageTurbidity = (roomNumber: string) => {
    return callApi(`/sewage_turbidity/${encodeRoomPath(roomNumber)}`) as Promise<Array<{
        id?: number;
        room_number?: string;
        turbidity_value: number;
        timestamp: string;
    }>>;
};

// ==================== 水费数据 API ====================

/**
 * 提交水费数据
 */
export const submitWaterBill = (roomNumber: string, amount: number, month: string) => {
    return callApi('/water_bill', 'POST', { room_number: roomNumber, amount: amount, month: month });
};

/**
 * 获取某个房间的水费数据
 */
export const getWaterBill = (roomNumber: string) => {
    return callApi(`/water_bill/${encodeRoomPath(roomNumber)}`) as Promise<Array<{
        id?: number;
        room_number?: string;
        amount: number;
        month: string;
    }>>;
};

// ==================== 灰水节水 API ====================

/**
 * 获取某个房间的灰水使用记录
 */
export const getGreywaterUsage = (roomNumber: string) => {
    return callApi(`/greywater_usage/${encodeRoomPath(roomNumber)}`) as Promise<GreywaterUsageRecord[]>;
};

/**
 * 获取某个房间的灰水 pH 和浊度记录
 */
export const getGreywaterQuality = (roomNumber: string) => {
    return callApi(`/greywater_quality/${encodeRoomPath(roomNumber)}`) as Promise<GreywaterQualityRecord[]>;
};

/**
 * 获取某个房间的节水统计
 */
export const getSavingStats = (roomNumber: string) => {
    return callApi(`/saving_stats/${encodeRoomPath(roomNumber)}`) as Promise<SavingStats>;
};

/**
 * 生成并保存某个房间的节水计划
 */
export const generateSavingPlan = (roomNumber: string) => {
    return callApi(`/saving_plans/${encodeRoomPath(roomNumber)}/generate`, 'POST').then(unwrapApiData<SavingPlan>);
};

/**
 * 获取某个房间最新的节水计划
 */
export const getLatestSavingPlan = (roomNumber: string) => {
    return callApi(`/saving_plans/${encodeRoomPath(roomNumber)}/latest`).then(unwrapApiData<SavingPlan>);
};

/**
 * 获取灰水设备列表，供管理员页面使用
 */
export const getDevices = () => {
    return callApi('/devices') as Promise<Device[]>;
};

// ==================== 其他 API ====================

/**
 * 获取所有用户列表 (仅供管理员或测试使用)
 */
export const getUsers = () => {
    return callApi('/users') as Promise<UserRecord[]>;
};

export const setApiBaseUrl = (baseUrl: string) => {
    uni.setStorageSync('api_base_url', baseUrl);
};

export const getStoredApiBaseUrl = () => {
    return uni.getStorageSync('api_base_url') || '';
};

export const getResolvedApiBaseUrl = () => {
    return getBaseUrl();
};
