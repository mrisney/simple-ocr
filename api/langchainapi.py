import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Set your OpenAI API key in your environment, not directly in the script
os.environ["OPENAI_API_KEY"] = "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"

# Initialize Langchain components
openai_embeddings = OpenAIEmbeddings()
chroma = Chroma(embedding_model=openai_embeddings)
text_splitter = CharacterTextSplitter()
llm = OpenAI()
chat_model = ChatOpenAI(llm=llm)
retrieval_qa = RetrievalQA(chat_model=chat_model, vectorstore=chroma, text_splitter=text_splitter)

def query_ocr_text(ocr_text, query):
    # Add the OCR text to the vector store
    chroma.add_documents([ocr_text])

    # Perform the query using RetrievalQA
    response = retrieval_qa.ask(query)

    return response

# Example usage
ocr_text = "2651515 Expites 2023 RISNEY, MARC STUART. 1845 Hanscom Drive DOB 11-15- 1967"
query = "What's the birthdate of the registered owner?"
answer = query_ocr_text(ocr_text, query)
print(answer)


