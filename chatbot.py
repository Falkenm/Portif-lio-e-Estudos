from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import os 
from dotenv import load_dotenv

load_dotenv("key.env") # Aqui tem que estar o .env com a chave da Groq

print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))

template = """ 
Você é um assistente virtual.
Responda apenas em Potuguês Brasileiro.

Input: {input}
"""

base_prompt = PromptTemplate(input_variables=["input"],
                             template=template)

llm = ChatGroq(model_name="llama3-8b-8192")
memory = ConversationBufferMemory(memory_key="chat_history", input_key='input')

llm_chain = LLMChain(llm=llm, prompt=base_prompt, memory=memory)

os.system("clear")

while True:
    user_input = input("Você: ")
    if user_input.lower() in ["sair", "exit", "quit"]:
        print("Encerrando o chatbot.")
        break
    resposta = llm_chain.run(input=user_input)
    print("Assistente:", resposta)