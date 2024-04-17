# pip install flask==2.0.2
# npm install bootstrap@5.2.0

# Importando o Flask
from contextlib import redirect_stderr
from flask import Flask, render_template, request, redirect, session, flash, url_for

# session - salvar dados de login(Retém informações por mais de um ciclo de request)
# redirect - redirecionar pagina
# render_template -  acessar página HTML
# Flash - Imprime mensagem na tela
# url_for - utilizada para atualizar as rotas de maneira dinamica


# -------------------------------------------------------------
# Criando classe (orientação a objeto)
class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Bruno Divino", "BD", "alohomora")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "Python_eh_vida")

usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3}


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


# Virou um fator Global.
jogo_2 = Jogo('GOD OF WAR', 'Ação', 'Playstation 2')
jogo_3 = Jogo('TETRIS', 'Puzzle', 'Atari')
jogo_4 = Jogo('Mortal Combate', 'Ação', 'Desktop')
lista_1 = [jogo_2, jogo_3, jogo_4]


# -------------------------------------------------------------

# Variavel app - chama a função flask, o __name__ faz o app rodar
app = Flask(__name__)
# chave secreta/encriptar os dados
app.secret_key = 'alura'

# colocando informação no site, para colocar uma informação no site é necessário colocar uma rota, nomeando a rota: '/inicio', faz necesssário a criação da função.


@app.route('/')  # @app.route('/inicio')
def index():
    # Passando manulmente valor do jogo (maneira 1 - manualmente)
    # jogo_1 = 'Mario Bros'
    # # Ajustando o conteúdo dinamicamente (maneira 2- via lista)
    # lista = ['Robocop x Exterminador do Futuro', 'Batman Beyond']

    return render_template('lista.html', titulo='Jogos', jogos=lista_1)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # return redirect('/login')
        # return redirect('/login?proxima=novo')  # Query string ?proxima
        # variavel proxima página
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


# por padrão aceita apenas get, para aceita o metodo Post precisar parametrizar
@app.route('/criar', methods=['POST', ])
def criar():
    # procura no novo HTML -> FORM -> TAG NOME -> NOME DOS CAMPOS(NAME)
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista_1.append(jogo)
    # return redirect('/')
    # return render_template('lista.html', titulo='Jogos', jogos=lista_2)
    return redirect(url_for('index'))
# -----------------------------------------------
# Login


@app.route('/login')
def login():
  # args -> argumetos
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))
# -----------------------------------------------
# Logout


@ app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    # return redirect('/')
    return redirect(url_for('index'))


app.run(debug=True)

# -----------------------------------------------


# Executar aplicação rodar
app.run(debug=True)
