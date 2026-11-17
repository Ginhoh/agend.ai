
from dotenv import load_dotenv  
from langchain_groq.chat_models import ChatGroq
from langchain.agents import create_agent
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
from datetime import datetime

# Memória
import asyncio
from pathlib import Path
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

load_dotenv()

CHECKPOINT_DB = str(Path(__file__).resolve().parent / "checkpoints.db")

with open('agent/system_prompt.md', 'r', encoding='utf-8') as file:
    PROMPT = file.read()

async def main(command):
    @tool
    def get_data():
         """Quando precisar consultar a data atual, utilize essa função. 
         Será muito comum em casos que o usuário não informar o ano, ou quando ele informar o dia da semana.
         Apenas neste caso estará no formato YYYY-MM-DD"""

         return datetime.today()




    client = MultiServerMCPClient({
            'agend.ai': {
                'command': 'python',
                'args': ['server.py'],
                'transport': 'stdio',
            }
        })

    tools = await client.get_tools()
    tools.append(get_data)
    async with AsyncSqliteSaver.from_conn_string(CHECKPOINT_DB) as checkpointer: 
        agente = create_agent(
            ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite'),
            name="Age Assistant",
            system_prompt=PROMPT,
            tools = tools,
            checkpointer=checkpointer
        )

        async def chat(mensagem: str) -> str:
            resposta = await agente.ainvoke(
                { 'messages': [{'role': 'user', 'content': mensagem}]}, #Executar de manera assíncrona
                {'configurable': {'thread_id': 'teste:agenda-1'}}, # configuração exigida para manter contexto
            )
            resultado = resposta['messages'][-1].content

            if isinstance(resultado, list):
                return resultado[0]['text']
            else:
                return resultado

        return await chat(command) # Executar de manera assíncrona
    
    # user = await asyncio.to_thread(input, 'USER: ') # Executar de manera assíncrona
    # o to_thread é usado para executar a função input de forma assíncrona, permitindo que o loop continue sem bloquear a execução do programa.


# System template
# Histórico de Conversar
# Memória
# Agente 
# Integração com MCP


# if __name__ == '__main__':
#     asyncio.run(main())