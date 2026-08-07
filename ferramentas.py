from langchain_core.tools import create_retriever_tool
from base_vetorial import criar_base_vetorial

retriever = criar_base_vetorial()

fazer_buscar = create_retriever_tool(
    retriever=retriever,
    name="fazer_buscar",
    description=("Use esta ferramenta para buscar informações dentro dos documentos técnicos ")
)
