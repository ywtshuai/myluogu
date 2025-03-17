/**
 * @file 聊天功能Hook
 * @description 处理聊天相关的状态和逻辑
 */
import { useState, useCallback } from 'react';
import type { ChatMessage } from '../../types/chat';

export const useChat = () => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);

    const sendMessage = useCallback((text: string) => {
        // TODO: 实现发送消息逻辑
        const newMessage: ChatMessage = {
            id: Date.now().toString(),
            text,
            sender: 'user',
            timestamp: Date.now()
        };
        setMessages(prev => [...prev, newMessage]);
    }, []);

    return {
        messages,
        sendMessage
    };
};