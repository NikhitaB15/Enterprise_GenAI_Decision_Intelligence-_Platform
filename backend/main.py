from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import query_db, get_ml_insights, get_company_policy

load_dotenv()

app = FastAPI(title="Enterprise GenAI Decision Intelligence API")

# Define the Reasoning Engine
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("WARNING: GROQ_API_KEY not found in environment variables.")

# Use native ChatGroq implementation
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)
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
    
    IMPORTANT: Use the provided tools to get information. Do NOT try to format tool calls yourself using tags like <function>. 
    The system will handle the tool call format. Just output the tool usage.
    
    Format your final response with:
    ### Analysis
    ### Root Cause
    ### Recommended Actions
    """),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
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
        if not os.getenv("GROQ_API_KEY"):
            return {"answer": "### Error: Groq API Key not configured.\n\nPlease set your `GROQ_API_KEY` in the `.env` file to enable the GenAI Reasoning Layer."}
        print("Processing query:", query.message)    
        try:
            result = agent_executor.invoke({"input": query.message})
            return {"answer": result["output"]}
        except Exception as inner_e:
            print(f"Error during agent execution: {str(inner_e)}")
            # If it's a tool-calling error specifically, provide a cleaner message
            if "BadRequestError" in str(inner_e) or "400" in str(inner_e):
                 return {"answer": "### Error: Reasoning Engine Failure\n\nThe AI model had trouble formatting the data request correctly. This usually happens if the search query is too complex. Please try rephrasing your question."}
            raise inner_e
    except Exception as e:
        print(f"Global Exception in /ask: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
