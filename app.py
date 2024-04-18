from flask import Flask, render_template, request, session, redirect, jsonify
from usuario import Usuario
from chat import Chat
from contato import Contatos

# Criando uma instância do Flask
app = Flask(__name__)
app.secret_key = "ben10"
usuario = Usuario()

# Definindo uma rota padrão
@app.route("/", methods=["GET", "POST"])
def pag_cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        senha = request.form["senha"]
        
        usuario.cadastrar(nome, telefone, senha)
        return render_template("login.html")

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def pag_login():
    if request.method == "POST":
        telefone = request.form["telefone"]
        senha = request.form["senha"]

        usuario.logar(telefone, senha)
        if usuario.logado:
            session['usuario_logado'] = {"nome": usuario.nome, "telefone": usuario.telefone}
            return render_template("chat.html")
        else:
            session.clear()
            return "Erro ao logar"
    else:
        return render_template("login.html")

@app.route("/chat")
def pag_chat():
    if "usuario_logado" in session:
        chatcola = Chat(usuario)
        contatos = chatcola.retornar_contatos()
        return render_template("chat.html", contatos=contatos)
    else:
        return redirect("/")  # Correção aqui
    

@app.route("/retorna_usuarios")
def retorna_usuarios():
    
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]                    
    chat = Chat(nome_usuario, telefone_usuario)

    contatos = chat.retornar_contatos()

    return jsonify(contatos), 200


@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagem(tel_destinatario):
    nome_usuario = session ["usuario_logado"]["nome"]
    telefone_usuario = session ["usuario_logado"]["telefone"]                    
    chat = Chat(nome_usuario, telefone_usuario)
    
    destinatario = Contatos ("", tel_destinatario)

    mensagens = chat.verificar_mensagem(0, destinatario)

    return jsonify(mensagens), 200 


@app.route("/enviar_mensagem", methods=['GET', 'POST'])
def enviar_mensagem():
    
    if request.method == "POST":
        dados = request.get_json()
        nome_usuario = session["usuario_logado"]["nome"]
        telefone_usuario = session["usuario_logado"]["telefone"]

        tel_destinatario = dados["usuario"]
        conteudo = dados["mensagem"]

        
        chat = Chat(nome_usuario, telefone_usuario)
        destinatario = Contatos("", tel_destinatario)
        enviado = chat.enviar_mensagem(conteudo, destinatario)
        return jsonify(enviado), 200
    
    


app.run(debug=True)
