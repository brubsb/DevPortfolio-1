from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Project, Skill, Experience, Contact
from forms import ContactForm
import logging

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
