
import langchain
import pkgutil

def find_member(package, member_name):
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        try:
            module = __import__(name, fromlist=[''])
            if hasattr(module, member_name):
                print(f"Found {member_name} in {name}")
        except Exception:
            continue

print("Searching for AgentExecutor and create_tool_calling_agent:")
find_member(langchain, "AgentExecutor")
find_member(langchain, "create_tool_calling_agent")
find_member(langchain, "create_openai_tools_agent")
