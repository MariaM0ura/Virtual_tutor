from src.utils.llms.llm_interface import LLMInterface
from src.virtual_tutor.helpers import ActionSelection, ChainOfThought, Step

class VirtualTutor:
    def __init__(self) -> None:
        self.llm_interface = LLMInterface()
        # Store conversation history as a list of message dicts.
        self.conversation_history = []

    def _format_conversation_history(self) -> str:
        """
        Returns the conversation history as a formatted string.
        """
        if not self.conversation_history:
            return ""
        # Optionally, you could limit how many previous turns are included (for prompt length reasons)
        return "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" 
                         for msg in self.conversation_history)

    def classify_question(self, question: str) -> ActionSelection:
        """
        Classify the user's query into one of the four actions, 
        taking into account the conversation context.
        """
        history_str = self._format_conversation_history()
        context_info = f"Histórico da conversa:\n{history_str}\n\n" if history_str else ""
        system_prompt = (
            f"{context_info}"
            "Você é um classificador inteligente em um diálogo contínuo. "
            "Dada a pergunta de um usuário, escolha uma das seguintes ações: "
            "'explain_concept', 'generate_problem', 'solve_problem' ou 'adjust_explaination'. "
            "Retorne um objeto JSON com exatamente uma chave 'acao' cujo valor seja um desses strings. "
            "Responda apenas em Português."
        )
        user_prompt = f"User query: {question}"
        return self.llm_interface.get_response(system_prompt, user_prompt, ActionSelection)

    def explain_concept(self, concept: str) -> ChainOfThought:
        """
        Explain a math concept using a step-by-step chain-of-thought with conversation context.
        """
        history_str = self._format_conversation_history()
        context_info = f"Histórico da conversa:\n{history_str}\n\n" if history_str else ""
        system_prompt = (
            f"{context_info}"
            "Você é um tutor de matemática muito útil em um diálogo contínuo. Explique o conceito fornecido passo a passo, "
            "usando uma abordagem de cadeia de raciocínio. Retorne um objeto JSON com uma lista de 'passos' "
            "(cada passo deve ter 'explicacao' e 'saida') e uma 'resposta_final' que seja uma explicação concisa. "
            "Certifique-se de que toda a resposta esteja em Português e que todas as expressões matemáticas estejam "
            "envoltas em $ para serem renderizadas como LaTeX."
        )
        user_prompt = f"Explique o conceito: {concept}"
        return self.llm_interface.get_response(system_prompt, user_prompt, ChainOfThought)

    def generate_problem(self, thema: str) -> ChainOfThought:
        """
        Generate a math problem with an explanation of the creative process in a conversational context.
        """
        history_str = self._format_conversation_history()
        context_info = f"Histórico da conversa:\n{history_str}\n\n" if history_str else ""
        system_prompt = (
            f"{context_info}"
            "Você é um tutor de matemática em uma conversa contínua. Gere um problema matemático interessante e descreva seu processo "
            "criativo passo a passo usando uma cadeia de raciocínio. Retorne um objeto JSON com uma lista de 'passos' "
            "(cada passo com 'explicacao' e 'saida') e uma 'resposta_final' que seja o problema gerado. "
            "A resposta deve estar em Português e todas as expressões matemáticas devem estar envoltas em $ para "
            "serem renderizadas como LaTeX."
        )
        user_prompt = f"Crie um problema sobre: {thema}"
        return self.llm_interface.get_response(system_prompt, user_prompt, ChainOfThought)

    def solve_problem(self, problem: str) -> ChainOfThought:
        """
        Solve a math problem step by step using a chain-of-thought in a more conversational manner.
        """
        history_str = self._format_conversation_history()
        context_info = f"Histórico da conversa:\n{history_str}\n\n" if history_str else ""
        system_prompt = (
            f"{context_info}"
            "Você é um tutor de matemática conversacional. Resolva o problema a seguir passo a passo usando uma cadeia de raciocínio. "
            "Retorne um objeto JSON com uma lista de 'passos' (cada passo com 'explicacao' e 'saida') "
            "e uma 'resposta_final' representando a solução final. "
            "Forneça a resposta em Português e garanta que todas as expressões matemáticas estejam envoltas em $ para "
            "serem renderizadas como LaTeX."
        )
        user_prompt = f"Resolva o problema: {problem}"
        return self.llm_interface.get_response(system_prompt, user_prompt, ChainOfThought)

    def adjust_explaination(self, student_answer: str, correct_answer: str) -> ChainOfThought:
        """
        Provide personalized feedback on the student's answer using a chain-of-thought explanation, 
        taking into account previous conversation context.
        """
        history_str = self._format_conversation_history()
        context_info = f"Histórico da conversa:\n{history_str}\n\n" if history_str else ""
        system_prompt = (
            f"{context_info}"
            "Você é um tutor de matemática conversacional. Um aluno forneceu uma resposta que pode estar incorreta. "
            "Explique passo a passo, usando uma cadeia de raciocínio, onde ocorreu o erro e como melhorar. "
            "Retorne um objeto JSON com uma lista de 'passos' (cada passo com 'explicacao' e 'saida') "
            "e uma 'resposta_final' que resuma o feedback. "
            "Certifique-se de que a resposta esteja em Português e que todas as expressões matemáticas estejam "
            "envoltas em $ para serem renderizadas como LaTeX."
        )
        user_prompt = f"Resposta do aluno: {student_answer}\nResposta correta: {correct_answer}"
        return self.llm_interface.get_response(system_prompt, user_prompt, ChainOfThought)

    def handle_query(self, query: str, **kwargs) -> ChainOfThought:
        """
        Classify the query and invoke the corresponding chain-of-thought method in a conversational context.
        
        For 'adjust_explaination', provide additional keyword arguments:
            - student_answer: str
            - correct_answer: str
        """
        # Add the user's query to the conversation history.
        self.conversation_history.append({"role": "user", "content": query})
        # Perform classification
        classification = self.classify_question(query)
        action = classification.action

        # Create a step to show the classification result to the user.
        classification_step = Step(
            explanation="Classificação da pergunta realizada.",
            output=f"A ação identificada foi: {action}"
        )

        # Process the query based on the detected action.
        if action == 'explain_concept':
            cot = self.explain_concept(query)
        elif action == 'generate_problem':
            cot = self.generate_problem(query)
        elif action == 'solve_problem':
            cot = self.solve_problem(query)
        elif action == 'adjust_explaination':
            student_answer = kwargs.get("student_answer", "N/A")
            correct_answer = kwargs.get("correct_answer", "N/A")
            cot = self.adjust_explaination(student_answer, correct_answer)
        else:
            # Fallback chain-of-thought for an unrecognized action.
            cot = ChainOfThought(
                steps=[Step(explanation="Unable to classify the query into a valid action.", output="")],
                final_answer="No action taken."
            )

        # Insert the classification result as the first step.
        cot.steps.insert(0, classification_step)
        # Append the assistant's response to the conversation history.
        self.conversation_history.append({"role": "assistant", "content": cot.final_answer})
        return cot
    
# --- Example Usage ---

if __name__ == "__main__":
    tutor = VirtualTutor()
    
    # Example 1: Explain a math concept 
    query1 = "Explique o conceito de derivadas."
    cot_explanation = tutor.handle_query(query1)
    print("Chain-of-Thought for explain_concept:")
    print(cot_explanation.model_dump_json(indent=2))

    # Example 2: Generate a math problem
    query2 = "Crie um problema sobre equações quadráticas."
    cot_problem = tutor.handle_query(query2)
    print("\nChain-of-Thought for generate_problem:")
    print(cot_problem.model_dump_json(indent=2))
    
    # Example 3: Solve a math problem 
    query3 = "Resolva a equação 8x + 7 = -23."
    cot_solution = tutor.handle_query(query3)
    print("\nChain-of-Thought for solve_problem:")
    print(cot_solution.model_dump_json(indent=2))
    
    # Example 4: Adjust explanation (feedback)
    query4 = "Não entendi bem a explicação fornecida."
    cot_feedback = tutor.handle_query(query4, student_answer="Acho que 2+2=5", correct_answer="2+2=4")
    print("\nChain-of-Thought for adjust_explaination:")
    print(cot_feedback.model_dump_json(indent=2))