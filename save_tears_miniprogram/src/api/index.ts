// 定义后端 API 的基础 URL
const BASE_URL = 'http://127.0.0.1:8000';

// 辅助函数：处理 API 请求 (适配微信小程序 uni.request)
function callApi(endpoint: string, method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET', data: any = null): Promise<any> {
    return new Promise((resolve, reject) => {
        const options: UniApp.RequestOptions = {
            url: `${BASE_URL}${endpoint}`,
            method: method,
            header: {
                'Content-Type': 'application/json',
            },
            success: (response) => {
                if (response.statusCode >= 200 && response.statusCode < 300) {
                    resolve(response.data);
                } else {
                    const error = new Error((response.data as any)?.detail || 'API 请求失败');
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
    return callApi('/login', 'POST', { username, password });
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
    return callApi(`/water_flow/${roomNumber}`);
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
    return callApi(`/sewage_turbidity/${roomNumber}`);
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
    return callApi(`/water_bill/${roomNumber}`);
};

// ==================== 其他 API ====================

/**
 * 获取所有用户列表 (仅供管理员或测试使用)
 */
export const getUsers = () => {
    return callApi('/users');
};
