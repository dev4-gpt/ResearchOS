import React, { useState, useEffect, useRef } from 'react';
import { Network, Loader, X } from 'lucide-react';
import { apiFetch } from '../api';

interface GraphNode {
  id: string;
  title: string;
  category: string;
  tags: string[];
  metadata: any;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
}

interface GraphEdge {
  source: string;
  target: string;
  type: string;
}

interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

const CATEGORY_META: Record<string, { color: string; label: string }> = {
  papers: { color: '#10b981', label: 'Paper Summaries' },     // Emerald
  concepts: { color: '#f59e0b', label: 'Concept Cards' },    // Amber
  debates: { color: '#8b5cf6', label: 'Debate Transcript' }, // Violet
  drafts: { color: '#f43f5e', label: 'Manuscript Drafts' }   // Rose
};

function hashStringToFloat(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return (Math.abs(hash) % 1000) / 1000;
}

const GraphView: React.FC = () => {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [nodeContent, setNodeContent] = useState<{ frontmatter: any; content: string } | null>(null);
  const [isLoadingContent, setIsLoadingContent] = useState(false);
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const svgRef = useRef<SVGSVGElement>(null);
  const simulationRef = useRef<number | null>(null);
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [draggedNode, setDraggedNode] = useState<GraphNode | null>(null);

  // Fetch graph data from backend
  useEffect(() => {
    fetchGraph();
    return () => {
      if (simulationRef.current) cancelAnimationFrame(simulationRef.current);
    };
  }, []);

  const fetchGraph = async () => {
    setIsLoading(true);
    try {
      const res = await apiFetch('/api/vault/graph');
      if (res.ok) {
        const data: GraphData = await res.json();
        setGraphData(data);
        
        // Initialize node positions deterministically based on node id hash
        const width = 600;
        const height = 400;
        const initializedNodes = data.nodes.map(n => {
          const hX = hashStringToFloat(n.id);
          const hY = hashStringToFloat(n.id + '_y');
          return {
            ...n,
            x: width / 2 + (hX - 0.5) * 300,
            y: height / 2 + (hY - 0.5) * 200,
            vx: 0,
            vy: 0
          };
        });
        setNodes(initializedNodes);
      }
    } catch (e) {
      console.error('Failed to fetch knowledge graph:', e);
    } finally {
      setIsLoading(false);
    }
  };

  // Simple Physics Force-Directed Simulation Loop
  useEffect(() => {
    if (nodes.length === 0 || !graphData) return;

    const width = 800;
    const height = 500;
    const centerX = width / 2;
    const centerY = height / 2;
    
    const runSimulation = () => {
      // Create a copy of nodes to mutate velocities and coordinates
      const nextNodes = nodes.map(n => ({ ...n }));
      
      const nodeMap = new Map(nextNodes.map(n => [n.id, n]));
      
      // Constants for forces
      const repulsionConstant = 600;
      const attractionConstant = 0.04;
      const centerForceConstant = 0.015;
      const damping = 0.85;

      // 1. Repulsion between all node pairs (Coulomb's Law)
      for (let i = 0; i < nextNodes.length; i++) {
        const nodeA = nextNodes[i];
        for (let j = i + 1; j < nextNodes.length; j++) {
          const nodeB = nextNodes[j];
          
          const dx = (nodeB.x || 0) - (nodeA.x || 0);
          const dy = (nodeB.y || 0) - (nodeA.y || 0);
          const distanceSq = dx * dx + dy * dy || 1;
          const distance = Math.sqrt(distanceSq);
          
          if (distance < 250) {
            const force = repulsionConstant / distanceSq;
            const fx = (dx / distance) * force;
            const fy = (dy / distance) * force;
            
            if (nodeA !== draggedNode) {
              nodeA.vx = (nodeA.vx || 0) - fx;
              nodeA.vy = (nodeA.vy || 0) - fy;
            }
            if (nodeB !== draggedNode) {
              nodeB.vx = (nodeB.vx || 0) + fx;
              nodeB.vy = (nodeB.vy || 0) + fy;
            }
          }
        }
      }

      // 2. Attraction along edges (Hooke's Law)
      graphData.edges.forEach(edge => {
        const sourceNode = nodeMap.get(edge.source);
        const targetNode = nodeMap.get(edge.target);
        
        if (sourceNode && targetNode) {
          const dx = (targetNode.x || 0) - (sourceNode.x || 0);
          const dy = (targetNode.y || 0) - (sourceNode.y || 0);
          const distance = Math.sqrt(dx * dx + dy * dy) || 1;
          
          const force = (distance - 80) * attractionConstant;
          const fx = (dx / distance) * force;
          const fy = (dy / distance) * force;
          
          if (sourceNode !== draggedNode) {
            sourceNode.vx = (sourceNode.vx || 0) + fx;
            sourceNode.vy = (sourceNode.vy || 0) + fy;
          }
          if (targetNode !== draggedNode) {
            targetNode.vx = (targetNode.vx || 0) - fx;
            targetNode.vy = (targetNode.vy || 0) - fy;
          }
        }
      });

      // 3. Gravity pulling towards center & update positions
      nextNodes.forEach(node => {
        if (node === draggedNode) return;
        
        // Pull to center
        const dx = centerX - (node.x || 0);
        const dy = centerY - (node.y || 0);
        node.vx = (node.vx || 0) + dx * centerForceConstant;
        node.vy = (node.vy || 0) + dy * centerForceConstant;
        
        // Damp and apply velocity
        node.vx *= damping;
        node.vy *= damping;
        node.x = (node.x || 0) + (node.vx || 0);
        node.y = (node.y || 0) + (node.vy || 0);

        // Keep inside bounds
        node.x = Math.max(30, Math.min(width - 30, node.x));
        node.y = Math.max(30, Math.min(height - 30, node.y));
      });

      setNodes(nextNodes);
      simulationRef.current = requestAnimationFrame(runSimulation);
    };

    simulationRef.current = requestAnimationFrame(runSimulation);
    return () => {
      if (simulationRef.current) cancelAnimationFrame(simulationRef.current);
    };
  }, [nodes.length, graphData, draggedNode]);

  // Click handler to open node summary drawer
  const handleNodeClick = async (node: GraphNode) => {
    setSelectedNode(node);
    setIsLoadingContent(true);
    setNodeContent(null);
    
    // Parse category and filename from node ID (e.g. 'papers/arxiv_2305_18290.md')
    const parts = node.id.split('/');
    if (parts.length < 2) return;
    
    const category = parts[0];
    const filename = parts[1];
    
    try {
      const res = await apiFetch(`/api/vault/read?category=${category}&filename=${filename}`);
      if (res.ok) {
        const data = await res.json();
        setNodeContent(data);
      }
    } catch (e) {
      console.error('Failed to load note content:', e);
    } finally {
      setIsLoadingContent(false);
    }
  };

  // Drag handlers
  const handleMouseDown = (node: GraphNode, e: React.MouseEvent) => {
    e.preventDefault();
    setDraggedNode(node);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!draggedNode || !svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    // Scale coordinates based on SVG width
    const svgWidth = 800;
    const svgHeight = 500;
    const scaleX = svgWidth / rect.width;
    const scaleY = svgHeight / rect.height;
    
    const mouseX = (e.clientX - rect.left) * scaleX;
    const mouseY = (e.clientY - rect.top) * scaleY;
    
    setNodes(prev => prev.map(n => {
      if (n.id === draggedNode.id) {
        return {
          ...n,
          x: mouseX,
          y: mouseY,
          vx: 0,
          vy: 0
        };
      }
      return n;
    }));
  };

  const handleMouseUp = () => {
    setDraggedNode(null);
  };

  // Filter nodes by search term
  const filteredNodes = nodes.filter(n => 
    n.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    n.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ display: 'grid', gridTemplateColumns: selectedNode ? '1fr 360px' : '1fr', height: '100%', gap: '16px', overflow: 'hidden' }}>
      
      {/* Main Graph Panel */}
      <div className="glass" style={{ display: 'grid', gridTemplateRows: 'auto 1fr', padding: '16px', overflow: 'hidden', position: 'relative' }}>
        
        {/* Graph Header Controls */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', zIndex: 10 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Network size={18} color="var(--primary)" />
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '15px', fontWeight: '700' }}>Obsidian Knowledge Graph</h3>
          </div>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <input 
              type="text" 
              placeholder="Search nodes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', fontSize: '12px', padding: '6px 12px', width: '180px', outline: 'none'
              }}
            />
            <button 
              onClick={fetchGraph}
              style={{
                background: 'var(--primary-glow)', border: 'none', color: 'var(--primary)', padding: '6px 12px', borderRadius: '6px', fontSize: '12px', cursor: 'pointer', fontWeight: '600'
              }}
            >
              Refresh Graph
            </button>
          </div>
        </div>

        {/* Legend */}
        <div style={{ position: 'absolute', bottom: '20px', left: '20px', display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '10px', color: 'var(--text-secondary)', background: 'rgba(10,11,14,0.8)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-color)', zIndex: 10 }}>
          <div style={{ fontWeight: 'bold', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '4px', marginBottom: '2px' }}>Legend</div>
          {Object.entries(CATEGORY_META).map(([key, meta]) => (
            <div key={key} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: meta.color }}></div>
              <span>{meta.label}</span>
            </div>
          ))}
        </div>

        {/* The SVG Canvas */}
        <div 
          style={{ width: '100%', height: '100%', overflow: 'hidden', cursor: draggedNode ? 'grabbing' : 'default' }}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
        >
          {isLoading ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: '12px', color: 'var(--text-muted)' }}>
              <Loader size={32} className="pulse-loading" style={{ animation: 'spin 2s linear infinite' }} />
              <span style={{ fontSize: '13px' }}>Parsing vault WikiLinks...</span>
            </div>
          ) : nodes.length === 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
              <span style={{ fontSize: '13px' }}>Graph is empty. Run a query on the Control Deck to generate notes.</span>
            </div>
          ) : (
            <svg 
              ref={svgRef}
              viewBox="0 0 800 500" 
              width="100%" 
              height="100%"
              style={{ display: 'block' }}
            >
              {/* Define Arrow Markers for Links */}
              <defs>
                <marker id="arrow" viewBox="0 0 10 10" refX="18" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="rgba(255,255,255,0.15)" />
                </marker>
              </defs>

              {/* Graph Edges */}
              {graphData?.edges.map((edge, idx) => {
                const nodeMap = new Map(nodes.map(n => [n.id, n]));
                const source = nodeMap.get(edge.source);
                const target = nodeMap.get(edge.target);
                if (!source || !target) return null;
                return (
                  <line 
                    key={idx}
                    x1={source.x}
                    y1={source.y}
                    x2={target.x}
                    y2={target.y}
                    stroke="rgba(255,255,255,0.08)"
                    strokeWidth="1.5"
                    markerEnd="url(#arrow)"
                  />
                );
              })}

              {/* Graph Nodes */}
              {filteredNodes.map(node => {
                const meta = CATEGORY_META[node.category] || { color: '#ffffff' };
                const isSelected = selectedNode?.id === node.id;
                const isHovered = hoveredNode?.id === node.id;
                
                return (
                  <g 
                    key={node.id} 
                    transform={`translate(${node.x || 0}, ${node.y || 0})`}
                    style={{ cursor: 'pointer' }}
                    onClick={() => handleNodeClick(node)}
                    onMouseDown={(e) => handleMouseDown(node, e)}
                    onMouseEnter={() => setHoveredNode(node)}
                    onMouseLeave={() => setHoveredNode(null)}
                  >
                    {/* Glowing outer ring on hover/select */}
                    {(isSelected || isHovered) && (
                      <circle 
                        r="14" 
                        fill="none" 
                        stroke={meta.color} 
                        strokeWidth="2" 
                        strokeOpacity="0.4"
                        style={{ transform: 'scale(1.2)', transformOrigin: 'center' }}
                      />
                    )}
                    
                    {/* Inner Node Circle */}
                    <circle 
                      r="8" 
                      fill={meta.color} 
                      stroke="rgba(255,255,255,0.8)" 
                      strokeWidth={isSelected ? '2' : '1'} 
                    />
                    
                    {/* Node Text Label */}
                    <text
                      y="-12"
                      textAnchor="middle"
                      fill={isSelected ? '#fff' : 'var(--text-secondary)'}
                      fontSize="9px"
                      fontWeight={isSelected ? 'bold' : '500'}
                      style={{ pointerEvents: 'none', background: '#000' }}
                    >
                      {node.title.length > 20 ? node.title.slice(0, 18) + '...' : node.title}
                    </text>
                  </g>
                );
              })}
            </svg>
          )}
        </div>
      </div>

      {/* Slide-out Sidebar details of selected node */}
      {selectedNode && (
        <div className="glass" style={{ display: 'grid', gridTemplateRows: 'auto 1fr', padding: '16px', overflow: 'hidden' }}>
          
          {/* Drawer Header */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', marginBottom: '12px' }}>
            <span style={{ fontSize: '10px', color: CATEGORY_META[selectedNode.category]?.color, fontWeight: '700', textTransform: 'uppercase' }}>
              {CATEGORY_META[selectedNode.category]?.label}
            </span>
            <button 
              onClick={() => setSelectedNode(null)}
              style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            >
              <X size={16} />
            </button>
          </div>

          {/* Drawer Content */}
          <div style={{ overflowY: 'auto', paddingRight: '4px' }}>
            {isLoadingContent ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: '10px', color: 'var(--text-muted)' }}>
                <Loader size={20} className="pulse-loading" style={{ animation: 'spin 2s linear infinite' }} />
                <span style={{ fontSize: '11px' }}>Loading note markdown...</span>
              </div>
            ) : nodeContent ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: 'bold', lineHeight: '1.3' }}>{selectedNode.title}</h4>
                
                {/* YAML Meta fields */}
                <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '11px' }}>
                  {Object.entries(nodeContent.frontmatter).map(([key, val]) => {
                    if (key === 'title') return null;
                    const displayVal = Array.isArray(val) ? val.join(', ') : String(val);
                    return (
                      <div key={key} style={{ display: 'flex', justifyContent: 'space-between', gap: '12px' }}>
                        <span style={{ color: 'var(--text-muted)', textTransform: 'capitalize' }}>{key}:</span>
                        <span style={{ color: 'var(--text-secondary)', textAlign: 'right', wordBreak: 'break-all' }}>{displayVal}</span>
                      </div>
                    );
                  })}
                </div>

                {/* Main Content Body */}
                <div style={{ fontSize: '12px', color: 'var(--text-primary)', lineHeight: '1.6', borderTop: '1px solid var(--border-color)', paddingTop: '12px', whiteSpace: 'pre-wrap' }}>
                  {nodeContent.content}
                </div>
              </div>
            ) : (
              <span style={{ fontSize: '12px', color: 'var(--danger)' }}>Failed to load document content.</span>
            )}
          </div>
        </div>
      )}
      
    </div>
  );
};

export default GraphView;
