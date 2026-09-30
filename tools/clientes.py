from sqlite3 import Connection, Cursor

def clientes_functions(mcp):
    @mcp.tool()
    def buscar_cliente_pelo_id(id: int) -> str:
        """Buscar um cliente pelo seu id"""
        output = "Cliente não encontrado"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute(f"SELECT nome, email, telefone, ativo FROM clientes WHERE id = {id}")
            data = cursor.fetchall()
            for nome, email, telefone, ativo in data:
                output = f'{nome} ({email}), {telefone} [{ativo}]'
        except Exception as e:
                    return f"ERRO: {e}"
        finally:
            db.close()
            return output
        
    @mcp.tool()
    def buscar_cliente_pelo_nome(nome: str) -> str:
        """Busca um cliente pelo seu nome"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            output = "Nome não encontrado"
            cursor.execute(f"SELECT id, nome, email, telefone, data_nascimento, ativo FROM clientes WHERE nome LIKE '%{nome.title()}%'")
            data = cursor.fetchall()
            for id, nome_c, email, telefone, data_nascimento, ativo in data:
                output = f'{id}. {nome_c} | {email} | tel: {telefone} | data de nascimento: {data_nascimento} | Ativo: {bool(ativo)}'
        except Exception as e:
                    return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def buscar_cliente_pelo_email(email: str) -> str:
        """Essa ferramenta busca por um cadastro através de um email"""
        try:
                db = Connection('db.db')
                cursor = Cursor(db)
        
                cursor.execute(f"SELECT email, telefone, nome FROM clientes WHERE email = '{email.lower()}'")
                data = cursor.fetchall()
                output = "Nome não encontrado"
                for email, telefone, nome in data:
                    output = f'{nome} ({email}), {telefone}'
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def listar_clientes()-> dict:
        """Listar todos os clientes cadastrados"""
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("SELECT id, nome, email, telefone, data_nascimento, ativo FROM clientes")
            dados = cursor.fetchall()
            output = {}
            for id, nome, email, telefone, data_nascimento, ativo in dados:
                output[id] = [nome, email, telefone, data_nascimento, ativo]

        except Exception as e:
            return f"ERRO: {e}"

        finally:
            db.close()

        return output


    @mcp.tool()
    def adicionar_cliente(nome: str, email: str, telefone:str, data_nascimento:str) -> str:
        """"
        Cadastrar um novo cliete
        """
        try:
            db = Connection('db.db')
            cursor = Cursor(db)
            cursor.execute(f"""INSERT INTO clientes (nome, email, telefone, data_nascimento) VALUES (?, ?, ?, ?)""",(nome.title(), email.lower(), telefone, data_nascimento))

            db.commit()

        except Exception as e:
            return f"ERRO: {e}"

        finally:
            db.close()

        return "Dado inserido com sucesso!"

    @mcp.tool()
    def remover_cliente_pelo_id(id:int)->str:

        """Remove cliente pelo id"""
        output = "Não foi possível remover o cliente!"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("DELETE FROM clientes WHERE id = (?)",(id,))
            output = "Cliente removido com sucesso!"
            db.commit()
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_nome_cliente_pelo_id(id: int, nome:str)->str:
        """Altera o nome do cliente pelo id"""
        output = "Não foi possível alterar o nome do cliente"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE clientes SET nome = (?) WHERE id = (?)""",(nome, id))
            output = "Nome do cliente alterado!"
            db.commit()

        except Exception as e:
            return f"ERRO: {e}"
        
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_email_cliente_pelo_id(id: int, email:str)->str:
        """Altera o email do cliente pelo id"""
        output = "Não foi possível alterar o email do cliente"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE clientes SET email = (?) WHERE id = (?)""",(email, id))
            output = "email do cliente alterado!"
            db.commit()

        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_numero_cliente_pelo_id(id: int, telefone:str)->str:
        """Altera o phone do cliente pelo id"""
        output = "Não foi possível alterar o telefone do cliente"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE clientes SET telefone = (?) WHERE id = (?)""",(telefone))
            output = "Telefone do cliente alterado!"
            db.commit()
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output

    @mcp.tool()
    def alterar_aniversario_pelo_id_(id: int, data:str)->str:
        """Altera o nome do cliente pelo id"""
        
        output = "Não foi possível alterar a data de nascimento do cliente"
        try:
            db = Connection('db.db')
            cursor = Cursor(db)

            cursor.execute("""UPDATE clientes SET data_nascimento = (?) WHERE id = (?)""",(data, id))
            output = "Data de nascimento do cliente alterado!"
            db.commit()
        except Exception as e:
            return f"ERRO: {e}"
        finally:
            db.close()
            return output