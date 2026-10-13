
from dotenv import load_dotenv  # type: ignore[reportMissingImport
from langchain_groq.chat_models import ChatGroq
from langchain.agents import create_agent
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
load_dotenv()

agente = create_agent(
    ChatGoogleGenerativeAI(model='gemini-2.5-flash'),
    name="Age Assistant",
    system_prompt='Você fala apenas 3 palavras em uma frase'
)

mensagem = agente.invoke({"role": 'user', 'messages':"Olá"})
print(mensagem)


# System template
# Histórico de Conversar
# Memória
# Agente 
# Integração com MCP