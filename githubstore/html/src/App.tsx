/**
 * @file 应用程序入口
 * @description 配置主题、路由和全局状态
 */
import React, { useState, useEffect } from 'react';
import { ConfigProvider, theme } from 'antd';
import { Dashboard } from './pages';
import { sceneManager } from './core/scene/SceneManager';
import { neo4jService } from './services/neo4j/neo4jService';
import { initializeSceneGraph } from './services/neo4j/sceneGraphData';
import styles from './App.module.css';

const App: React.FC = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // 初始化应用
    useEffect(() => {
        const initializeApp = async () => {
            try {
                // TODO: 加载必要的资源和配置
                // 连接 Neo4j 数据库
                await neo4jService.connect(
                    'neo4j://1.12.255.121:7687', // Neo4j 数据库地址
                    'neo4j',                  // 用户名
                    'password'            // 密码
                );
                
                // 初始化场景图数据
                await initializeSceneGraph();
                setIsLoading(false);    
            } catch(error) {
                console.error('Failed to initialize app:', error);
                // TODO: 错误处理
            }
        };

        initializeApp();

        // 订阅场景更新
        const unsubscribe = sceneManager.subscribe((scene) => {
            console.log('Scene updated:', scene);
        });

        return () => {
            unsubscribe();
            // 关闭 Neo4j 数据库连接
            neo4jService.close().catch(err => {
                console.error('Close Neo4j:', err);
            });
        };
    }, []);

    // 如果有错误，显示错误信息
    if (error) {
        return (
            <ConfigProvider
                theme={{
                    algorithm: theme.darkAlgorithm,
                    token: {
                        colorPrimary: '#1890ff',
                        colorBgBase: '#1f1f1f',
                        colorTextBase: '#ffffff',
                    },
                }}
            >
                <div className={styles.app}>
                    <div className={styles.error}>
                        <h2>初始化失败</h2>
                        <p>{error}</p>
                        <p>您可以暂时跳过数据库连接，继续使用应用</p>
                        <button onClick={() => setError(null)}>继续使用应用</button>
                    </div>
                </div>
            </ConfigProvider>
        );
    }

    return (
        <ConfigProvider
            theme={{
                algorithm: theme.darkAlgorithm,
                token: {
                    colorPrimary: '#1890ff',
                    colorBgBase: '#1f1f1f',
                    colorTextBase: '#ffffff',
                },
            }}
        >
            <div className={styles.app}>
                <Dashboard isLoading={isLoading} />
            </div>
        </ConfigProvider>
    );
};

export default App;