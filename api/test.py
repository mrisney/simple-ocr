# insert an openai key below parameter
import os
os.environ["OPENAI_API_KEY"] = "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"

# load the LLM model
from langchain.chat_models import ChatOpenAI
model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=model_name)

# Using q&a chain to get the answer for our query
from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(llm, chain_type="stuff",verbose=True)

# write your query and perform similarity search to generate an answer
query = "What are the emotional benefits of owning a pet?"
matching_docs = db.similarity_search(query)
answer =  chain.run(input_documents=matching_docs, question=query)
print(answer)