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
        self.system_prompt = """Você é um assistente técnico prestativo da empresa Santo Pegasus.
                    Sua função é consultar documentos locais e responder perguntas sobre eles.
                    
                    Use ferramentas para consultar:
                    - fazer_buscar: Use essa ferramente para fazer as buscas.
                    
                    Se não conseguir uma resposta com fazer_buscar SEMPRE retorne 'Não tenho essa resposta na minha base de dados.'
                    
                    Responda SEMPRE em português brasileiro com base no que a ferramenta retornar."""
        self.agente = create_agent(model=self.llm, tools=self.tools, system_prompt=self.system_prompt,
                                   checkpointer=InMemorySaver())

    def funcao_agente(self, pergunta, id_conversa) -> dict:
        configuracao = {"configurable": {"thread_id": id_conversa}}

        resposta = self.agente.invoke({"messages": [("user", pergunta)]}, config=configuracao)
        return resposta['messages'][-1].content[0].get('text', '')
