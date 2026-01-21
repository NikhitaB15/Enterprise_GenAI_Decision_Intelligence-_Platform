from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import query_db, get_ml_insights, get_company_policy

load_dotenv()

app = FastAPI(title="Enterprise GenAI Decision Intelligence API")

# Define the Reasoning Engine
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

tools = [query_db, get_ml_insights, get_company_policy]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are the 'Enterprise Decision Intelligence' Agent. 
    Your goal is to help executives understand business performance and churn risk by combining ML insights, raw data, and company policies.
    
    You have access to:
    1. A SQL database with customer metrics.
    2. Structured ML insights (churn risk, segments).
    3. Documented company policies.
    
    When asked a question:
    - First, check the ML insights for context.
    - Second, query the SQL database if you need specific numbers or region-level data.
    - Third, cross-reference with company policies to provide actionable recommendations.
    
    Format your response with:
    ### Analysis
    ### Root Cause
    ### Recommended Actions
    """),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

class Query(BaseModel):
    message: str

class Response(BaseModel):
    answer: str

@app.get("/")
async def root():
    return {"status": "online", "message": "Enterprise GenAI Platform is running."}

@app.post("/ask", response_model=Response)
async def ask_question(query: Query):
    try:
        # Check for API key
        if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
            return {"answer": "### Error: OpenAI API Key not configured.\n\nPlease set your `OPENAI_API_KEY` in the `.env` file to enable the GenAI Reasoning Layer."}
            
        result = agent_executor.invoke({"input": query.message})
        return {"answer": result["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
