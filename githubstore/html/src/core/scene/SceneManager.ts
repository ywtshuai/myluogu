/**
 * @file 场景管理器
 * @description 处理场景的加载、更新和状态管理
 */
import type { SceneState } from '../../types/scene';

class SceneManager {
    private currentScene: SceneState | null = null;
    private subscribers: Set<(scene: SceneState | null) => void> = new Set();

    public updateScene(newScene: Partial<SceneState>) {
        const defaultSceneState: SceneState = { ...newScene, id: newScene.id || 'default-id' };
        this.currentScene = this.currentScene
            ? { ...this.currentScene, ...defaultSceneState }
            : defaultSceneState;
        this.notifySubscribers();
    }

    public subscribe(callback: (scene: SceneState | null) => void) {
        this.subscribers.add(callback);
        return () => this.subscribers.delete(callback);
    }

    private notifySubscribers() {
        this.subscribers.forEach(callback => callback(this.currentScene));
    }
}

export const sceneManager = new SceneManager();