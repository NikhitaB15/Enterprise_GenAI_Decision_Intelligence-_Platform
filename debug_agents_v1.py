
import langchain.agents
import inspect

print("Searching for agent-related functions in langchain.agents:")
for name, obj in inspect.getmembers(langchain.agents):
    if "agent" in name.lower():
        print(f"{name}: {type(obj)}")
