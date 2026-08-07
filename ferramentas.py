from base_vetorial import criar_base_vetorial
from langchain_core.tools import tool


retriever = criar_base_vetorial()


@tool
def fazer_buscar(query: str) -> str:
    """Pesquise na base de dados e retorna a melhor resposta para o usuário"""
    resultado = retriever.invoke(query)
    return resultado
