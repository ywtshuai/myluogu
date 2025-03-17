/**
 * @file 聊天面板组件
 * @description 处理AI对话交互
 */
import React, { useState, useRef, useEffect } from 'react';
import { Input, Button, message } from 'antd';
import type { ChatPanelProps } from './types';
import type { ChatMessage } from '../../../types/chat';
import { sendWorldDescription, getWorldStatus } from '../../../services/chatService';
import styles from './styles.module.css';

// 扩展消息类型，添加高亮属性
interface LocalMessage {
    id: string;
    text: string;
    sender: 'user' | 'ai' | 'system';
    timestamp: number;
    isHighlighted?: boolean;
}

// 联合类型，用于处理两种可能的消息类型
type MessageType = LocalMessage | ChatMessage;

const ChatPanel: React.FC<ChatPanelProps> = ({
                                                 messages = [],
                                                 onSendMessage
                                             }) => {
    const [inputValue, setInputValue] = useState('');
    const [localMessages, setLocalMessages] = useState<LocalMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Add initial message when component mounts
    useEffect(() => {
        // Only add the initial message if there are no messages yet
        if (localMessages.length === 0) {
            setLocalMessages([
                {
                    id: 'initial-message',
                    text: 'Describe your World',
                    sender: 'system',
                    timestamp: Date.now(),
                    isHighlighted: true
                }
            ]);
        }
    }, []);

    const handleSend = async () => {
        if (inputValue.trim() && !isLoading) {
            setIsLoading(true);

            // Add user message
            const userMessage: LocalMessage = {
                id: `user-${Date.now()}`,
                text: inputValue,
                sender: 'user',
                timestamp: Date.now()
            };

            // Add "Your World is being created......" message
            const creatingWorldMessage: LocalMessage = {
                id: `ai-${Date.now() + 1}`,
                text: 'Your World is being created......',
                sender: 'system',
                timestamp: Date.now() + 1,
                isHighlighted: true
            };

            setLocalMessages(prev => [...prev, userMessage, creatingWorldMessage]);

            try {
                // 发送世界描述到后端
                const response = await sendWorldDescription(inputValue);

                if (response.success && response.worldId) {
                    // 如果发送成功且返回了 worldId，开始轮询世界创建状态
                    const statusResponse = await getWorldStatus(response.worldId);

                    // 如果世界创建成功，更新消息
                    if (statusResponse.success) {
                        message.success('世界描述已发送成功！');
                    } else {
                        message.error(statusResponse.message || '获取世界状态失败');
                    }
                } else {
                    // 发送失败
                    message.error(response.message || '发送失败');
                }
            } catch (error) {
                console.error('发送世界描述时出错:', error);
                message.error('发送失败，请稍后重试');
            } finally {
                setIsLoading(false);
            }

            // 清空输入框
            setInputValue('');

            // 如果提供了 onSendMessage 回调，调用它
            if (onSendMessage) {
                onSendMessage(inputValue);
            }
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [localMessages, messages]);

    // Combine local messages with props messages if provided
    const displayMessages = localMessages.length > 0 ? localMessages : messages;

    // Function to get the appropriate message class
    const getMessageClass = (msg: MessageType) => {
        let className = styles.message;

        if (msg.sender === 'user') {
            className += ` ${styles.userMessage}`;
        } else if (msg.sender === 'ai') {
            className += ` ${styles.aiMessage}`;
        } else if (msg.sender === 'system') {
            className += ` ${styles.systemMessage}`;
        }

        // 检查是否有 isHighlighted 属性
        if ('isHighlighted' in msg && msg.isHighlighted) {
            className += ` ${styles.highlightedMessage}`;
        }

        return className;
    };

    return (
        <div className={styles.chatPanel}>
            <div className={styles.header}>
                <h2>AI Chat Room</h2>
            </div>
            <div className={styles.messageArea}>
                {displayMessages.map((msg) => (
                    <div
                        key={msg.id}
                        className={getMessageClass(msg)}
                    >
                        {msg.text}
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            <div className={styles.inputArea}>
                <Input.TextArea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onPressEnter={(e) => {
                        if (!e.shiftKey) {
                            e.preventDefault();
                            handleSend();
                        }
                    }}
                    placeholder="Type your message..."
                    autoSize={{ minRows: 2, maxRows: 4 }}
                    disabled={isLoading}
                />
                <Button
                    type="primary"
                    onClick={handleSend}
                    loading={isLoading}
                >
                    Send
                </Button>
            </div>
        </div>
    );
};
export default ChatPanel;