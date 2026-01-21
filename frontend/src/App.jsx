import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Zap, BarChart3, ShieldAlert, Cpu, RefreshCw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([
        {
            type: 'ai',
            text: "### Welcome to Decision Intelligence\nI am connected to your enterprise data and ML pipelines. How can I assist you with business reasoning today?"
        }
    ]);
    const [loading, setLoading] = useState(false);
    const [metrics, setMetrics] = useState({
        churnRate: '15.2%',
        highRiskCount: '152',
        lastUpdate: 'Just now'
    });

    const chatEndRef = useRef(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { type: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await axios.post('/api/ask', { message: input });
            setMessages(prev => [...prev, { type: 'ai', text: response.data.answer }]);
        } catch (error) {
            setMessages(prev => [...prev, { type: 'ai', text: "### Error\nCould not connect to the reasoning engine. Please ensure the backend is running and OPENAI_API_KEY is set." }]);
        } finally {
            setLoading(false);
        }
    };

    const formatText = (text) => {
        // Simple mock markdown formatter
        return text.split('\n').map((line, i) => {
            if (line.startsWith('### ')) return <h3 key={i}>{line.replace('### ', '')}</h3>;
            if (line.startsWith('- ')) return <li key={i}>{line.replace('- ', '')}</li>;
            return <p key={i}>{line}</p>;
        });
    };

    return (
        <div className="app-container">
            <header>
                <div>
                    <h1>Enterprise GenAI</h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Decision Intelligence Platform</p>
                </div>
                <div className="status-badge">
                    <Zap size={12} style={{ marginRight: '4px' }} />
                    System Operational
                </div>
            </header>

            <main className="dashboard-grid">
                <section className="main-panel">
                    <div className="chat-history">
                        <AnimatePresence>
                            {messages.map((msg, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`message ${msg.type}`}
                                >
                                    {formatText(msg.text)}
                                </motion.div>
                            ))}
                        </AnimatePresence>
                        {loading && (
                            <div className="message ai">
                                <motion.div
                                    animate={{ opacity: [0.4, 1, 0.4] }}
                                    transition={{ repeat: Infinity, duration: 1.5 }}
                                >
                                    Reasoning across data sources...
                                </motion.div>
                            </div>
                        )}
                        <div ref={chatEndRef} />
                    </div>

                    <div className="input-area">
                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask a strategic question (e.g., 'Why is churn high in North region?')"
                        />
                        <button onClick={handleSend} disabled={loading}>
                            <Send size={18} />
                        </button>
                    </div>
                </section>

                <aside className="side-panel">
                    <div className="card metric-card">
                        <h3><BarChart3 size={16} /> Current Churn Rate</h3>
                        <div className="value">{metrics.churnRate}</div>
                        <p style={{ fontSize: '0.8rem', color: '#4ade80' }}>+0.2% vs last month</p>
                    </div>

                    <div className="card metric-card">
                        <h3><ShieldAlert size={16} /> High Risk Customers</h3>
                        <div className="value" style={{ color: '#f87171' }}>{metrics.highRiskCount}</div>
                        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Based on ML Analysis</p>
                    </div>

                    <div className="card">
                        <h3 style={{ fontSize: '0.8rem', marginBottom: '1rem', display: 'flex', alignItems: 'center' }}>
                            <Cpu size={16} style={{ marginRight: '8px' }} />
                            Active Pipeline
                        </h3>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                            <RefreshCw size={14} className="spin" />
                            Airflow: refresh_insights_dag
                        </div>
                        <div style={{ marginTop: '1rem', fontSize: '0.8rem', padding: '0.5rem', background: 'rgba(0,0,0,0.2)', borderRadius: '8px' }}>
                            <code style={{ color: '#60a5fa' }}>Status: RUNNING</code>
                        </div>
                    </div>
                </aside>
            </main>
        </div>
    );
}

export default App;
