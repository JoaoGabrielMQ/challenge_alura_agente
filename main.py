from agente import AgentePesquisa


def main():
    agente = AgentePesquisa()
    id_conversa = "conversa_local"

    while True:
        pergunta_usuario = input("\nVocê: ")

        if pergunta_usuario.strip().lower() == "sair":
            print("Encerrando o chat... Até logo!")
            break

        # Evita enviar perguntas vazias
        if not pergunta_usuario.strip():
            continue

        resposta = agente.funcao_agente(pergunta_usuario, id_conversa)

        print(f"\nAgente IA: {resposta}")


if __name__ == "__main__":
    main()
