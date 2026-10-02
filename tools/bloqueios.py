from sqlite3 import Connection, Cursor

def bloqueios_functions(mcp):
    @mcp.tool()
    def buscar_bloqueio_pelo_id(id: int) -> str:
        """Buscar um bloqueio pelo seu id"""
        output = "Bloqueio não encontrado"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute(f"SELECT nome, barbeiro_id, data_hora_inicio, data_hora_fim FROM bloqueios WHERE id = {id}")
            data = cursor.fetchall()
            for nome, barbeiro_id, data_hora_inicio, data_hora_fim in data:
                output = f'Nome: {nome} Barbeiro ID: {barbeiro_id} {data_hora_inicio}-> {data_hora_fim}'
        except Exception as e:
                    return f"ERRO: {e}"
        finally:
            db.close()
            return output
        
    @mcp.tool()
    def buscar_bloqueio_pelo_nome(nome: str) -> str:
        """Busca um bloqueio pelo seu nome"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            output = "Bloqueio não encontrado"
            cursor.execute(f"SELECT nome, barbeiro_id, data_hora_inicio, data_hora_fim FROM bloqueios WHERE nome LIKE '%{nome.title()}%'")
            data = cursor.fetchall()
            for nome, barbeiro_id, data_hora_inicio, data_hora_fim in data:
                    output = f'Nome: {nome} Barbeiro ID: {barbeiro_id} {data_hora_inicio}-> {data_hora_fim}'
        except Exception as e:
                    return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def buscar_bloquei_pelo_barbeiro_id(barbeiro_id: str) -> str:
        """Essa ferramenta busca por um bloqueio através do id do barbeiro"""
        output = "Bloqueio não encontrado"
        try:
                db = Connection('db.db')
                cursor = Cursor(db)
        
                cursor.execute(f"SELECT nome, barbeiro_id, data_hora_inicio, data_hora_fim FROM bloqueios WHERE id = {barbeiro_id}")
                data = cursor.fetchall()
                for nome, barbeiro_id, data_hora_inicio, data_hora_fim in data:
                    output = f'Nome: {nome} Barbeiro ID: {barbeiro_id} {data_hora_inicio}-> {data_hora_fim}'
                    
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def listar_bloqueios()-> dict:
        """Listar todos os bloqueios cadastrados"""
        output = {}
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute(f"SELECT id, nome, barbeiro_id, data_hora_inicio, data_hora_fim FROM bloqueios")
            data = cursor.fetchall()
            for id, nome, barbeiro_id, data_hora_inicio, data_hora_fim in data:
                output[id] = f'Nome: {nome} Barbeiro ID: {barbeiro_id} {data_hora_inicio}-> {data_hora_fim}'

        except Exception as e:
            return f"ERRO: {e}"

        finally:
            db.close()

        return output


    @mcp.tool()
    def adicionar_bloqueio(nome: str, barbeiro_id: int, data_hora_inicio:str, data_hora_fim:str) -> str:
        """"
        Cadastrar um novo bloqueio
        """
        try:
            db = Connection('db.db')
            cursor = Cursor(db)
            cursor.execute(f"""INSERT INTO bloqueios (nome, barbeiro_id, data_hora_inicio, data_hora_fim) VALUES (?, ?, ?, ?)""",(nome.title(), barbeiro_id, data_hora_inicio, data_hora_fim))

            db.commit()
            return "Bloqueio adicionado com sucesso"
        except Exception as e:
            return f"ERRO: {e}"

        finally:
            db.close()

    @mcp.tool()
    def remover_bloqueio_pelo_id(id:int)->str:

        """Remove bloqueio pelo seu id"""
        output = "Não foi possível remover o bloqueio!"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("DELETE FROM bloqueios WHERE id = (?)",(id,))
            output = "Bloqueio removido com sucesso!"
            db.commit()
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_nome_bloqueio_pelo_id(id: int, nome:str)->str:
        """Altera o nome do bloqueio pelo id"""
        output = "Não foi possível alterar o nome do bloqueio"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE bloqueios SET nome = (?) WHERE id = (?)""",(nome, id))
            output = "Nome do bloqueio alterado!"
            db.commit()

        except Exception as e:
            return f"ERRO: {e}"
        
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_horario_bloqueio_pelo_id(id: int, data_hora_inicio:str, data_hora_fim)->str:
        """Altera o horário do bloqueio pelo id"""
        output = "Não foi possível alterar o bloqueio do barbeiro"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE bloqueios SET data_hora_inicio = ?, data_hora_fim 
            WHERE id = ?""",(data_hora_inicio, data_hora_fim, id))
            output = "Bloqueio do barbeiro alterado!"
            db.commit()

        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

   