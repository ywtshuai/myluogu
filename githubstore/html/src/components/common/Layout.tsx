/**
 * @file 游戏主布局组件
 * @description 负责整体页面布局，包括聊天面板、游戏场景和玩家视图
 */
import React, { useState } from 'react';
import { Layout } from 'antd';
import ChatPanel from '../chat/ChatPanel';
import GameScene from '../scene/GameScene';
import MiniMap from '../scene/MiniMap';
import PlayerView from '../player/PlayerView';
import styles from './styles.module.css';
import type { ChatMessage } from '../../types/chat';

const { Sider, Content } = Layout;

// No props needed for now
const GameLayout: React.FC = () => {
    // We're keeping setMessages for future implementation
    //const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [messages] = useState<ChatMessage[]>([]);

    const handleSendMessage = (message: string) => {
        // Here you would typically send the message to your backend
        console.log('Message sent:', message);

        // You can add additional logic here if needed
        // For example, processing the world description
    };

    return (
        <Layout className={styles.gameLayout}>
            <Sider width="33%" className={styles.sider}>
                <ChatPanel
                    messages={messages}
                    onSendMessage={handleSendMessage}
                />
            </Sider>
            <Content className={styles.content}>
                <div className={styles.upperSection}>
                    <GameScene />
                    <div className={styles.miniMapWrapper}>
                        <MiniMap />
                    </div>
                </div>
                <div className={styles.lowerSection}>
                    <PlayerView />
                </div>
            </Content>
        </Layout>
    );
};
export default GameLayout;