from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'labs'

class lab:
    def __init__(self, nome, setor, hora, professor, disciplina):
        self.nome = nome
        self.setor = setor
        self.hora = hora
        self.professor = professor
        self.disciplina = disciplina

lab1 = lab('Laboratório 1','Agropecuária', '07:30', 'Nustenil', 'Algoritmos e Programação II')
lab2 = lab('Laboratório 2', 'Informática', '18:30', 'Prof. Teste', 'Banco de Dados')
lista = [lab1,lab2]

class cadastro:
    def __init__(self, matricula, nome_prof, segundo_nome, email_prof, senha, telefone):
        self.matricula = matricula
        self.nome_prof = nome_prof
        self.segundo_nome = segundo_nome
        self.email_prof = email_prof
        self.senha = senha
        self.telefone = telefone


usuario1 = cadastro('2014','Professor Teste', 'Souza' ,'teste123@gmail.com', '123', '(88) 9-92323134')
usuario2 = cadastro('','Maria Joana','Mendes','joaninhaMaria@gmail.com', 'marijo123', '(88) 9-93254226')
lista_cadastros = [usuario1, usuario2]


@app.route('/')
def index():
    return render_template('/index.html')

@app.route ('/inicio')
def inicio():
    return render_template('lista.html', titulo = 'Laboratórios Ocupados', labs = lista)

@app.route ('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=novo')
    return render_template ('novo.html', titulo = 'Reservar Laboratório')

@app.route ('/criar',methods=['POST','GET',])
def criar():
    nome = request.form['nome']
    setor = request.form['setor']
    hora = request.form['hora']
    professor = session['usuario_logado']
    disciplina = request.form['disciplina']

    for i in range(len(lista)):
        if nome == lista[i].nome and setor == lista[i].setor and hora == lista[i].hora:
            flash("Ops... O Mesmo laboratório já está reservado para este horário :(")
            return redirect('/novo')

    new_lab = lab(nome,setor,hora,professor,disciplina)
    lista.append(new_lab)
    return redirect('/inicio')


@app.route ('/login')
def login():
    for i in range(len(lista_cadastros)):
        print(lista_cadastros[i].email_prof, '||', lista_cadastros[i].senha)

    if session['usuario_logado'] != None:
        flash('Ops... Voce já está logado.')
        return redirect ('/inicio')

    if(request.args.get('proxima') != None):
        proxima = request.args.get('proxima')
    else:
        proxima = "inicio"
    print(proxima)
    return render_template('login.html', proxima=proxima)


@app.route ('/autenticar', methods=['POST','GET',])
def autenticar():
    if request.method == 'POST': 
        for i in range(len(lista_cadastros)):
            if request.form['usuario'] == lista_cadastros[i].email_prof and request.form['senha'] == lista_cadastros[i].senha:
                session['usuario_logado'] = lista_cadastros[i].nome_prof
                flash(session['usuario_logado'] + ' logado com sucesso.')
                proxima_pagina = request.form['proxima'] 
                return redirect (url_for('{}'.format(proxima_pagina)))
        flash('Não logado, tente novamente.')
        return redirect('/login')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum Usuário Logado!')
    return redirect('/')

@app.route('/cadastro')
def cad():
    return render_template('cadastro.html')

@app.route('/novo_usu', methods =['POST'])
def cria_usuario():
    professor = request.form['nome_prof']
    segundo_nome = request.form['segundo_nome']
    matricula = request.form['matricula']
    email_prof = request.form['email']
    senha_prof = request.form['senha']
    telefone = request.form['telefone']

    novo_cadastro = cadastro(matricula,professor,segundo_nome,email_prof,senha_prof,telefone)
    lista_cadastros.append(novo_cadastro)
    return redirect('/')

app.run(debug=True) 
