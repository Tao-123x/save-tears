import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'
const userInfo = createApp({
    data() {
        return {
            //用户信息
            userInfo:
            {
                'name': '张三',
                'email': 'zhangsan@example.com',
                'level': 2,
                "totalWaterInMonth": 12.4,      //月总用水量
                "averageWater": 0.41,           //平均每日用水量
                "points": 96,                   //本月积分
                //近期活动
                recentActivities: [
                    { 'date': '2025-05-15', 'action': '登录系统' },
                    { 'date': '2025-05-10', 'action': '缴费成功 $45.80' },
                    { 'date': '2025-05-08', 'action': '浏览用水页面' },
                ],

                //支付信息
                paidInfo: [
                    { 'date': '2025-04-12', 'amount': 45.80, "ifPaid": false },
                    { 'date': '2025-05-09', 'amount': 48.00, "ifPaid": false },
                    { 'date': '2025-03-21', 'amount': 49.00, "ifPaid": true },
                    { 'date': '2025-04-24', 'amount': 52.00, "ifPaid": true },
                    { 'date': '2025-05-02', 'amount': 55.00, "ifPaid": true },
                    { 'date': '2025-05-15', 'amount': 58.00, "ifPaid": true },
                    { 'date': '2025-03-28', 'amount': 60.00, "ifPaid": false },
                ],
            },
        }
    },

    computed: {
        // 计算属性：返回按日期排序的支付信息
        sortedPaidInfo() {
            // 复制数组避免修改原始数据
            return [...this.userInfo.paidInfo].sort((a, b) => {
                // 将日期字符串转换为Date对象进行比较
                return new Date(b.date) - new Date(a.date);
            });
        }
    },

    methods: {

    }
})
export default userInfo
userInfo.mount('#userAccount')