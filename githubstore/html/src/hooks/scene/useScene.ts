/**
 * @file 场景管理Hook
 * @description 处理场景状态和更新
 */
import { useState, useCallback } from 'react';
import type { SceneState } from '../../types/scene';

export const useScene = () => {
    const [currentScene, setCurrentScene] = useState<SceneState | null>(null);

    const updateScene = useCallback((newScene: Partial<SceneState>) => {
        setCurrentScene(prev => prev ? { ...prev, ...newScene } : null);
    }, []);

    return {
        currentScene,
        updateScene
    };
};