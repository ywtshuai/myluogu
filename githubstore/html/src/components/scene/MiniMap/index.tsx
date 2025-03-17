/**
 * @file 小地图组件
 * @description 游戏场景的缩略图显示
 */
import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import { useScene } from '../../../hooks/scene/useScene.ts';
import { neo4jService } from '../../../services/neo4j/neo4jService';
import styles from './styles.module.css';

interface Node {
  id: string;
  name: string;
  group: number;
  x?: number;
  y?: number;
}

interface Link {
  source: string | Node;
  target: string | Node;
  value: number;
}

interface GraphData {
  nodes: Node[];
  links: Link[];
}

const MiniMap: React.FC = () => {
    const svgRef = useRef<SVGSVGElement>(null);
    const { currentScene } = useScene();
    const [graphData, setGraphData] = useState<GraphData | null>(null);

    // 获取场景图数据
    useEffect(() => {
        const fetchGraphData = async () => {
            try {
                const data = await neo4jService.getAllScenes();
                setGraphData(data);
            } catch (err) {
                console.error('获取场景图数据失败:', err);
            }
        };

        fetchGraphData();
    }, []);

    // 渲染小地图
    useEffect(() => {
        if (!graphData || !svgRef.current) return;

        // 清除之前的图形
        d3.select(svgRef.current).selectAll('*').remove();

        const width = 200;
        const height = 200;
        const svg = d3.select(svgRef.current)
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height]);

        // 设置颜色比例尺
        const color = d3.scaleOrdinal(d3.schemeCategory10);

        // 创建力导向图模拟
        const simulation = d3.forceSimulation(graphData.nodes as d3.SimulationNodeDatum[])
            .force("link", d3.forceLink(graphData.links).id((d: any) => d.id))
            .force("charge", d3.forceManyBody().strength(-30))
            .force("center", d3.forceCenter(width / 2, height / 2));

        // 添加连接线
        const link = svg.append("g")
            .selectAll("line")
            .data(graphData.links)
            .join("line")
            .attr("stroke", "#666")
            .attr("stroke-width", 1)
            .attr("stroke-opacity", 0.5);

        // 添加节点
        const node = svg.append("g")
            .selectAll("circle")
            .data(graphData.nodes)
            .join("circle")
            .attr("r", 3)
            .attr("fill", d => {
                // 高亮当前场景
                return d.id === currentScene?.id ? "#ff0" : color(d.group.toString());
            })
            .attr("stroke", "#fff")
            .attr("stroke-width", 0.5);

        // 更新模拟
        simulation.on("tick", () => {
            link
                .attr("x1", d => (d.source as Node).x!)
                .attr("y1", d => (d.source as Node).y!)
                .attr("x2", d => (d.target as Node).x!)
                .attr("y2", d => (d.target as Node).y!);

            node
                .attr("cx", d => d.x!)
                .attr("cy", d => d.y!);
        });

        // 组件卸载时停止模拟
        return () => {
            simulation.stop();
        };
    }, [graphData, currentScene]);

    return (
        <div className={styles.miniMap}>
            <svg ref={svgRef} className={styles.svg} />
        </div>
    );
};

export default MiniMap;