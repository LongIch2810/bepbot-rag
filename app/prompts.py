class Prompts:
    def __init__(self, prompt):
        self._prompt = prompt
        
    def get_system_prompt(self):
        return self._prompt