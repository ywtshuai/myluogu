/**
 * @file 聊天服务
 * @description 处理与后端的聊天相关接口
 */

import axios, { AxiosError } from 'axios';

// API 响应类型定义
interface WorldDescriptionResponse {
    success: boolean;
    message: string;
    worldId?: string;
    error?: string;
}

// 创建 axios 实例，设置基础配置
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000', // 从环境变量获取 API 地址
    timeout: 15000, // 15 秒超时
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * 发送世界描述到后端
 * @param description 用户输入的世界描述文本
 * @returns 后端响应数据
 */
export const sendWorldDescription = async (description: string): Promise<WorldDescriptionResponse> => {
    try {
        const response = await api.post<WorldDescriptionResponse>('/api/world/create', {
            description,
            timestamp: Date.now(),
        });

        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            const axiosError = error as AxiosError<{ message: string; error: string }>;
            if (axiosError.response?.data) {
                // 返回后端的错误信息
                return {
                    success: false,
                    message: axiosError.response.data.message || '发送失败',
                    error: axiosError.response.data.error,
                };
            }
        }

        // 网络错误或其他错误
        return {
            success: false,
            message: '网络错误，请稍后重试',
            error: error instanceof Error ? error.message : '未知错误',
        };
    }
};

/**
 * 获取世界创建状态
 * @param worldId 世界ID
 * @returns 世界创建状态
 */
export const getWorldStatus = async (worldId: string): Promise<WorldDescriptionResponse> => {
    try {
        const response = await api.get<WorldDescriptionResponse>(`/api/world/status/${worldId}`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            const axiosError = error as AxiosError<{ message: string; error: string }>;
            if (axiosError.response?.data) {
                return {
                    success: false,
                    message: axiosError.response.data.message || '获取状态失败',
                    error: axiosError.response.data.error,
                };
            }
        }

        return {
            success: false,
            message: '网络错误，请稍后重试',
            error: error instanceof Error ? error.message : '未知错误',
        };
    }
};