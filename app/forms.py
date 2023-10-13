from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import User

types_install = ["apt", "apt not official", "git", "curl"]
categories = [
    "Information Collection",
    "Vulnerability Analysis",
    "Wireless Attacks",
    "Web Applications",
    "Sniffing and Faking",
    "Maintaining Access",
    "Reporting Tools",
    "Exploitation Tools",
    "Forensic Tools",
    "Stress Test",
    "Password Attacks",
    "Reverse Engineering",
    "Hardware Hacking",
    "Extra"
]

class RegisterToolForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    alias = StringField('Apelido', validators=[DataRequired()])
    custom_alias = StringField('Apelido customizado')
    name_repository = StringField('Nome do repositório')
    link = StringField('Link do repositório ou instalador')
    type_install = SelectField(
        'Tipo de instalação', 
        choices=types_install, 
        id="type_install", default="apt",
        validators=[DataRequired()]
    )
    category = SelectField(
        'Categoria',
        choices=categories,
        id="category", default="Extra",
        validators=[DataRequired()]
    )
    dependencies = StringField('Dependencias')
    submit = SubmitField('Cadastrar')


class ToEditToolForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    alias = StringField('Apelido', validators=[DataRequired()])
    custom_alias = StringField('Apelido customizado')
    name_repository = StringField('Nome do repositório')
    link = StringField('Link')
    type_install = SelectField('Tipo de instalação',
        choices=types_install,
        id="type_install", 
        default="apt", 
        validators=[DataRequired()]
    )
    category = SelectField('Categoria',
        choices=categories,
        id="category", default="Extra",
        validators=[DataRequired()]
    )
    dependencies = StringField('Dependenciad')
    submit = SubmitField('Editar')


class RegisterUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user is not None:
            raise ValidationError('Escolha um usuário diferente!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is not None:
            raise ValidationError('Escolha um email diferente!')


class LoginUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Acessar')
