from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Project(db.Model):
    """Model for portfolio projects"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(200), nullable=False)
    technologies = db.Column(db.String(500), nullable=False)  # Comma-separated
    github_url = db.Column(db.String(200))
    live_url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    category = db.Column(db.String(50), nullable=False)
    featured = db.Column(db.Boolean, default=False)
    order_priority = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    likes = db.relationship('ProjectLike', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('ProjectComment', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    def is_liked_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.likes.filter_by(user_id=user.id).first() is not None
    
    def __repr__(self):
        return f'<Project {self.title}>'

class Skill(db.Model):
    """Model for skills with proficiency levels"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # frontend, backend, tools, etc.
    proficiency = db.Column(db.Integer, nullable=False)  # 1-100
    icon_class = db.Column(db.String(50))  # Font Awesome class
    order_priority = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Skill {self.name}>'

class Experience(db.Model):
    """Model for work experience"""
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # Null for current position
    location = db.Column(db.String(100))
    company_url = db.Column(db.String(200))
    order_priority = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Experience {self.position} at {self.company}>'

class Contact(db.Model):
    """Model for contact form submissions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Contact from {self.name}>'

# User Models for Authentication
class User(UserMixin, db.Model):
    """Model for registered users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    likes = db.relationship('ProjectLike', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('ProjectComment', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class ProjectLike(db.Model):
    """Model for project likes"""
    __tablename__ = 'project_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate likes
    __table_args__ = (db.UniqueConstraint('user_id', 'project_id'),)
    
    def __repr__(self):
        return f'<ProjectLike user:{self.user_id} project:{self.project_id}>'

class ProjectComment(db.Model):
    """Model for project comments"""
    __tablename__ = 'project_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)  # Admin can moderate
    
    def __repr__(self):
        return f'<ProjectComment by {self.user.username} on {self.project.title}>'
