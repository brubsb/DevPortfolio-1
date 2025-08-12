from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class ContactForm(FlaskForm):
    """Contact form for portfolio"""
    name = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=2, max=100, message='Nome deve ter entre 2 e 100 caracteres')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido'),
        Length(max=120, message='Email muito longo')
    ])
    
    subject = StringField('Assunto', validators=[
        DataRequired(message='Assunto é obrigatório'),
        Length(min=5, max=200, message='Assunto deve ter entre 5 e 200 caracteres')
    ])
    
    message = TextAreaField('Mensagem', validators=[
        DataRequired(message='Mensagem é obrigatória'),
        Length(min=10, max=1000, message='Mensagem deve ter entre 10 e 1000 caracteres')
    ])
    
    submit = SubmitField('Enviar Mensagem')

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Usuário', validators=[
        DataRequired(message='Nome de usuário é obrigatório'),
        Length(min=3, max=80, message='Nome de usuário deve ter entre 3 e 80 caracteres')
    ])
    
    password = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])
    
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    """User registration form"""
    full_name = StringField('Nome Completo', validators=[
        DataRequired(message='Nome completo é obrigatório'),
        Length(min=2, max=100, message='Nome deve ter entre 2 e 100 caracteres')
    ])
    
    username = StringField('Nome de Usuário', validators=[
        DataRequired(message='Nome de usuário é obrigatório'),
        Length(min=3, max=80, message='Nome de usuário deve ter entre 3 e 80 caracteres')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido'),
        Length(max=120, message='Email muito longo')
    ])
    
    password = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, max=128, message='Senha deve ter pelo menos 6 caracteres')
    ])
    
    password2 = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Confirmação de senha é obrigatória'),
        EqualTo('password', message='Senhas devem ser iguais')
    ])
    
    submit = SubmitField('Cadastrar')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nome de usuário já está sendo usado.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já está sendo usado.')

class CommentForm(FlaskForm):
    """Form for project comments"""
    content = TextAreaField('Comentário', validators=[
        DataRequired(message='Comentário é obrigatório'),
        Length(min=5, max=500, message='Comentário deve ter entre 5 e 500 caracteres')
    ])
    
    submit = SubmitField('Comentar')
