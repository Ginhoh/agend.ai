
from dotenv import load_dotenv  # type: ignore[reportMissingImport
from langchain_groq.chat_models import ChatGroq
from langchain.agents import create_agent
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
load_dotenv()

with open('agent/system_prompt.md', 'r', encoding='utf-8') as file:
    PROMPT = file.read()



agente = create_agent(
    ChatGoogleGenerativeAI(model='gemini-2.5-flash'),
    name="Age Assistant",
    system_prompt=PROMPT
)

mensagem = agente.invoke({"role": 'user', 'messages':"O que você pode fazer?"})
print(mensagem['messages'][-1].content)


# System template
# Histórico de Conversar
# Memória
# Agente 
# Integração com MCP