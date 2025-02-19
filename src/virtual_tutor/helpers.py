from pydantic import BaseModel
from typing import List, Literal



# --- Action Classifier Model ---

class ActionSelection(BaseModel):
    action: Literal['explain_concept', 'generate_problem', 'solve_problem', 'adjust_explaination']

# --- Chain-of-Thought Models ---

class Step(BaseModel):
    explanation: str
    output: str

class ChainOfThought(BaseModel):
    steps: List[Step]
    final_answer: str
