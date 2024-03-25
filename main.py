import getpass
import os

os.environ["OPENAI_API_KEY"] = "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"

from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_core.prompts import PromptTemplate

from langchain_community.document_loaders import TextLoader

loader = TextLoader("/Users/ameya/PycharmProjects/pythonProject2/venv/info.txt")
docs = loader.load()

# splits the text into chunks for openai
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

# index the data
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# use similarity to search through data
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# connect to OpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Don't answer if it is not pertaining to the information given to you.
Use three sentences maximum and keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""
custom_rag_prompt = PromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

def query(question):
    total = ""
    for chunk in rag_chain.stream(question):
        total += chunk
    return total

