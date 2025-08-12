from flask import render_template, request, jsonify, flash, redirect, url_for, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import Project, Skill, Experience, Contact, User, ProjectLike, ProjectComment
from forms import ContactForm, LoginForm, RegisterForm, CommentForm
from functools import wraps
import logging

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Main portfolio page"""
    # Get featured projects
    featured_projects = Project.query.filter_by(featured=True).order_by(Project.order_priority.desc()).limit(6).all()
    
    # Get all projects for portfolio section
    all_projects = Project.query.order_by(Project.order_priority.desc()).all()
    
    # Get skills grouped by category
    frontend_skills = Skill.query.filter_by(category='frontend').order_by(Skill.order_priority.desc()).all()
    backend_skills = Skill.query.filter_by(category='backend').order_by(Skill.order_priority.desc()).all()
    tools_skills = Skill.query.filter_by(category='tools').order_by(Skill.order_priority.desc()).all()
    
    # Get work experience
    experiences = Experience.query.order_by(Experience.order_priority.desc()).all()
    
    # Create contact form
    contact_form = ContactForm()
    
    return render_template('index.html',
                         featured_projects=featured_projects,
                         all_projects=all_projects,
                         frontend_skills=frontend_skills,
                         backend_skills=backend_skills,
                         tools_skills=tools_skills,
                         experiences=experiences,
                         contact_form=contact_form)

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Create new contact entry
            contact_entry = Contact(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            
            db.session.add(contact_entry)
            db.session.commit()
            
            flash('Mensagem enviada com sucesso! Retornarei em breve.', 'success')
            logging.info(f"New contact message from {form.name.data} ({form.email.data})")
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao enviar mensagem. Tente novamente.', 'error')
            logging.error(f"Error saving contact message: {e}")
    
    else:
        # Return validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'error')
    
    return redirect(url_for('index') + '#contact')

@app.route('/api/projects')
def api_projects():
    """API endpoint for projects (for filtering)"""
    category = request.args.get('category', 'all')
    
    if category == 'all':
        projects = Project.query.order_by(Project.order_priority.desc()).all()
    else:
        projects = Project.query.filter_by(category=category).order_by(Project.order_priority.desc()).all()
    
    projects_data = []
    for project in projects:
        projects_data.append({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'short_description': project.short_description,
            'technologies': project.technologies.split(',') if project.technologies else [],
            'github_url': project.github_url,
            'live_url': project.live_url,
            'image_url': project.image_url,
            'category': project.category
        })
    
    return jsonify(projects_data)

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    return render_template('index.html'), 500

# Initialize sample data if database is empty
def create_sample_data():
    """Create sample data for demonstration"""
    if Project.query.count() == 0:
        # Sample projects
        projects = [
            Project(
                title="E-commerce Moderno",
                description="Plataforma completa de e-commerce com carrinho, pagamentos e dashboard administrativo.",
                short_description="E-commerce completo com React e Node.js",
                technologies="React,Node.js,MongoDB,Stripe,Tailwind CSS",
                github_url="https://github.com/example/ecommerce",
                live_url="https://ecommerce-demo.com",
                image_url="https://pixabay.com/get/g8d1feba2d9bf971f47663a7f5d85d4cd9d27bf10c21d4d856b079d57cd0c6d8d1df5fdb443862a2d979a81bd284ad66c8719e66c27d9884faa1292bc13798ead_1280.jpg",
                category="fullstack",
                featured=True,
                order_priority=10
            ),
            Project(
                title="Dashboard Analytics",
                description="Dashboard interativo com gráficos em tempo real e análise de dados avançada.",
                short_description="Dashboard com visualização de dados",
                technologies="Vue.js,Python,Flask,Chart.js,PostgreSQL",
                github_url="https://github.com/example/dashboard",
                live_url="https://dashboard-demo.com",
                image_url="https://pixabay.com/get/g3d14b6a808ac9a9d280afbe399b39fe74a6f1b592c04a1ac99a696223045a637019699c4334173d763d69e6713077b225d48d60762e90d61576c81f93836849b_1280.jpg",
                category="frontend",
                featured=True,
                order_priority=9
            ),
            Project(
                title="API RESTful",
                description="API robusta com autenticação JWT, rate limiting e documentação completa.",
                short_description="API RESTful com Node.js e Express",
                technologies="Node.js,Express,JWT,Redis,Docker",
                github_url="https://github.com/example/api",
                live_url="https://api-demo.com/docs",
                image_url="https://pixabay.com/get/g4cf8983770ff0b80c396f8aed6edf8a722e58c5b774d44b041dbd159ed5a8954cfbde0e8f2d3b26f1f6bf264a51a1d39c22738c4048318f8aede5e6d39bf17d4_1280.jpg",
                category="backend",
                featured=True,
                order_priority=8
            )
        ]
        
        for project in projects:
            db.session.add(project)
        
        # Sample skills
        skills = [
            # Frontend
            Skill(name="React", category="frontend", proficiency=95, icon_class="fab fa-react", order_priority=10),
            Skill(name="Vue.js", category="frontend", proficiency=90, icon_class="fab fa-vuejs", order_priority=9),
            Skill(name="JavaScript", category="frontend", proficiency=95, icon_class="fab fa-js", order_priority=8),
            Skill(name="TypeScript", category="frontend", proficiency=85, icon_class="fab fa-js", order_priority=7),
            Skill(name="HTML5/CSS3", category="frontend", proficiency=98, icon_class="fab fa-html5", order_priority=6),
            
            # Backend
            Skill(name="Node.js", category="backend", proficiency=90, icon_class="fab fa-node-js", order_priority=10),
            Skill(name="Python", category="backend", proficiency=95, icon_class="fab fa-python", order_priority=9),
            Skill(name="Flask", category="backend", proficiency=90, icon_class="fas fa-server", order_priority=8),
            Skill(name="MongoDB", category="backend", proficiency=85, icon_class="fas fa-database", order_priority=7),
            Skill(name="PostgreSQL", category="backend", proficiency=80, icon_class="fas fa-database", order_priority=6),
            
            # Tools
            Skill(name="Git", category="tools", proficiency=95, icon_class="fab fa-git-alt", order_priority=10),
            Skill(name="Docker", category="tools", proficiency=85, icon_class="fab fa-docker", order_priority=9),
            Skill(name="AWS", category="tools", proficiency=80, icon_class="fab fa-aws", order_priority=8),
            Skill(name="Figma", category="tools", proficiency=85, icon_class="fab fa-figma", order_priority=7),
        ]
        
        for skill in skills:
            db.session.add(skill)
        
        # Sample experience
        from datetime import date
        experiences = [
            Experience(
                company="TechCorp Solutions",
                position="Desenvolvedor Full Stack Sênior",
                description="Liderança técnica em projetos de grande escala, desenvolvimento de APIs RESTful e interfaces modernas com React. Mentoria de desenvolvedores júnior e implementação de boas práticas de desenvolvimento.",
                start_date=date(2022, 1, 1),
                end_date=None,
                location="São Paulo, SP",
                company_url="https://techcorp.com",
                order_priority=10
            ),
            Experience(
                company="StartupX",
                position="Desenvolvedor Full Stack",
                description="Desenvolvimento de MVP para startup de tecnologia financeira. Criação de sistema de pagamentos, dashboard administrativo e aplicativo mobile.",
                start_date=date(2020, 6, 1),
                end_date=date(2021, 12, 31),
                location="Remote",
                company_url="https://startupx.com",
                order_priority=9
            ),
        ]
        
        for experience in experiences:
            db.session.add(experience)
        
        db.session.commit()
        logging.info("Sample data created successfully")

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Bem-vindo, {user.full_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('index'))

# Project interaction routes
@app.route('/project/<int:project_id>/like', methods=['POST'])
@login_required
def toggle_like(project_id):
    """Toggle project like"""
    project = Project.query.get_or_404(project_id)
    
    existing_like = ProjectLike.query.filter_by(
        user_id=current_user.id, 
        project_id=project_id
    ).first()
    
    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        new_like = ProjectLike(user_id=current_user.id, project_id=project_id)
        db.session.add(new_like)
        liked = True
    
    db.session.commit()
    
    return jsonify({
        'liked': liked,
        'likes_count': project.likes_count
    })

@app.route('/project/<int:project_id>/comment', methods=['POST'])
@login_required
def add_comment(project_id):
    """Add project comment"""
    project = Project.query.get_or_404(project_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = ProjectComment(
            user_id=current_user.id,
            project_id=project_id,
            content=form.content.data
        )
        
        db.session.add(comment)
        db.session.commit()
        
        flash('Comentário adicionado com sucesso!', 'success')
    else:
        for error in form.content.errors:
            flash(error, 'error')
    
    return redirect(url_for('index') + f'#project-{project_id}')

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Project detail page with comments"""
    project = Project.query.get_or_404(project_id)
    comments = ProjectComment.query.filter_by(
        project_id=project_id, 
        is_approved=True
    ).order_by(ProjectComment.created_at.desc()).all()
    
    comment_form = CommentForm()
    
    return render_template('project_detail.html', 
                         project=project, 
                         comments=comments, 
                         comment_form=comment_form)

# Admin Routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    # Get statistics
    stats = {
        'projects': Project.query.count(),
        'users': User.query.count(),
        'contacts': Contact.query.filter_by(is_read=False).count(),
        'comments': ProjectComment.query.filter_by(is_approved=False).count()
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/projects')
@login_required
@admin_required
def admin_projects():
    """Admin projects management"""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Admin users management"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/contacts')
@login_required
@admin_required
def admin_contacts():
    """Admin contacts management"""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@app.route('/admin/contact/<int:contact_id>/mark_read')
@login_required
@admin_required
def mark_contact_read(contact_id):
    """Mark contact as read"""
    contact = Contact.query.get_or_404(contact_id)
    contact.is_read = True
    db.session.commit()
    flash('Mensagem marcada como lida.', 'success')
    return redirect(url_for('admin_contacts'))

@app.route('/admin/comment/<int:comment_id>/approve')
@login_required
@admin_required
def approve_comment(comment_id):
    """Approve comment"""
    comment = ProjectComment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    flash('Comentário aprovado.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/create_admin')
def create_admin_user():
    """Create admin user (development only)"""
    if User.query.filter_by(is_admin=True).first():
        return "Admin user already exists"
    
    admin = User(
        username='admin',
        email='admin@portfolio.com',
        full_name='Administrator',
        is_admin=True
    )
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    
    return "Admin user created! Username: admin, Password: admin123"
