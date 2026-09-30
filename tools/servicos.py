from sqlite3 import Connection, Cursor


def servicos_function(mcp):
    """Caso deseje alterar o nome, adicione um novo serviço"""
    @mcp.tool()
    def adicionar_servico(nome: str, duracao_minutos: int, preco: float )-> str:
        """Adiciona um novo serviço"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor = db.cursor()    
            cursor.execute("INSERT INTO servicos (nome, duracao_minutos, preco) VALUES (?, ?, ?)",(nome, duracao_minutos, preco))
            db.commit()
            return "Serviço inserido com sucesso!"
        except Exception as e:
            return f'ERRO: {e}'
        finally:
            db.close()

    @mcp.tool()
    def buscar_servico_pelo_nome(nome: str)-> str:
        """Busca o serviço pelo seu nome"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("SELECT id, nome, duracao_minutos, preco FROM servicos WHERE nome LIKE '%(?)%'",(nome.title()))
            data = cursor.fetchall()
            output = "Nome não encontrado"
            for id, nome_servico, duracao, preco in data:
                output = f'{id}. {nome_servico} | {duracao}min | R${preco:.2f}'
        except TypeError as e:
            return (f"ERRO: {e}")
        finally:
            db.close()
            return output

    @mcp.tool()
    def pesquisar_servico_pelo_id(id: str)-> str:
            """Essa função retorna um dado da query"""
            try:
                db = Connection('db.db')
                cursor = Cursor(db)
    
                cursor.execute("SELECT id, nome, duracao_minutos, preco FROM servicos WHERE id = (?)",(id,))
                data = cursor.fetchall()
                output = "id não encontrado"
                for id, nome_servico, duracao, preco in data:
                    output = f'{id}. {nome_servico} | {duracao}min | R${preco:.2f}'

            except Exception as e:
                return f"ERRO: {e}"
            
            finally:
                db.close()
                return output

    @mcp.tool()
    def alterar_preco_servico_pelo_id(preco: float, id:int)->str:
        """Alterar o preço do serviço pesquisando pelo seu nome"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("UPDATE servicos SET preco = (?) WHERE id = (?)",(preco, id,))
            output = f"Preço alterado para R${preco:.2f}"
            db.commit()
        except Exception as e:
            return (f"ERRO: {e}")
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_duracao_servico(duracao: int, id:int)->str:
        """Essa função altera a duração do servico"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("UPDATE servicos SET duracao_minutos = (?) WHERE id = (?)",(duracao, id,))
            output = f"Duração alterada para {duracao} min"
            db.commit()
        except Exception as e:
            return (f"ERRO: {e}")
        finally:
            db.close()
            return output

    @mcp.tool()
    def listar_servicos()->dict:
        """Essa função retorna todos os serviços cadastrados"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("SELECT id, nome, duracao_minutos, preco FROM servicos")
            data = cursor.fetchall()
            output = {}
            for id, nome_servico, duracao, preco in data:
                output[id] = f'{nome_servico} | {duracao}min | R${preco:.2f}'
        except Exception as e:
            return (f"ERRO: {e}")
        finally:
            db.close()
            return output

    @mcp.tool()
    def remover_servico_pelo_id(id:int)->str:
        """Essa função deleta um serviço pelo id"""
        
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("DELETE FROM servicos WHERE id = (?)",(id,))
            output = "Serviço removido com sucesso!"
            
            db.commit()

        except Exception as e:
            return (f"ERRO: {e}")
        finally:
            db.close()
            return output
