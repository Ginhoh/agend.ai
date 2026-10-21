
from dotenv import load_dotenv  
from langchain_groq.chat_models import ChatGroq
from langchain.agents import create_agent
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
import asyncio

load_dotenv()

with open('agent/system_prompt.md', 'r', encoding='utf-8') as file:
    PROMPT = file.read()

async def main():
    client = MultiServerMCPClient({
            'agend.ai': {
                'command': 'python',
                'args': ['server.py'],
                'transport': 'stdio',
            }
        })

    tools = await client.get_tools()
    agente = create_agent(
        ChatGoogleGenerativeAI(model='gemini-2.5-flash'),
        name="Age Assistant",
        system_prompt=PROMPT,
        tools = tools,
        checkpointer=InMemorySaver()
    )

    async def chat(mensagem: str) -> str:
        resposta = await agente.ainvoke(
            { 'messages': [{'role': 'user', 'content': mensagem}]}, #Executar de manera assíncrona
            {'configurable': {'thread_id': 'chat-1'}}, # configuração exigida para manter contexto
        )
        resultado = resposta['messages'][-1].content

        if isinstance(resultado, list):
             return resultado[0]['text']
        else:
            return resultado

    while True:
            user = await asyncio.to_thread(input, 'USER: ') # Executar de manera assíncrona
            # o to_thread é usado para executar a função input de forma assíncrona, permitindo que o loop continue sem bloquear a execução do programa.
            if user.strip() == '' or user.strip().lower() == 'sair':
                break
            print(await chat(user)) # Executar de manera assíncrona


# System template
# Histórico de Conversar
# Memória
# Agente 
# Integração com MCP


if __name__ == '__main__':
    asyncio.run(main())