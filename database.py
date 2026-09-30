from sqlite3 import Cursor, Connection , connect


db = connect('db.db')
cursor = Cursor(db)
#cursor.execute("""DROP TABLE if EXISTS clientes""")

# TABELA DE CLIENTES

cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULl,
    email VARCHAR(50) NOT NULL,
    telefone VARCHAR(14) NOT NULL,
    data_nascimento VARCHAR(12),
    ativo BOOLEAN DEFAULT TRUE 
    )""")

# TABELA DE BARBEIROS
cursor.execute("""CREATE TABLE IF NOT EXISTS barbeiros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULl,
    ativo BOOLEAN DEFAULT TRUE 
    )""")


# TABELA DE AGENDAMENTOS

#cursor.execute("DROP TABLE IF EXISTS agendamentos")


cursor.execute("""CREATE TABLE IF NOT EXISTS agendamentos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER FOREING KEY NOT NULL,
    barbeiro_id INTEGER FOREING KEY NOT NULL,
    servico INTEGER NOT NULL,
    data_hora_inicio VARCHAR(20) NOT NULL,
    data_hora_fim VARCHAR(20) NOT NULL,
    status VARCHAR(20)
    )""")

# TABELA DE SERVIÇOS

cursor.execute("""CREATE TABLE IF NOT EXISTS servicos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULl,
    duracao_minutos INTEGER NOT NULL,
    preco REAL NOT NULL
    )""")

# TABELA DE HORÁRIOS

cursor.execute("""CREATE TABLE IF NOT EXISTS horarios_trabalho(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barbeiro_id INTEGER FOREING KEY NOT NULL,
    dia_semana VARCHAR(10) NOT NULL,
    hora_inicio VARCHAR(5) NOT NULL,
    hora_fim VARCHAR(5) NOT NULL
    )""")




# TABELA DE BLOQUEIOS

cursor.execute("""CREATE TABLE IF NOT EXISTS bloqueios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barbeiro_id INTEGER FOREING KEY NOT NULL,
    data_hora_inicio VARCHAR(20) NOT NULL,
    data_hora_fim VARCHAR(20) NOT NULL
    )""")


# ÁREA DE TESTES
if __name__ == "__main__":
    # cursor.execute("""SELECT id, barbeiro_id, hora_inicio, hora_fim FROM horarios_trabalho WHERE dia_semana = (?)""", ('segunda',))
    # dados_horarios = cursor.fetchall()
    # horarios = {}

    # for id, barbeiro_id, hora_inicio, hora_fim in dados_horarios:
    #     horarios[id] = (barbeiro_id, hora_inicio, hora_fim)

    # print(horarios)
    from datetime import datetime, timedelta

    cursor.execute("""SELECT id, duracao_minutos FROM servicos""")
    dados_servico = cursor.fetchall()
    servicos = {}
    for id, duracao_minutos in dados_servico:
        servicos[id] = duracao_minutos

    cursor.execute("""SELECT hora_inicio, hora_fim FROM horarios_trabalho WHERE dia_semana = (?) AND barbeiro_id = (?)""", ('segunda',1,))
    dados_horarios = cursor.fetchall()

    hora_inicio, hora_fim = dados_horarios[0]
    
    cursor.execute("""SELECT * FROM agendamentos 
    WHERE data_hora_inicio LIKE ?  AND barbeiro_id = ?""",(f'07/09/2026%',1,))
    dados_agendamentos = cursor.fetchall()

    agendamentos = {}

    for id, id_cliente, id_barbeiro, servico, data_hora_inicio, data_hora_final, status in dados_agendamentos:
        agendamentos[id] = {'Id do Barbeiro': id_barbeiro,'Id do Cliente': id_cliente,'Serviço': servico,'Data': datetime.strptime(data_hora_inicio, "%d/%m/%Y %H:%M"),'Fim': datetime.strptime(data_hora_final, "%d/%m/%Y %H:%M"),'Status': status}          

    inicio_janela = datetime.strptime(f'07/09/2026 {hora_inicio}',"%d/%m/%Y %H:%M")
    fim_janela = datetime.strptime(f'07/09/2026 {hora_fim}',"%d/%m/%Y %H:%M")
    duracao_servico = servicos[1]
    duracao_servico = timedelta(minutes=int(duracao_servico))

    horarios_possiveis = []
    horario_atual = inicio_janela
    marcados = []

    for cortes in agendamentos:
        marcados.append(agendamentos[cortes]['Data'].strftime("%d/%m/%Y %H:%M"))

    while True:
        if horario_atual >= fim_janela: 
            break
        elif len(marcados) > 0:
            for hora in marcados:
                hora = datetime.strptime(f'{hora}',"%d/%m/%Y %H:%M")
                #print(f'{horario_atual} - {hora} -> {horario_atual - hora} --- {timedelta(days=0, hours=0, minutes=30)}\n')
                if hora == horario_atual or horario_atual - hora <= timedelta(days=0, hours=0, minutes=25):
                    
                    horario_atual += duracao_servico
                    break
                elif horario_atual.strftime("%d/%m/%Y %H:%M") not in horarios_possiveis and horario_atual.strftime("%d/%m/%Y %H:%M") not in marcados:  
                    horarios_possiveis.append(horario_atual.strftime("%d/%m/%Y %H:%M"))


                horario_atual += duracao_servico
        else:  
            horarios_possiveis.append(horario_atual.strftime("%d/%m/%Y %H:%M"))
            horario_atual += duracao_servico
        

    for hr in horarios_possiveis:
        print(hr)
  