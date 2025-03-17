import React, { useRef, useEffect } from 'react';
//import * as d3 from 'd3';

const SceneGraph: React.FC = () => {
    const svgRef = useRef<SVGSVGElement>(null);

    useEffect(() => {
        // TODO: 实现D3图形渲染
    }, []);

    return (
        <svg
            ref={svgRef}
            style={{ width: '100%', height: '100%', minHeight: '500px' }}
        />
    );
};

export default SceneGraph;