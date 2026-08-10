# Assistente de Pesquisa — Santo Pegasus

Agente de inteligência artificial que responde perguntas sobre documentos técnicos internos da empresa **Santo Pegasus**. O usuário faz perguntas em linguagem natural e o agente busca as informações nos documentos PDF da base de conhecimento, respondendo sempre em português.

---

## Arquitetura da Solução

O projeto segue um padrão **RAG (Retrieval-Augmented Generation)**: os documentos são convertidos em vetores e armazenados em memória; quando o usuário faz uma pergunta, o agente recupera os trechos mais relevantes e usa um LLM para formular a resposta.

```
Usuário
   │
   ▼
Interface (Streamlit ou CLI)
   │
   ▼
AgentePesquisa  ←─── Memória de conversa (InMemorySaver / thread_id)
   │
   ├── LLM: Gemini Flash (via LangChain + LangGraph)
   │
   └── Ferramenta: fazer_buscar
            │
            ▼
      Base Vetorial (InMemoryVectorStore)
            │
            ▼
      Documentos PDF  →  chunks de 600 chars  →  embeddings (embeddinggemma-300m)
```

**Fluxo de dados:**

1. **`base_vetorial.py`** — ao iniciar, carrega todos os PDFs de `./documentos/`, divide em chunks (600 caracteres, sobreposição de 100) e gera embeddings com o modelo `google/embeddinggemma-300m` (HuggingFace). O resultado é um `InMemoryVectorStore` (não persistido em disco).
2. **`ferramentas.py`** — expõe o retriever como uma ferramenta LangChain (`fazer_buscar`) para o agente.
3. **`agente.py`** — define a classe `AgentePesquisa`, que usa `create_agent` do LangGraph com Gemini Flash e `InMemorySaver` para manter histórico por `thread_id`.
4. **`app.py`** — interface web via Streamlit, com histórico visual e botão de nova conversa.
5. **`main.py`** — interface de linha de comando, útil para testes rápidos.

---

## Tecnologias e Ferramentas

| Camada | Tecnologia |
|---|---|
| LLM | Google Gemini (`gemini-3.1-flash-lite`) via `langchain-google-genai` |
| Embeddings | `google/embeddinggemma-300m` via `langchain-huggingface` |
| Orquestração do agente | LangGraph (`create_agent`, `InMemorySaver`) |
| Recuperação de documentos | LangChain (`InMemoryVectorStore`, `create_retriever_tool`) |
| Carregamento de PDFs | `PyPDFLoader` + `DirectoryLoader` |
| Interface web | Streamlit |
| Variáveis de ambiente | `python-dotenv` |

---

## Como Executar

### Pré-requisitos

- Python 3.11+
- Chave de API do Google Gemini

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requiremets.txt
```

### 3. Configurar a variável de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
GEMINI_API_KEY=sua_chave_aqui
```

### 4. Adicionar os documentos

Coloque os arquivos PDF que o agente deve consultar na pasta `./documentos/`.

### 5. Executar

**Interface web (recomendado):**
```bash
streamlit run app.py
```
Acesse `http://localhost:8501` no navegador.

**Interface de linha de comando:**
```bash
python main.py
```
Digite `sair` para encerrar o chat.

> **Atenção:** a base vetorial é criada na memória a cada inicialização, então o tempo de arranque depende do tamanho dos documentos e do download do modelo de embeddings na primeira execução.

---

## Exemplos de Perguntas

- *"Como a Santo Pegasus responde a incidentes?"*
- *"Quais os 4 pilares da excelência em engenharia da empresa?"*
- *"Quando a empresa começou?"*

---

## Exemplos de Respostas

**Pergunta:** Como a Santo Pegasus responde a incidentes?

**Resposta do agente:**
> A Santo Pegasus trata a resposta a incidentes com base em uma cultura de segurança psicológica e aprendizado sistêmico, utilizando as seguintes diretrizes:
> * Cultura Blameless (Sem Culpa): As investigações de incidentes (feitas via Post-Mortem) focam no sistema, não no indivíduo. A pergunta central não é "quem errou?", mas "por que o sistema permitiu que aquela ação causasse impacto?". Ocultar erros deliberadamente é considerado uma falha grave e passível de demissão, pois a empresa valoriza a transparência como o "melhor desinfetante tecnológico".
> * Segurança Psicológica: Qualquer colaborador, independentemente do cargo ou tempo de casa, é incentivado a declarar um incidente imediatamente ao percebê-lo, sem medo de retaliação.
> * Ciclo OODA (Observe, Orient, Decide, Act): A resposta a incidentes segue um processo estruturado militarizado, dividindo a ação em duas fases distintas:
>  * Mitigação: Focada na estabilização imediata e na continuidade do serviço (prioridade total para o usuário/cliente).
>  * Resolução: Focada na correção definitiva do bug no código.
> * Fluxo de Resposta:
>  * Detecção: Capturada por monitoramento (ex: Prometheus).
>  * Triagem: O engenheiro on-call avalia o impacto em menos de 5 minutos.
>  * Declaração: Se o impacto for grave, declara-se um SEV-1, aciona-se um Incident Commander e abre-se uma War Room.
> * Foco em Prevenção: O objetivo final das investigações é implementar proteções arquiteturais (como infraestrutura imutável e testes de caos) para garantir que aquele erro específico não possa ser repetido. Além disso, a empresa busca reduzir o Toil (trabalho massante), automatizando alertas sempre que possível para focar o tempo de engenharia em melhorias estruturais.

---

**Pergunta:** Quais os 4 pilares da excelência em engenharia da empresa?

**Resposta do agente:**
> Os quatro pilares inegociáveis da excelência em engenharia da Santo Pegasus são:
> 1. Propriedade Técnica (Ownership): O desenvolvedor é responsável pelo ciclo de vida completo do seu código, desde o design até o monitoramento em produção.
> 1. Simplicidade Radical: Resolver problemas complexos com o mínimo de código necessário, partindo do princípio de que código que não existe não possui bugs.
> 1. Segurança por Design: A conformidade com a LGPD e a proteção contra ameaças cibernéticas são integradas desde a primeira linha de código, e não apenas no momento do deploy.
> 1. Evolução Contínua: Adoção do "Kaizen" (melhoria constante), tratando os guias de engenharia como organismos vivos que refletem o estado da arte da tecnologia.

---

**Pergunta:** Quando a empresa começou?

**Resposta do agente:**
> A Santo Pegasus nasceu em 2018, na garagem de um sobrado no bairro da Vila Madalena, em São Paulo. Ela foi fundada por três pessoas: uma engenheira de dados, um arquiteto de software e uma product designer.

**Pergunta:** Qual o tamanho da lua?

**Resposta do agente:**
> Não tenho essa resposta na minha base de dados.
