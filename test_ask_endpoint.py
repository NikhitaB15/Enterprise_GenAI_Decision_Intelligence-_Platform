"""Test script to reproduce the NoneType error"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("Testing imports...")
    from backend.main import app, agent_executor
    
    print("Testing agent execution...")
    result = agent_executor.invoke({"input": "What is the churn rate?"})
    print("Success! Result:", result)
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
