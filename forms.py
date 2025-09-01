from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, URL
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

class ProjectForm(FlaskForm):
    """Form for creating and editing projects"""
    title = StringField('Título', validators=[
        DataRequired(message='Título é obrigatório'),
        Length(min=5, max=100, message='Título deve ter entre 5 e 100 caracteres')
    ])
    
    short_description = StringField('Descrição Curta', validators=[
        DataRequired(message='Descrição curta é obrigatória'),
        Length(min=10, max=200, message='Descrição curta deve ter entre 10 e 200 caracteres')
    ])
    
    description = TextAreaField('Descrição Completa', validators=[
        DataRequired(message='Descrição completa é obrigatória'),
        Length(min=50, max=2000, message='Descrição deve ter entre 50 e 2000 caracteres')
    ])
    
    technologies = StringField('Tecnologias', validators=[
        DataRequired(message='Tecnologias são obrigatórias'),
        Length(min=5, max=500, message='Tecnologias deve ter entre 5 e 500 caracteres')
    ], description='Separe as tecnologias por vírgula (ex: React, Node.js, MongoDB)')
    
    category = SelectField('Categoria', choices=[
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('fullstack', 'Full Stack'),
        ('mobile', 'Mobile'),
        ('design', 'Design')
    ], validators=[DataRequired(message='Categoria é obrigatória')])
    
    github_url = StringField('URL do GitHub', validators=[
        Optional(),
        URL(message='URL do GitHub inválida'),
        Length(max=200, message='URL muito longa')
    ])
    
    live_url = StringField('URL do Projeto', validators=[
        Optional(),
        URL(message='URL do projeto inválida'),
        Length(max=200, message='URL muito longa')
    ])
    
    image = FileField('Imagem do Projeto', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Apenas imagens são permitidas!')
    ])
    
    featured = BooleanField('Projeto em Destaque')
    
    order_priority = IntegerField('Prioridade', validators=[
        Optional()
    ], default=0, description='Maior número = maior prioridade')
    
    submit = SubmitField('Salvar Projeto')

class SkillForm(FlaskForm):
    """Form for creating and editing skills"""
    name = StringField('Nome da Habilidade', validators=[
        DataRequired(message='Nome da habilidade é obrigatório'),
        Length(min=2, max=50, message='Nome deve ter entre 2 e 50 caracteres')
    ])
    
    category = SelectField('Categoria', choices=[
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('tools', 'Ferramentas'),
        ('database', 'Banco de Dados'),
        ('design', 'Design')
    ], validators=[DataRequired(message='Categoria é obrigatória')])
    
    proficiency = IntegerField('Proficiência (%)', validators=[
        DataRequired(message='Proficiência é obrigatória'),
    ], description='Entre 1 e 100')
    
    icon_class = StringField('Classe do Ícone', validators=[
        Optional(),
        Length(max=50, message='Classe muito longa')
    ], description='Ex: fab fa-react, fas fa-database')
    
    order_priority = IntegerField('Prioridade', validators=[
        Optional()
    ], default=0, description='Maior número = maior prioridade')
    
    submit = SubmitField('Salvar Habilidade')
