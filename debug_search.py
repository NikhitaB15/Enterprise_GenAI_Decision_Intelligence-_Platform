
import langchain.agents
print("Searching for create_* functions in langchain.agents:")
for x in dir(langchain.agents):
    if x.startswith("create"):
        print(x)
