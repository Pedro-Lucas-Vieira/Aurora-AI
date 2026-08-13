
# ============================================================
# CHATBOT DA AURORA S.A.
# ============================================================

import os

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS



# CONFIGURAÇÕES


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY não encontrada no .env")



# EMBEDDINGS


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=GOOGLE_API_KEY
)



# CARREGA A BASE FAISS


print("Carregando base vetorial...")

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

print("Base vetorial carregada com sucesso.")



# MODELO GEMINI


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # <--- ATUALIZADO AQUI
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2

)

#
# HISTÓRICO
#

historico = []


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def responder(pergunta):

    # Pesquisa na base de documentos
    documentos = vectorstore.similarity_search(
        pergunta,
        k=4
    )

    # Junta os documentos encontrados
    contexto = ""

    for documento in documentos:
        contexto += documento.page_content
        contexto += "\n\n"

    # Pega as últimas mensagens
    conversa = "\n".join(historico[-8:])

    # Prompt
    prompt = f"""
Você é o AURORA S.A, assistente corporativo da empresa AURORA S.A.

Sua função é responder dúvidas dos colaboradores utilizando EXCLUSIVAMENTE
as informações presentes na documentação interna da empresa.

=========================
REGRAS
=========================

1. Utilize apenas as informações do contexto recuperado.

2. Nunca invente informações ou complemente respostas com conhecimento próprio.

3. Explique o conteúdo com suas próprias palavras, evitando copiar grandes trechos da documentação.

4. Utilize linguagem profissional, clara, objetiva e cordial.

5. Sempre que fizer sentido, organize a resposta em pequenos parágrafos ou listas.

6. Quando a resposta estiver baseada em uma política, manual, procedimento ou diretriz interna, introduza naturalmente com expressões como:
- "Conforme a política da empresa..."
- "Com base na política interna..."
- "Segundo as diretrizes da empresa..."
- "De acordo com o procedimento interno..."

Escolha a expressão que melhor se encaixar na situação.

7. Nunca mencione nomes de arquivos, extensões (.pdf, .docx, .xlsx, .md, .html) ou detalhes técnicos da implementação.

8. Caso a informação não exista na documentação, responda exatamente:
"Não encontrei essa informação na documentação da empresa."

9. Caso a pergunta não esteja relacionada à documentação interna da empresa, responda:
"Posso ajudar apenas com informações presentes na documentação interna da AURORA S.A."

10. Cumprimente, agradeça ou despeça-se naturalmente quando apropriado.

HISTÓRICO:
{conversa}

DOCUMENTAÇÃO:
{contexto}

PERGUNTA:
{pergunta}
=========================
INSTRUÇÃO FINAL
=========================

Escreva uma resposta natural, profissional e objetiva.
Não mencione arquivos ou detalhes técnicos.
Quando apropriado, indique que a resposta está baseada em uma política, procedimento ou diretriz interna da empresa.

"""

    # Envia para o Gemini
    resposta = llm.invoke(prompt)

    # A resposta pode vir como texto ou lista
    if isinstance(resposta.content, str):

        texto = resposta.content

    else:

        texto = ""

        for item in resposta.content:

            if isinstance(item, dict) and "text" in item:
                texto += item["text"]

            elif isinstance(item, str):
                texto += item

    # Salva no histórico
    historico.append(
        f"Usuário: {pergunta}"
    )

    historico.append(
        f"Assistente: {texto}"
    )

    # Mantém somente as últimas mensagens
    if len(historico) > 20:
        historico.pop(0)
        historico.pop(0)

    return texto.strip()

