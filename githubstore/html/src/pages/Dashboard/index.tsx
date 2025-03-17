/**
 * @file 主面板页面
 * @description 整合所有游戏组件的主页面
 */
import React, { useEffect } from 'react';
import { Spin } from 'antd';
import GameLayout from '../../components/common/Layout';
//import { useChat } from '../../hooks/useChat';
//import { useScene } from '../../hooks/useScene';
import { gameLoop } from '../../core/engine/GameLoop';
import type { DashboardProps } from './types';
import styles from './styles.module.css';

const Dashboard: React.FC<DashboardProps> = ({ isLoading = false }) => {
    //const { messages, sendMessage } = useChat();
    //const { currentScene, updateScene } = useScene();

    // 初始化游戏循环
    useEffect(() => {
        gameLoop.start();

        return () => {
            gameLoop.stop();
        };
    }, [isLoading]);

    if (isLoading) {
        return (
            <div className={styles.loadingContainer}>
                <Spin size="large" tip="Loading game world..." />
            </div>
        );
    }

    return <GameLayout />;
};

export default Dashboard;