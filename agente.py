from ferramentas import fazer_buscar
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv

load_dotenv()


class AgentePesquisa:
    def __init__(self):
        self.tools = [fazer_buscar]
        self.llm = ChatGoogleGenerativeAI(api_key=os.getenv('GEMINI_API_KEY'), model="gemini-3.1-flash-lite")
        self.system_prompt = """Você é um assistente técnico prestativo. Você tem acesso a ferramentas para consultar documentos locais.
                    fazer_buscar: Use essa ferramente para fazer as buscas.
                    Se não conseguir uma resposta com fazer_buscar retorne 'Não encontrei a resposta.'
                    Responda SEMPRE em português brasileiro com base no que a ferramenta retornar."""
        self.agente = create_agent(model=self.llm, tools=self.tools, system_prompt=self.system_prompt, checkpointer=InMemorySaver())

    def funcao_agente(self, pergunta) -> dict:
        configuracao = {"configurable": {"thread_id": "conversa_aprendizado_01"}}

        resposta = self.agente.invoke({"messages": [("user", pergunta)]}, config=configuracao)
        return resposta['messages'][-1].content


agente = AgentePesquisa()

print(agente.funcao_agente(pergunta="Qual o checklist de WCAG 2.1 AA?"))
print(agente.funcao_agente(pergunta="Quantos itens são na pergunta anterior?"))
