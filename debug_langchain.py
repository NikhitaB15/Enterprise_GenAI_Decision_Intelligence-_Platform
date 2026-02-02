
try:
    from langchain.agents import create_openai_tools_agent
    print("SUCCESS: create_openai_tools_agent found in langchain.agents")
except ImportError as e:
    print(f"FAILURE: {e}")
    try:
        from langchain.agents import create_tool_calling_agent
        print("INFO: create_tool_calling_agent found (alternative)")
    except ImportError:
        pass
    import langchain
    print(f"LangChain Version: {langchain.__version__}")
