from usuario import Usuario
from mensagem import Mensagem
from conexao import Conexao
from contato import Contatos




class Chat:
    def __init__(self, nome_usuario: str, telefone_usuario: str):
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario

    def enviar_mensagem(self, conteudo:str,destinatario: Contatos) -> bool:

        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        sql = f"INSERT INTO tb_mensagem (tel_remetente,mensagem, tel_destinatario) VALUES ('{self.telefone_usuario}', '{conteudo}', '{destinatario.telefone}')"
        mycursor.execute(sql)

        mydb.commit()
        
        return True
    
    def verificar_mensagem(self,quantidade: int, destinatario: Contatos): 

        mydb = Conexao.conectar()

        mycursor = mydb.cursor()


        sql = f"SELECT nome, mensagem FROM tb_mensagem m "\
        f"INNER JOIN tb_usuario u " \
        f"ON m.tel_remetente = u.tel " \
        f"WHERE m.tel_remetente = '{self.telefone_usuario}' " \
        f"AND m.tel_destinatario = '{destinatario.telefone}' " \
        f"OR m.tel_remetente = '{destinatario.telefone}' " \
        f"AND m.tel_destinatario = '{self.telefone_usuario}' \
          ORDER BY m.id_mensagem""" 
        

        mycursor.execute(sql)
        resultado = mycursor.fetchall()
        mycursor.close()

        lista_mensagens = []

        for linha in resultado:

            mensagem =  {"nome":linha[0],"mensagem":linha[1]}
            lista_mensagens.append(mensagem)

            # lista_mensagens.append(Mensagem(linha[0],linha[1]))

        return (lista_mensagens)
  
    def retornar_contatos(self):
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()


        sql = f"SELECT nome,tel FROM tb_usuario order by nome"
        mycursor.execute(sql)
        resultado = mycursor.fetchall()

        lista_contatos = []
        lista_contatos.append({"nome":"TODOS","telefone": ""})

        for linha in resultado:

            contato = {"nome":linha[0],"telefone":linha[1]}
            lista_contatos.append(contato)


        return(lista_contatos)