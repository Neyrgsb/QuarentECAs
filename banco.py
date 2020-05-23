# guardar entregador(cpf), email, nome do cliente, data, status
# mandar emails 
  
import sqlite3

avisos = []

id = 1
CPF_c = 123
CPF_e = 321
nome_e = "evanilson"
nome_c = "jorge"
email_c = "kkk"
data = 22
cliente = 2
telefone = 99999999

conn = sqlite3.connect('covid.db')
cursor = conn.cursor()
####
cursor.execute("""
CREATE TABLE IF NOT EXISTS entregadores (
        cpf INTEGER PRIMARY KEY,
        nome TEXT
);
""")

cursor.execute("""
INSERT INTO entregador (cpf,nome)
VALUES (?,?)
""", (CPF_e, nome_e))
conn.commit()
#
####
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        telefone
);
""")

cursor.execute("""
INSERT INTO cliente (nome,email,telefone)
VALUES (?,?,?)
""", (nome_c,email_c,telefone))
conn.commit()
#
#####
cursor.execute("""
CREATE TABLE IF NOT EXISTS entregas (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        data INTEGER,
        cpf_entregador INTEGER,
        email_cliente TEXT
);
""")

cursor.execute("""
INSERT INTO entregas (data)
VALUES (?)
""", (data,cpf_e,email_c))
conn.commit()



def checar_cliente(cliente):
    """
    Procura cliente no banco de dados. Caso o cliente ja esteja cadastrado nada acontece.
    Input: entregador = dicionario com todos os dados do cliente
    Output: id_cliente
    """
    email = cursor.execute("""
    SELECT nome
    FROM clientes
    WHERE cpf=(?);
    """,(cliente[1],)).fetchall()

    if email == []:
        id_cliente = adicionar_clientes(cliente)
        return id_cliente
    else:
        return email
        

def checar_entregador(entregador):
    """
    Procura entregador no banco de dados. Caso o entregador ja esteja cadastrado nada acontece.
    Input: entregador = dicionario com todos os dados do entregador
    Output: id_entregador
    """
    cpf = cursor.execute("""
    SELECT cpf
    FROM entregadores
    WHERE cpf=(?);
    """,(entregador[1],)).fetchall()

    if cpf == []:
        id_entregador = adicionar_entregador(entregador)
        return id_entregador
    else:
        return cpf 
        

def adicionar_clientes(cliente):
    """
    Adiciona cadastro do novo cliente ao banco.
    """
    cursor.execute("""
    INSERT INTO cliente (nome,email,telefone)
    VALUES (?,?,?)
    """, (cliente[0],cliente[1],cliente[2]))
    conn.commit()
    return cliente[1]


def adicionar_entregador(entregador):
    """
    Adiciona cadastro do novo entregador ao banco.
    """
    cursor.execute("""
    INSERT INTO entregador (cpf,nome)
    VALUES (?,?)
    """, (entregador[1], entregador[0]))
    conn.commit()
    return entregador[1]


def adicionar_pedido(pedido):
    """
    Adiciona dados do novo pedido.
    """
    id_cliente = checar_cliente(pedido[cliente]) 
    id_entregador = checar_entregador(pedido[entregador])   

    cursor.execute("""
    INSERT INTO entregas (data)
    VALUES (?)
    """, (pedido,id_entregador,id_cliente))
    conn.commit()

    


def limpar_pedidos_antigos(data):
    """
    Apaga do banco registros de pedidos feitos a mais de 15.
    Input: data = dia de hoje
    """
    pass


def buscar_clientes_contaminados(cpf_entregador):
    """
    Busca dados de clientes expostos a entregadores possivelmente contaminados.
    Input: id_entregador
    Output: clientes = lista com todos os clientes expostos 
    """

    l_data = cursor.execute("""
    SELECT data
    FROM entregas
    WHERE cpf=(?);
    """,(cpf_entregador)).fetchall()

    l_email = cursor.execute("""
    SELECT email
    FROM entregas
    WHERE cpf=(?);
    """,(cpf_entregador)).fetchall()

    for i in l_email:
        l_dados = cursor.execute("""
        SELECT *
        FROM clientes
        WHERE cpf=(?);
        """,(cpf_entregador)).fetchall()

    for i in len(l_email):
        avisos.append([l_data[i],l_dados[i][1],l_dados[i][2]])




    print(avisos)
