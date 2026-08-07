from ferramentas import fazer_buscar
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    user_query: str
    web_answer: str
    scientific_answer: str
    final_answer: str


def funcao_agente_web(state: AgentState) -> dict:
    tools = [fazer_buscar]
    llm = ChatGoogleGenerativeAI(api_key=os.getenv('GEMINI_API_KEY'), model="gemini-3.1-flash-lite")
    system_prompt = """Você é um assistente técnico prestativo. Você tem acesso a ferramentas para consultar documentos locais.
                    fazer_buscar: Use essa ferramente para fazer as buscas.
                    Se não conseguir uma resposta com fazer_buscar retorne 'Não encontrei a resposta.'
                    Responda SEMPRE em português brasileiro com base no que a ferramenta retornar."""

    agente = create_agent(model=llm, tools=tools, system_prompt=system_prompt)

    resposta = agente.invoke({"messages": [("user", state["Qual o checklist de WCAG 2.1 AA?"])]})
    return resposta['messages'][-1].content

print(funcao_agente_web())
