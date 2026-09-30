from sqlite3 import Cursor, Connection
from datetime import date, datetime, timedelta

def dia_semana_data(data:str)->str:
        # Cria uma data (ano, mês, dia) TEM QUE SER DO TIPO INTEIRO
        dia = int(data[:2])
        mes = int(data[3:5])
        ano = int(data[6:])
        d = date(ano, mes, dia)
        # Retorna um número de 0 (segunda) a 6 (domingo)
        numero_dia = d.weekday()
        match numero_dia:
            case 0: return "segunda"
            case 1: return "terca"
            case 2: return "quarta"
            case 3: return "quinta"
            case 4: return "sexta"
            case 5: return "sabado"
            case 6: return "domingo"


def agendamentos_function(mcp):
    # Não pode mudar o horário pelo id do cliente, pode ter conflito com outros agendamentos

    # Configurar padrões do agente para os status
    @mcp.tool() # Arrumar serviços
    def agendar_servico(id_cliente: int, barbeiro_id:int, servico:int, data_hora_inicio:str, data_hora_fim: str)->str:
        """Adiciona um agendamento de serviço na tabela"""

        output = "Não foi possível inserir um novo agendamento"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""INSERT INTO agendamentos
            (id_cliente, barbeiro_id, servico, data_hora_inicio, data_hora_fim, status)
            VALUES (?, ?, ?, ?, ?, 'Confirmado')""", 
            (id_cliente, barbeiro_id, servico, data_hora_inicio, data_hora_fim,))
            db.commit()
            output = "Agendamento inserido com sucesso!"

        except Exception as e:
            return f'ERRO {e}'
        finally:
            db.close()
            return output

    @mcp.tool() 
    def cancelar_agendamento(id:int)->str:
        """Remove um agendamento de serviço na tabela"""

        output = "Não foi possível cancelar o agendamento"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE agendamentos
            SET status = 'Cancelado' WHERE id = (?)""", 
            (id,))
            db.commit()
            output = "Agendamento cancelado com sucesso!"

        except Exception as e:
            return f'ERRO {e}'
        finally:
            db.close()
            return output

    @mcp.tool() 
    def alterar_data_agendamento_pelo_id(id:int, data_hora_inicio: str, data_hora_fim: str)->str:
        """Atualiza o horário de um agendamento pelo id"""

        output = "Não foi possível alterar data do agendamento"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE agendamentos
            SET data_hora_inicio = (?), data_hora_fim = (?) WHERE id = (?)""", 
            (data_hora_inicio,data_hora_fim,id,))
            db.commit()
            output = "Data do agendamento alterada com sucesso!"

        except Exception as e:
            return f'ERRO {e}'
        finally:
            db.close()
            return output

    @mcp.tool()
    def consultar_agendamento(id: int) -> str:
        """Busca os detalhes de um agendamento específico"""
        output = "Não foi possível consultar o agendamento"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""SELECT 
            id_cliente, barbeiro_id, servico, data_hora_inicio, data_hora_fim, status 
            FROM agendamentos WHERE id = (?)""",(id,))
            dados = cursor.fetchall()
            for barbeiro_id, cliente_id, servico, data_inicio, data_final, status in dados:
                output = f"""
Id do Barbeiro: {barbeiro_id}
Id do Cliente: {cliente_id}
Serviço: {servico}
Data: {data_inicio}
Fim: {data_final}
Status: {status}"""
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def listar_agendamento_cliente(id_cliente: int) -> str:
        """Lista agendamentos de um cliente (histórico/futuro)"""
        output = "Não foi possível consultar o agendamento"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""SELECT 
            id_cliente, barbeiro_id, servico, data_hora_inicio, data_hora_fim, status 
            FROM agendamentos WHERE id_cliente = (?)""",(id_cliente,))
            dados = cursor.fetchall()
            for barbeiro_id, cliente_id, servico, data_inicio, data_final, status in dados:
                output = f"""
Id do Barbeiro: {barbeiro_id}
Id do Cliente: {cliente_id}
Serviço: {servico}
Data: {data_inicio}
Fim: {data_final}
Status: {status}"""
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output


    @mcp.tool()
    def listar_agendamento_barbeiro(barbeiro_id: int) -> str:
        """Lista agendamentos de um cliente (histórico/futuro)"""
        output = "Não foi possível consultar o agendamento"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""SELECT 
            id_cliente, barbeiro_id, servico, data_hora_inicio, data_hora_fim, status 
            FROM agendamentos WHERE barbeiro_id = (?)""",(barbeiro_id,))
            dados = cursor.fetchall()
            for barbeiro_id, cliente_id, servico, data_inicio, data_final, status in dados:
                output = f"""
Id do Barbeiro: {barbeiro_id}
Id do Cliente: {cliente_id}
Serviço: {servico}
Data: {data_inicio}
Fim: {data_final}
Status: {status}"""
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def concluir_agendamento(id: int) -> str:
        """Marca o agendamento como concluído depois que o atendimento realmente aconteceu"""
        output = "Não foi possível concluir o agendamento"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE agendamentos 
            SET status = 'Concluido'
            WHERE id = (?)""",(id,))
            db.commit()
            output = "Agendamento concluido!"
            
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def marcar_no_show(id: int) -> str:
        """Marca o agendamento (pelo id) como que o cliente não apareceu"""
        output = "Não foi possível atuializar o agendamento"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE agendamentos 
            SET status = 'Faltante'
            WHERE id = (?)""",(id,))
            db.commit()
            output = "Agendamento atualizado!"
            
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def agendamentos_disponiveis_dia_por_barbeiro(barbeiro_id: int,data: str) -> list:
        """Consulta datas disponíveis de APENAS UM BARBEIRO em um determinado dia. Formato da data: DD/MM/YYYY"""
        horarios_possiveis = []

        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""SELECT id, nome, duracao_minutos FROM servicos""")
            dados_servico = cursor.fetchall()
            servicos = {}
            for id, nome, duracao_minutos in dados_servico:
                servicos[id] = (nome,duracao_minutos)

            cursor.execute("""SELECT hora_inicio, hora_fim FROM horarios_trabalho WHERE dia_semana = (?) AND barbeiro_id = (?)""", (dia_semana_data(data),id,))
            dados_horarios = cursor.fetchall()
            hora_inicio, hora_fim = dados_horarios[0]
            cont = 1
            # for id, barbeiro_id, hora_inicio, hora_fim in dados_horarios:
            #     horarios[cont] = (barbeiro_id, hora_inicio, hora_fim)
            #     cont += 1

            cursor.execute("""SELECT * FROM agendamentos 
            WHERE data_hora_inicio LIKE ? AND barbeiro_id = ?""",(f'{data}%',barbeiro_id,))
            dados_agendamentos = cursor.fetchall()

            agendamentos = {}

            for id, id_cliente, id_barbeiro, servico, data_hora_inicio, data_hora_final, status in dados_agendamentos:
                agendamentos[id] = {'Id do Barbeiro': id_barbeiro,'Id do Cliente': id_cliente,'Serviço': servico,'Data': datetime.strptime(data_hora_inicio, "%d/%m/%Y %H:%M"),'Fim': datetime.strptime(data_hora_final, "%d/%m/%Y %H:%M"),'Status': status}          

            inicio_janela = datetime.strptime(f'{data} {hora_inicio}',"%d/%m/%Y %H:%M")
            fim_janela = datetime.strptime(f'{data} {hora_fim}',"%d/%m/%Y %H:%M")
        
            nome_servico, duracao_servico = servicos[1]
            duracao_servico = timedelta(minutes=int(duracao_servico))
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
                        
                        if hora == horario_atual or horario_atual - hora <= timedelta(days=0, hours=0, minutes=25):
                            horario_atual += duracao_servico
                            break
                        elif horario_atual.strftime("%d/%m/%Y %H:%M") not in horarios_possiveis and horario_atual.strftime("%d/%m/%Y %H:%M") not in marcados:  
                            horarios_possiveis.append(horario_atual.strftime("%d/%m/%Y %H:%M"))

                        horario_atual += duracao_servico
                else:  
                    horarios_possiveis.append(horario_atual.strftime("%d/%m/%Y %H:%M"))
                    horario_atual += duracao_servico
        
        
            # for horarios in horarios_possiveis:
            #     print(horarios)


        except Exception as e:
            return f"ERRO: {e}"
        
        finally:
            db.close()
            return horarios_possiveis

    @mcp.tool()
    def listar_agendamentos_dia(data: str):
        """Lista serviços agendados em um determinado dia."""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)


            cursor.execute("""SELECT * FROM agendamentos 
            WHERE data_hora_inicio LIKE ?""",(f'{data}%',))
            dados_agendamentos = cursor.fetchall()

            agendamentos = {}

            for id, id_cliente, barbeiro_id, servico, data_hora_inicio, data_hora_final, status in dados_agendamentos:
                agendamentos[id] = {'Id do Barbeiro': barbeiro_id,'Id do Cliente': id_cliente,'Serviço': servico,'Data': datetime.strptime(data_hora_inicio, "%d/%m/%Y %H:%M"),'Fim': datetime.strptime(data_hora_final, "%d/%m/%Y %H:%M"),'Status': status}          



        except Exception as e:
            return f"ERRO: {e}"
        
        finally:
            db.close()
            return agendamentos

        