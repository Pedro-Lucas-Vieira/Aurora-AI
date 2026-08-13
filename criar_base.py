
# ============================================================
# CRIAÇÃO DA BASE VETORIAL
# ============================================================
#
# Este arquivo deve ser executado sempre que novos documentos
# forem adicionados ou alterados.
#
# Exemplo:
#
# python criar_base.py
#
# ============================================================

import os

from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.vectorstores import FAISS

from leitor_documentos import ler_arquivo


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_DOCUMENTOS = "documentos"

PASTA_VECTORSTORE = "vectorstore"

MODELO_EMBEDDINGS = "gemini-embedding-2"


# ============================================================
# CARREGA A CHAVE DA API
# ============================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:

    raise ValueError(
        "A GOOGLE_API_KEY não foi encontrada no arquivo .env"
    )


# ============================================================
# PASTA DOS DOCUMENTOS
# ============================================================

if not os.path.exists(PASTA_DOCUMENTOS):

    raise FileNotFoundError(
        "A pasta 'documentos' não existe."
    )


# ============================================================
# MODELO DE EMBEDDINGS
# ============================================================

print()
print("=" * 60)
print("CARREGANDO MODELO DE EMBEDDINGS")
print("=" * 60)

print(f"Modelo: {MODELO_EMBEDDINGS}")

try:

    embeddings = GoogleGenerativeAIEmbeddings(
        model=MODELO_EMBEDDINGS,
        google_api_key=GOOGLE_API_KEY
    )

except Exception as erro:

    print()
    print("ERRO AO CARREGAR O MODELO DE EMBEDDINGS")
    print(type(erro).__name__)
    print(erro)

    raise


# ============================================================
# DIVISOR DE TEXTO
# ============================================================

divisor = RecursiveCharacterTextSplitter(

    chunk_size=1000,

    chunk_overlap=300
)


# ============================================================
# LISTA DE DOCUMENTOS
# ============================================================

todos_os_pedacos = []

arquivos_lidos = 0

arquivos_com_erro = 0


# ============================================================
# LEITURA DOS DOCUMENTOS
# ============================================================

print()
print("=" * 60)
print("LENDO DOCUMENTOS")
print("=" * 60)


# ============================================================
# PERCORRE TODAS AS SUBPASTAS
# ============================================================

for raiz, _, arquivos in os.walk(PASTA_DOCUMENTOS):

    for arquivo in arquivos:

        caminho = os.path.join(raiz, arquivo)

        categoria = os.path.basename(raiz)

        extensao = os.path.splitext(arquivo)[1].lower()


        print()
        print("--------------------------------------------")

        print(f"Arquivo   : {arquivo}")

        print(f"Categoria : {categoria}")

        print(f"Extensão  : {extensao}")


        try:

            # ------------------------------------------------
            # LÊ O ARQUIVO
            # ------------------------------------------------

            documentos = ler_arquivo(caminho)


            # ------------------------------------------------
            # VERIFICA SE FOI POSSÍVEL LER
            # ------------------------------------------------

            if not documentos:

                print("Formato não suportado ou arquivo vazio.")

                arquivos_com_erro += 1

                continue


            # ------------------------------------------------
            # ADICIONA A CATEGORIA AO METADATA
            # ------------------------------------------------

            for documento in documentos:

                documento.metadata["categoria"] = categoria

                documento.metadata["arquivo"] = arquivo


            # ------------------------------------------------
            # DIVIDE O DOCUMENTO EM PEDACOS
            # ------------------------------------------------

            pedacos = divisor.split_documents(
                documentos
            )


            # ------------------------------------------------
            # ADICIONA OS PEDACOS À LISTA
            # ------------------------------------------------

            todos_os_pedacos.extend(
                pedacos
            )


            arquivos_lidos += 1


            print(
                f"OK -> {len(pedacos)} pedaços criados."
            )


        except Exception as erro:

            arquivos_com_erro += 1

            print()
            print("ERRO AO PROCESSAR O ARQUIVO")

            print(
                f"Tipo: {type(erro).__name__}"
            )

            print(
                f"Detalhes: {erro}"
            )

            continue


# ============================================================
# RESUMO
# ============================================================

print()
print("=" * 60)
print("RESUMO")
print("=" * 60)

print(
    f"Arquivos lidos    : {arquivos_lidos}"
)

print(
    f"Arquivos com erro : {arquivos_com_erro}"
)

print(
    f"Total de pedaços  : {len(todos_os_pedacos)}"
)


# ============================================================
# VERIFICA SE EXISTEM DOCUMENTOS
# ============================================================

if not todos_os_pedacos:

    raise ValueError(
        "\nNenhum documento foi processado."
    )


# ============================================================
# CRIA A BASE FAISS
# ============================================================

print()
print("=" * 60)
print("CRIANDO BASE FAISS")
print("=" * 60)

print(
    f"Gerando embeddings para "
    f"{len(todos_os_pedacos)} pedaços..."
)


try:

    vectorstore = FAISS.from_documents(

        todos_os_pedacos,

        embeddings

    )

except Exception as erro:

    print()
    print("=" * 60)
    print("ERRO AO CRIAR A BASE FAISS")
    print("=" * 60)

    print(
        f"Tipo: {type(erro).__name__}"
    )

    print(
        f"Detalhes: {erro}"
    )

    raise


# ============================================================
# SALVA A BASE
# ============================================================

print()
print("=" * 60)
print("SALVANDO BASE VETORIAL")
print("=" * 60)


try:

    vectorstore.save_local(
        PASTA_VECTORSTORE
    )

except Exception as erro:

    print()
    print("ERRO AO SALVAR A BASE VETORIAL")

    print(
        f"Tipo: {type(erro).__name__}"
    )

    print(
        f"Detalhes: {erro}"
    )

    raise


# ============================================================
# FINALIZAÇÃO
# ============================================================

print()
print("=" * 60)
print("BASE CRIADA COM SUCESSO!")
print("=" * 60)

print(
    f"Pasta criada: {PASTA_VECTORSTORE}"
)

print(
    f"Documentos processados: {arquivos_lidos}"
)

print(
    f"Total de pedaços: {len(todos_os_pedacos)}"
)

print()
print("A base vetorial está pronta para o AURORA AI.")
print()

