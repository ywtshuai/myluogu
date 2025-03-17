/**
 * @file 游戏diffusion渲染的图片
 * @description 游戏场景的图片示意
 */
import React, { useEffect, useRef } from 'react';
import { useScene } from '../../../hooks/scene/useScene'; // 假设有一个场景 hook

const GameScene: React.FC = () => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null);
    const { currentScene } = useScene();

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;

        const render = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 临时绘制一些内容以展示场景区域
            ctx.fillStyle = '#2a2a2a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#3a3a3a';
            ctx.fillRect(50, 50, canvas.width - 100, canvas.height - 100);

            animationFrameId = requestAnimationFrame(render);
        };

        render();

        // 清理函数，在组件卸载时取消动画帧请求
        return () => {
            cancelAnimationFrame(animationFrameId);
        };
    }, [currentScene]);

    return <canvas ref={canvasRef} width={800} height={600}></canvas>;
};

export default GameScene;