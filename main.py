from agente import AgentePesquisa
import uuid


def main():
    agente = AgentePesquisa()
    id_conversa = str(uuid.uuid4())

    while True:
        pergunta_usuario = input("\nVocê: ")
        if pergunta_usuario.strip().lower() == "sair":
            print("Encerrando o chat... Até logo!")
            break
        if not pergunta_usuario.strip():
            continue

        resposta = agente.funcao_agente(pergunta_usuario, id_conversa)

        print(f"\nAgente IA: {resposta}")


if __name__ == "__main__":
    main()
