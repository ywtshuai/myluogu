export interface SceneNode {
    id: string;
    position: {
        x: number;
        y: number;
    };
    type: string;
}

export interface SceneEdge {
    id: string;
    source: string;
    target: string;
}

export interface SceneState {
    //TODO: 实现
    id: string
}