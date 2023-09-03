from dotenv import load_dotenv

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

load_dotenv()


def call_langchain(content_name, query):
    loader = TextLoader(f"./{content_name}.txt", encoding="UTF-*")
    document = loader.load()

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
    )

    docs = text_splitter.split_documents(document)

    embeddings = OpenAIEmbeddings()

    try:
        db = FAISS.load_local(content_name, embeddings, content_name)
    except:
        db = FAISS.from_documents(docs, embeddings)
        db.save_local(content_name, content_name)

    retriever = db.as_retriever()

    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4"),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

    result = chain({"query": query})

    final_result = {
        "query": query,
        "result": result["result"],
        "source_documents": [dict(tmp) for tmp in result["source_documents"]],
    }

    return final_result
