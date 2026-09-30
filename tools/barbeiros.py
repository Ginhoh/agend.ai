from sqlite3 import Cursor, Connection

def barbeiros_function(mcp):
    
    @mcp.tool()
    def listar_barbeiros()-> dict:
        """Essa função retorna todos os dados da parte de barbeiros"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("SELECT id, nome, ativo FROM barbeiros")
            dados = cursor.fetchall()
            output = {}
            for id, nome, ativo in dados:
                output[id] = f"{nome} | {"Ativo" if ativo == 1 else "Inativo"}"

        except Exception as e:
            return f"ERRO: {e}"

        finally:
            db.close()

        return output

    @mcp.tool()
    def adicionar_barbeiro(nome: str) -> str:
        """Adicionar um novo barbeiro"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)
            cursor.execute("INSERT INTO barbeiros (nome) VALUES (?)", (nome.title(),))

            db.commit()

        except Exception as e:
                    return f"ERRO: {e}"

        finally:
            db.close()

        return "Barbeiro inserido com sucesso!"

    @mcp.tool()
    def buscar_barbeiro_pelo_id(id: int) -> str:
        """Pesquisar por um barbeiro pelo seu id"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute(f"SELECT id, nome, ativo FROM barbeiros WHERE id = (?)",(id,))
            data = cursor.fetchall()
            output = "Barbeiro não encontrado"
            for id, nome, ativo in data:
                output = f'{id}. {nome} | {"Ativo" if ativo == 1 else "Inativo"}'
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def buscar_barbeiro_pelo_nome(nome: str) -> str:
        """Essa função busca um barbeiro pelo nome"""
        output = "Nome não encontrado"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute(f"SELECT id, nome, ativo FROM barbeiros WHERE nome = (?)",(nome.title(),))
            data = cursor.fetchall()
            for id, nome_b, ativo in data:
                output = f'{id}. {nome_b} | {"Ativo" if ativo == 1 else "Inativo"}'
        except TypeError as e:
            return (f"ERRO: {e}")
        finally:
            db.close()
            return output

    @mcp.tool()
    def desativar_barbeiro(id: int) -> str:
        """Desativar um barbeiro pelo seu id"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute(f"UPDATE barbeiros SET ativo = 0 WHERE id = (?)",(id,))
            db.commit()
            output = f'Barbeiro com id {id} desativado com sucesso!'

        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def ativar_barbeiro(id: int) -> str:
        """Essa função sativa um barbeiro pelo seu id"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("UPDATE barbeiros SET ativo = 1 WHERE id = (?)",(id,))
            db.commit()
            output = f'Barbeiro com id {id} ativado com sucesso!'

        except Exception as e:
                    return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def remover_barbeiro(id: int) -> str:
        """Essa função exclui um barbeiro pelo id"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("DELETE FROM barbeiros WHERE id = (?)",(id,))
            output = "Barbeiro excluido com sucesso!"
            db.commit()
        except TypeError as e:
            return (f"ERRO: {e}")
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_nome_barbeiro_pelo_id(id: int, name:str)->str:
        """Altera o nome do barbeiro pelo id"""
        output = "Não foi possível alterar o nome do barbeiro"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE barbeiros SET nome = (?) WHERE id = (?)""",(name, id))
            output = "Nome do barbeiro alterado!"
            db.commit()
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output