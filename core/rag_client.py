# core/rag_client.py
import os
from typing import Optional

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA


class RAGClient:
    """
    RAG fallback client using Ollama embeddings + ChatOllama LLM.
    No OpenAI API key and no FAISS required.
    Only uses Chroma vector store.
    """

    def __init__(
        self,
        vector_store_path: Optional[str] = "vectorstore",
        top_k: int = 3,
        embedding_model_name: str = "llama3.2:3b",
        llm_model_name: str = "llama3.2:3b",
    ):
        self.vector_store_path = vector_store_path
        self.top_k = top_k

        # Initialize LLM
        self.llm = ChatOllama(model=llm_model_name, temperature=0.0)

        # Initialize Ollama embeddings
        self.embeddings = OllamaEmbeddings(model=embedding_model_name)

        # Only use Chroma (no FAISS needed)
        if os.path.exists(vector_store_path):
            self.vstore = Chroma(
                persist_directory=vector_store_path,
                embedding_function=self.embeddings,
            )
        else:
            # Create a minimal store with a placeholder doc
            self.vstore = Chroma(
                persist_directory=vector_store_path,
                embedding_function=self.embeddings,
            )
            self.vstore.add_texts(["Temporary placeholder document for RAG."])

        # Create retriever
        self.retriever = self.vstore.as_retriever(search_kwargs={"k": top_k})

        # Create RAG QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=False,
        )

    def ask(self, question: str) -> str:
        if not question.strip():
            return "No question provided."

        try:
            answer = self.qa_chain.run(question)
            if not answer or not answer.strip():
                return "I could not find a relevant answer in the documents."
            return answer
        except Exception as e:
            return f"RAG system error: {e}"


def rag_answer(question: str, top_k: int = 3) -> str:
    """
    Wrapper for app.py
    """
    client = RAGClient(top_k=top_k)
    return client.ask(question)
