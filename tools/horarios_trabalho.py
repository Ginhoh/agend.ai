from sqlite3 import Cursor, Connection

def horarios_trabalho_function(mcp):
    """
    ATENÇÃO: é recomendável que não faça alteraçoes do barbeiro_id, caso precise fazer uma alteração, crie um novo dado e exclua o anterior.
    """

    @mcp.tool()
    def adicionar_horario_trabalho(barbeiro_id: int,dia_semana:str, hora_inicio : str, hora_fim: str)->str:
        """Cria um novo horário de trabalho"""
        output = "Não foi possível criar o horário de trabalho, tente novamente!"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""INSERT INTO horarios_trabalho (barbeiro_id, dia_semana, hora_inicio, hora_fim)
            VALUES (?, ?, ?, ?)""",(barbeiro_id, dia_semana.lower(), hora_inicio, hora_fim,))
            output = "Horário adicionado!"
            db.commit()
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def remover_horario_trabalho_pelo_id(id)->str:
        """Remove horário de trabalho pelo id do horário"""
        output = 'Não foi possível remover.'
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""DELETE FROM horarios_trabalho WHERE id = (?)""",(id,))

            db.commit()
            output = "Horário de Trabalho removido com sucesso!"
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def listar_horarios_trabalho()->dict:
        """Exibe todos horários de trabalho"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""SELECT *
            FROM horarios_trabalho""")
            dados = cursor.fetchall()
            output = {}
            for id, barbeiro_id, dia_semana, hora_inicio, hora_fim in dados:
                output[id] = f"Código barbeiro: {barbeiro_id} | {dia_semana} | {hora_inicio} -> {hora_fim}"
            
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output


    @mcp.tool()
    def alterar_hora_inicio_pelo_id(id: int, hora_inicio:str)->str:
        """Altera hora de início do barbeiro pelo id do horário"""
        output = "Não foi possível alterar o horário inicial"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE horarios_trabalho SET hora_inicio = (?) WHERE id = (?)""",(hora_inicio, id))
            output = "Horário de início alterado!"
            db.commit()
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_hora_final_pelo_id(id: int, hora_final:str)->str:
            """Altera hora de término do barbeiro pelo id do horário"""
            output = "Não foi possível alterar o horário final"
            try:
                db = Connection('db.db')
                cursor = Cursor(db)
    
                cursor.execute("""UPDATE horarios_trabalho SET hora_fim = (?) WHERE id = (?)""",(hora_final, id))
                output = "Horário de término alterado!"
                db.commit()
                
            except Exception as e:
                return f"ERRO: {e}"
            finally:
                db.close()
                return output

   