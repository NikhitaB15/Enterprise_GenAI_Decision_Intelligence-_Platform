# Implementation Plan - Enterprise GenAI Decision Intelligence Platform

## 🏗 Architecture Overview

1.  **Data Layer**: BigQuery/SQL (Simulated via SQLite for local dev) + Document Store.
2.  **ML Insights**: Python-based ML pipeline for forecasting/classification.
3.  **Orchestration**: Airflow DAGs for data ingestion, ML runs, and Vector DB updates.
4.  **Reasoning Engine**: FastAPI + LLM Agent (LangChain/PydanticAI) with Tool Calling.
5.  **User Interface**: React Dashboard with natural language interaction.

## 🚀 Phases

### Phase 1: Foundation & Project Structure
- [ ] Initialize project structure: `/backend`, `/frontend`, `/airflow`, `/data`, `/ml`.
- [ ] Set up Python virtual environment and `requirements.txt`.
- [ ] Configure environment variables (.env).

### Phase 2: Data & ML Simulation
- [ ] Create a `data_generator.py` to create mock customer/enterprise data in SQLite.
- [ ] Build a `churn_prediction.py` (or similar) to generate structured "Insights" (JSON/SQL).
- [ ] Prepare sample enterprise PDFs/Markdown for RAG testing.

### Phase 3: The Reasoning Engine (Backend)
- [ ] Setup FastAPI server.
- [ ] Implement Vector DB (ChromaDB) for document retrieval.
- [ ] Implement SQL Agent Tools for querying the "BigQuery" surrogate.
- [ ] Design the "Reasoning Layer": A prompt that takes ML insights + Docs + SQL results to generate recommendations.

### Phase 4: Orchestration (Airflow)
- [ ] Setup local Airflow (Docker or local installation).
- [ ] Create DAG to simulate the "Reason-Refresh" cycle.

### Phase 5: Modern Dashboard (Frontend)
- [ ] Initialize Vite + React.
- [ ] Design a premium UI using CSS (vibrant colors, glassmorphism).
- [ ] Implement a "Decision Command Center" where users ask questions and see the reasoning trace.

### Phase 6: Polish & Documentation
- [ ] Refine LLM prompts for "Executive Summary" style.
- [ ] Add loading states and micro-animations.
- [ ] Finalize README and project walkthrough.
