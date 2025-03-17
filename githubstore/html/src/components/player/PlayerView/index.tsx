/**
 * @file 玩家视图组件
 * @description 显示玩家当前视角
 */
import React, { useRef, useEffect } from 'react';
import styles from './styles.module.css';

const PlayerView: React.FC = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        if (!canvasRef.current) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // TODO: 实现玩家视角渲染
        const render = () => {
            if (!ctx) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 临时绘制内容以展示玩家视角区域
            ctx.fillStyle = '#1a1a1a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#2a2a2a';
            ctx.fillRect(100, 100, canvas.width - 200, canvas.height - 200);
        };

        render();
    }, []);

    return (
        <div className={styles.playerView}>
            <canvas
                ref={canvasRef}
                className={styles.canvas}
                width={800}
                height={600}
            />
        </div>
    );
};

export default PlayerView;