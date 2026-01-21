# Enterprise GenAI Decision Intelligence Platform

A sophisticated platform that combines traditional ML pipelines with GenAI reasoning to provide actionable business intelligence.

## 🚀 Key Features
- **Data & ML Layer**: Automated pipelines that generate customer metrics and churn risk scores.
- **Orchestration**: Airflow-ready DAGs to manage data flows and insight refreshes.
- **GenAI Reasoning**: An LLM agent that reasons across SQL data, ML insights, and company policies.
- **Premium Dashboard**: A modern, glassmorphic React interface for natural language business queries.

## 🏗 Project Structure
```text
├── backend/            # FastAPI reasoning engine & LangChain tools
├── frontend/           # Vite + React premium dashboard
├── ml/                 # Data generation and ML simulation scripts
├── airflow/           # DAG definitions for pipeline orchestration
├── data/               # SQLite and JSON data stores
├── docs/               # Unstructured company policies & SOPs
└── requirements.txt    # Python dependencies
```

## 🛠 Setup & Launch

### 1. Backend Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key in a `.env` file (see `.env.example`):
   ```text
   OPENAI_API_KEY=sk-...
   ```
3. Initialize the data:
   ```bash
   python ml/data_generator.py
   python ml/churn_reasoning.py
   ```
4. Start the FastAPI server:
   ```bash
   python -m backend.main
   ```

### 2. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

### 3. Airflow (Optional)
Drop the `airflow/refresh_insights_dag.py` into your Airflow DAGs folder to enable scheduled refreshes.

## 🧠 Reasoning Example
Ask the platform:
- *"Why is churn high in the North region?"*
- *"What are the recommended actions for high-risk customers with many support tickets?"*

The agent will query the database, read ML insights, check company policy, and provide a structured decision-ready response.

## 📊 Data Strategy
This platform uses a hybrid data approach to mirror real-world enterprise environments:
- **Structured Data**: Customer profiles and churn metrics based on realistic distributions (inspired by Telco/Banking sectors).
- **Unstructured Docs**: Company policy PDFs and SOPs located in `/docs` to simulate real-world RAG scenarios.
- **Synthetic Augmentation**: High-fidelity synthetic data for tickets and feedback to simulate active enterprise workloads.

*"The platform uses public enterprise datasets and synthetic data to simulate real production environments. This mirrors how GenAI systems are prototyped in regulated industries."*
