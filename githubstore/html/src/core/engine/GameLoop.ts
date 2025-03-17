/**
 * @file 游戏循环
 * @description 处理游戏主循环和时间管理
 */

class GameLoop {
    private isRunning: boolean = false;
    private lastTime: number = 0;
    private callbacks: Array<(deltaTime: number) => void> = [];
    private animationFrameId: number | null = null;

    // 开始游戏循环
    public start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.lastTime = performance.now();
        this.animationFrameId = requestAnimationFrame(this.tick);
    }

    // 停止游戏循环
    public stop() {
        this.isRunning = false;
        if (this.animationFrameId !== null) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }

    // 添加回调函数
    public addCallback(callback: (deltaTime: number) => void) {
        this.callbacks.push(callback);
        return () => {
            const index = this.callbacks.indexOf(callback);
            if (index !== -1) this.callbacks.splice(index, 1);
        };
    }

    // 内部方法：处理每一帧的循环逻辑
    private tick = () => {
        if (!this.isRunning) return;

        const currentTime = performance.now();
        const deltaTime = (currentTime - this.lastTime) / 1000;
        this.lastTime = currentTime;

        this.callbacks.forEach(callback => callback(deltaTime));

        this.animationFrameId = requestAnimationFrame(this.tick);
    };
}

export const gameLoop = new GameLoop();