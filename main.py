from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Enhanced Portfolio Data
PORTFOLIO_DATA = {
    "personal_info": {
        "name": "Utkarsh Dimri",
        "title": "AI/ML Engineer",
        "location": "India",
        "email": "utkarsh@example.com",
        "phone": "+91 XXXXX XXXXX",
        "github": "https://github.com/utkarsh",
        "linkedin": "https://linkedin.com/in/utkarsh",
        "avatar": "UD",
        "bio": "Passionate AI/ML engineer with a strong foundation in full-stack development. I love building intelligent systems that solve real-world problems and constantly exploring new technologies to enhance productivity and innovation.",
        "status": "Available for opportunities",
        "experience": "3+ Years",
        "projects_count": "15+",
        "coffee_consumed": "∞"
    },
    "skills": {
        "programming_languages": [
            {"name": "Python", "level": 90, "icon": "🐍"},
            {"name": "JavaScript", "level": 85, "icon": "🟨"},
            {"name": "TypeScript", "level": 80, "icon": "🔵"},
            {"name": "HTML/CSS", "level": 95, "icon": "🌐"},
            {"name": "SQL", "level": 75, "icon": "🗄️"}
        ],
        "frameworks": [
            {"name": "React", "level": 85, "icon": "⚛️"},
            {"name": "Django", "level": 90, "icon": "🎯"},
            {"name": "Flask", "level": 85, "icon": "🌶️"},
            {"name": "Node.js", "level": 75, "icon": "🟢"},
            {"name": "TailwindCSS", "level": 90, "icon": "🎨"}
        ],
        "ai_ml": [
            {"name": "TensorFlow", "level": 70, "icon": "🧠"},
            {"name": "PyTorch", "level": 65, "icon": "🔥"},
            {"name": "Scikit-learn", "level": 75, "icon": "📊"},
            {"name": "NumPy", "level": 80, "icon": "🔢"},
            {"name": "Pandas", "level": 75, "icon": "🐼"}
        ],
        "tools": [
            {"name": "Git", "level": 85, "icon": "🔧"},
            {"name": "Docker", "level": 70, "icon": "🐳"},
            {"name": "AWS", "level": 65, "icon": "☁️"},
            {"name": "PostgreSQL", "level": 80, "icon": "🐘"},
            {"name": "MongoDB", "level": 75, "icon": "🍃"}
        ]
    },
    "projects": [
        {
            "id": 1,
            "title": "AI-Powered Task Automation",
            "description": "Developed an intelligent task automation system using Python and machine learning algorithms to optimize workflow efficiency by 60%.",
            "technologies": ["Python", "TensorFlow", "Flask", "NumPy", "Pandas"],
            "github": "https://github.com/utkarsh/ai-task-automation",
            "demo": "https://ai-automation-demo.com",
            "category": "AI/ML",
            "status": "Completed",
            "year": "2023",
            "features": [
                "Automated workflow optimization",
                "Machine learning predictions",
                "Real-time analytics dashboard",
                "API integration"
            ]
        },
        {
            "id": 2,
            "title": "Full-Stack Web Application",
            "description": "Built a comprehensive web application with user authentication, real-time data processing, and responsive design serving 1000+ users.",
            "technologies": ["React", "Node.js", "PostgreSQL", "Socket.io", "JWT"],
            "github": "https://github.com/utkarsh/fullstack-app",
            "demo": "https://fullstack-demo.com",
            "category": "Web Development",
            "status": "Completed",
            "year": "2023",
            "features": [
                "User authentication system",
                "Real-time notifications",
                "Responsive design",
                "API rate limiting"
            ]
        },
        {
            "id": 3,
            "title": "Data Analysis Dashboard",
            "description": "Created an interactive dashboard for data visualization and analysis using advanced Python libraries processing 10GB+ daily data.",
            "technologies": ["Python", "Pandas", "Plotly", "Django", "Redis"],
            "github": "https://github.com/utkarsh/data-dashboard",
            "demo": "https://data-dashboard-demo.com",
            "category": "Data Science",
            "status": "Completed",
            "year": "2022",
            "features": [
                "Interactive data visualization",
                "Real-time data processing",
                "Export functionality",
                "Multi-user support"
            ]
        },
        {
            "id": 4,
            "title": "Smart Recommendation Engine",
            "description": "Built a machine learning recommendation system with collaborative filtering achieving 85% accuracy rate.",
            "technologies": ["Python", "Scikit-learn", "FastAPI", "Docker", "Redis"],
            "github": "https://github.com/utkarsh/recommendation-engine",
            "demo": "https://recommendation-demo.com",
            "category": "AI/ML",
            "status": "In Progress",
            "year": "2024",
            "features": [
                "Collaborative filtering",
                "Content-based recommendations",
                "A/B testing framework",
                "Scalable architecture"
            ]
        },
        {
            "id": 5,
            "title": "Terminal Portfolio Website",
            "description": "Developed this interactive terminal-based portfolio with animations and responsive design.",
            "technologies": ["Flask", "JavaScript", "TailwindCSS", "HTML5"],
            "github": "https://github.com/utkarsh/terminal-portfolio",
            "demo": "https://utkarsh-portfolio.com",
            "category": "Web Development",
            "status": "Completed",
            "year": "2024",
            "features": [
                "Terminal interface",
                "Command-line navigation",
                "Animated elements",
                "Responsive design"
            ]
        }
    ],
    "journey": [
        {
            "year": "2024",
            "title": "Senior AI/ML Engineer",
            "company": "Tech Innovation Corp",
            "description": "Leading AI initiatives and building intelligent systems for enterprise clients",
            "technologies": ["Python", "TensorFlow", "AWS", "Docker"],
            "achievements": [
                "Increased system efficiency by 45%",
                "Led team of 5 developers",
                "Deployed ML models to production"
            ]
        },
        {
            "year": "2023",
            "title": "Full-Stack Developer",
            "company": "StartupXYZ",
            "description": "Built scalable web applications and APIs serving thousands of users",
            "technologies": ["React", "Node.js", "PostgreSQL", "AWS"],
            "achievements": [
                "Developed 3 major applications",
                "Reduced load time by 60%",
                "Implemented CI/CD pipeline"
            ]
        },
        {
            "year": "2022",
            "title": "Backend Developer",
            "company": "DataCorp Solutions",
            "description": "Specialized in Python development and data processing systems",
            "technologies": ["Python", "Django", "PostgreSQL", "Redis"],
            "achievements": [
                "Processed 10GB+ daily data",
                "Built RESTful APIs",
                "Optimized database queries"
            ]
        },
        {
            "year": "2021",
            "title": "Junior Developer",
            "company": "WebDev Agency",
            "description": "Started professional journey with web development fundamentals",
            "technologies": ["HTML", "CSS", "JavaScript", "PHP"],
            "achievements": [
                "Created 10+ websites",
                "Learned modern frameworks",
                "Collaborated with design team"
            ]
        }
    ]
}

# Essential Terminal Commands
TERMINAL_COMMANDS = {
    "help": "Show all available commands",
    "about": "Display detailed information about me",
    "projects": "View my portfolio projects",
    "skills": "Check out my technical skills",
    "journey": "View my career journey",
    "contact": "Get in touch with me",
    "resume": "Download my resume",
    "ls": "List available sections",
    "cat": "Display file contents",
    "clear": "Clear the terminal",
    "date": "Show current date and time",
    "pwd": "Show current directory",
    "tree": "Display directory structure"
}

@app.route('/')
def index():
    """Main terminal portfolio page"""
    return render_template('index.html', 
                         personal_info=PORTFOLIO_DATA['personal_info'],
                         commands=TERMINAL_COMMANDS)

@app.route('/about')
def about():
    """About page with journey timeline"""
    return render_template('about.html', 
                         personal_info=PORTFOLIO_DATA['personal_info'],
                         journey=PORTFOLIO_DATA['journey'])

@app.route('/projects')
def projects():
    """Projects showcase page"""
    return render_template('projects.html', 
                         projects=PORTFOLIO_DATA['projects'],
                         personal_info=PORTFOLIO_DATA['personal_info'])

@app.route('/skills')
def skills():
    """Skills and technologies page"""
    return render_template('skills.html', 
                         skills=PORTFOLIO_DATA['skills'],
                         personal_info=PORTFOLIO_DATA['personal_info'])

@app.route('/journey')
def journey():
    """Career journey page"""
    return render_template('journey.html', 
                         journey=PORTFOLIO_DATA['journey'],
                         personal_info=PORTFOLIO_DATA['personal_info'])

@app.route('/contact')
def contact():
    """Contact information page"""
    return render_template('contact.html', 
                         personal_info=PORTFOLIO_DATA['personal_info'])

# API Routes
@app.route('/api/terminal/command', methods=['POST'])
def process_terminal_command():
    """Process terminal commands with enhanced responses"""
    data = request.get_json()
    command = data.get('command', '').strip().lower()
    args = command.split()[1:] if len(command.split()) > 1 else []
    base_command = command.split()[0] if command else ''
    
    response = {
        'command': data.get('command', ''),
        'output': '',
        'redirect': None,
        'timestamp': datetime.now().isoformat()
    }
    
    if base_command == 'help':
        response['output'] = {
            'type': 'help',
            'commands': TERMINAL_COMMANDS
        }
    elif base_command == 'about':
        response['redirect'] = '/about'
        response['output'] = 'Initializing about.exe...'
    elif base_command == 'projects':
        response['redirect'] = '/projects'
        response['output'] = 'Loading project portfolio...'
    elif base_command == 'skills':
        response['redirect'] = '/skills'
        response['output'] = 'Scanning skill database...'
    elif base_command == 'journey':
        response['redirect'] = '/journey'
        response['output'] = 'Accessing career timeline...'
    elif base_command == 'contact':
        response['redirect'] = '/contact'
        response['output'] = 'Opening contact interface...'
    elif base_command == 'resume':
        response['output'] = 'Resume download initiated... [Feature coming soon]'
    elif base_command == 'date':
        response['output'] = datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')
    elif base_command == 'ls':
        response['output'] = {
            'type': 'ls',
            'sections': ['about/', 'projects/', 'skills/', 'journey/', 'contact/', 'resume.pdf']
        }
    elif base_command == 'pwd':
        response['output'] = '/home/utkarsh/portfolio'
    elif base_command == 'tree':
        response['output'] = {
            'type': 'tree',
            'structure': [
                'portfolio/',
                '├── about/',
                '├── projects/',
                '│   ├── ai-automation/',
                '│   ├── web-apps/',
                '│   └── data-science/',
                '├── skills/',
                '├── journey/',
                '├── contact/',
                '└── resume.pdf'
            ]
        }
    elif base_command == 'cat':
        if args and args[0] == 'readme.txt':
            response['output'] = {
                'type': 'file',
                'filename': 'readme.txt',
                'content': f"""# {PORTFOLIO_DATA['personal_info']['name']} - Portfolio

## About
{PORTFOLIO_DATA['personal_info']['bio']}

## Quick Stats
- Experience: {PORTFOLIO_DATA['personal_info']['experience']}
- Projects: {PORTFOLIO_DATA['personal_info']['projects_count']}
- Status: {PORTFOLIO_DATA['personal_info']['status']}

## Contact
- Email: {PORTFOLIO_DATA['personal_info']['email']}
- GitHub: {PORTFOLIO_DATA['personal_info']['github']}
- LinkedIn: {PORTFOLIO_DATA['personal_info']['linkedin']}

## Commands
Type 'help' to see available commands or explore:
- about    - Learn more about me
- projects - View my work
- skills   - Check my technical skills
- journey  - See my career path
- contact  - Get in touch
"""
            }
        else:
            filename = args[0] if args else 'filename'
            response['output'] = f"cat: {filename}: No such file or directory"
    elif base_command == 'clear':
        response['output'] = 'CLEAR_TERMINAL'
    elif base_command:
        response['output'] = f"bash: {base_command}: command not found\nType 'help' to see available commands."
    
    return jsonify(response)

@app.route('/api/portfolio')
def api_portfolio():
    """API endpoint to get all portfolio data"""
    return jsonify(PORTFOLIO_DATA)

@app.route('/api/contact', methods=['POST'])
def api_contact():
    """Handle contact form submissions"""
    data = request.get_json()
    
    # Here you would typically save to database or send email
    response = {
        'success': True,
        'message': 'Message received! I will get back to you within 24 hours.',
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)