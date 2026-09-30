from mcp.server.fastmcp import FastMCP

from tools.clientes import clientes_functions
from tools.barbeiros import barbeiros_function
from tools.servicos import servicos_function
from tools.horarios_trabalho import horarios_trabalho_function
from tools.agendamentos import agendamentos_function

mcp = FastMCP("Consults db")

# CLIENTES
clientes_functions(mcp=mcp)

# # BARBEIROS
barbeiros_function(mcp=mcp)

 # SERVIÇOS
servicos_function(mcp=mcp)

# HORÁRIOS DE TRABALHO
horarios_trabalho_function(mcp=mcp)

# AGENDAMENTOS
agendamentos_function(mcp=mcp)

if __name__ == "__main__":
    mcp.run()   