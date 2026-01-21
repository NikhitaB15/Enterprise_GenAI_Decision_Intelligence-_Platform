# Project Walkthrough: Enterprise GenAI Decision Intelligence Platform

Welcome to your new enterprise-grade GenAI platform! This project is designed to showcase how GenAI can be integrated into existing ML and Data Engineering ecosystems.

## 1. The Data Foundation (`/ml` and `/data`)
- **`data_generator.py`**: Simulates a "BigQuery" surrogate using SQLite. It creates realistic customer data including regions, spend, support tickets, and churn flags.
- **`churn_reasoning.py`**: Acts as your "ML Model". It analyzes the raw data and extracts high-level KPI insights (e.g., "Region North is high risk") and saves them as structured JSON.
- **`enterprise_data.db`**: The single source of truth for the platform.

## 2. The Orchestration Layer (`/airflow`)
- **`refresh_insights_dag.py`**: A standard Airflow DAG that automates the flow from raw data to ML insights. This demonstrates your ability to build production-grade pipelines.

## 3. The Reasoning Engine (`/backend`)
- **`tools.py`**: The "eyes and ears" of the GenAI. It defines tools for SQL querying, reading ML insights, and fetching company policy.
- **`main.py`**: A FastAPI application that hosts a LangChain agent. This agent takes a natural language question and decides which tools to use to find the answer.
- **System Prompt**: The agent is programmed to follow a specific reasoning logic: **Analyze -> Identify Root Cause -> Recommend Actions**.

## 4. The Decision Command Center (`/frontend`)
- **Design**: Built with a "Premium-First" approach. Glassmorphism, deep dark mode, and vibrant accents create a high-end enterprise feel.
- **Interactions**: The chat interface is connected directly to the Reasoning Engine.
- **Live Metrics**: Sidebar components show live KPIs directly from the data store.

## How to Pitch This Project
When talking to recruiters, focus on:
1. **Hybrid Approach**: "I didn't just build a chatbot; I built a reasoning layer on top of a working ML pipeline."
2. **Data-Centricity**: "The AI's answers are grounded in real SQL data and business policies, preventing hallucinations."
3. **Production Readiness**: "I included Airflow DAGs and a FastAPI backbone to show how this fits into a real enterprise stack."
