from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import RegisterToolForm, ToEditToolForm, RegisterUserForm, LoginUserForm, ProfileEditForm
from app.models import Tool, User
from datetime import datetime

@app.route('/index', methods=['GET',])
@app.route('/', methods=['GET',])
@login_required
def index():
    return render_template('index.html', title="Home")

@app.route('/listar', methods=['GET',])
@login_required
def listar():
    tool = Tool.query.limit(10).all()

    return render_template('listar.html', tool=tool, title='Listar')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():

    form = RegisterToolForm()

    if form.validate_on_submit():
        tool = Tool(
            name=form.name.data, 
            author=form.author.data,
            alias=form.alias.data, 
            custom_alias=form.custom_alias.data,
            name_repository=form.name_repository.data,
            link=form.link.data, 
            type_install=form.type_install.data, 
            category=form.category.data, 
            dependencies=form.dependencies.data)
        db.session.add(tool)
        db.session.commit()
        flash('Ferramenta cadastrada com sucesso')
        return redirect(url_for('listar'))

    return render_template('cadastrar.html', title='Cadastrar', form=form)

@app.route('/visualizar/<id>/', methods=['GET',])
@login_required
def visualizar(id):
    tool = Tool.query.filter_by(id=id).first()

    if tool is None:
        flash('Ferramenta não existe')
        return redirect(url_for('index'))

    return render_template('visualizar.html', tool=tool, title='Visualizar')

@login_required
@app.route('/editar/<id>/', methods=['GET', 'POST'])
def editar(id):
    form = ToEditToolForm()
    tool = Tool.query.filter_by(id=id).first()

    if tool is None:
        flash('Ferramenta não existe')
        return redirect(url_for('listar'))

    if form.validate_on_submit():
        tool.name=form.name.data
        tool.author=form.author.data
        tool.alias=form.alias.data
        tool.custom_alias=form.custom_alias.data
        tool.name_repository=form.name_repository.data
        tool.link=form.link.data
        tool.type_install=form.type_install.data
        tool.category=form.category.data
        tool.dependencies=form.dependencies.data
        tool.modified=datetime.utcnow()

        db.session.commit()
        flash('Ferramenta atualizada com sucesso')
        return redirect(url_for('listar'))

    if request.method == 'GET':
        form.name.data = tool.name
        form.author.data = tool.author
        form.alias.data = tool.alias
        form.custom_alias.data = tool.custom_alias
        form.name_repository.data = tool.name_repository
        form.link.data = tool.link
        form.type_install.data = tool.type_install
        form.category.data = tool.category
        form.dependencies.data = tool.dependencies

    return render_template('edit.html', form=form, tool=tool, title='Editar')

@app.route('/deletar/<id>/', methods=['GET',])
@login_required
def deletar(id):
    tool = Tool.query.filter_by(id=id).first()

    if tool is None:
        flash('Ferramenta não existe')
        return redirect(url_for('listar'))

    db.session.delete(tool)
    db.session.commit()
    flash('Ferramenta excluída com sucesso')
    return redirect(url_for('listar'))

### Cadastro do usuário
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterUserForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form, title='Cadastrar')

### Acesso do usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginUserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou senha inválido!')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Acessar', form=form)

# Perfil do usuário
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileEditForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = form.password.data
        db.session.commit()
        flash('Perfil atualizado')

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('profile.html', title='Profile', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
