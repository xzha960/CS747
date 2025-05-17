import fitz  # PyMuPDF
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document

import os


def extract_paragraphs_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    paragraphs = []
    for page in doc:
        text = page.get_text()
        for para in text.split('\n\n'):
            clean_para = para.strip().replace('\n', ' ')
            if len(clean_para) > 50:  #
                paragraphs.append(clean_para)
    return paragraphs


os.environ["OPENAI_API_KEY"] = ""

def build_faiss_index(paragraphs):
    docs = [Document(page_content=p) for p in paragraphs]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("how_people_learn_index")
    return vectorstore

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def build_rag_chain():
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("how_people_learn_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(temperature=0.5, model_name="gpt-4.1-nano")
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return chain

def ask_rag(query):
    chain = build_rag_chain()
    result = chain({"query": query})
    return result["result"]


def ask_rag_with_question(query):
    chain = build_rag_chain()
    result = chain({"query": query})
    return result["result"], result["source_documents"]


def set_up():
    pdf_path = "How People Learn.pdf"
    paras = extract_paragraphs_from_pdf(pdf_path)
    print(f"共提取段落数: {len(paras)}")

    build_faiss_index(paras)    

if __name__ == "__main__":
    set_up()
    query = "Why do learners form persistent misconceptions according to cognitive psychology?"
    print("RAG回答：")
    print(ask_rag(query))
