from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

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
