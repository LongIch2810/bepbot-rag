from langchain.agents import create_agent
class Agent:
    def __init__(self,model, tools, system_prompt):
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt
        self._agent = create_agent(model, tools, system_prompt=self.system_prompt)

    def get_agent(self):
        return self._agent
    
        