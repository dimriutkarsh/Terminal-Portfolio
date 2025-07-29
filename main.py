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
        "email": "dimriutkarsh55@gmail.com",
        "phone": "+91 XXXXX X6262",
        "github": "https://github.com/dimriutkarsh",
        "linkedin": "https://www.linkedin.com/in/utkarsh-dimri-029672242/",
        "kaggle": "https://www.kaggle.com/utkarshdimri",
        "avatar": "UD",
        "bio": "Passionate AI/ML engineer with a strong foundation in full-stack development. I love building intelligent systems that solve real-world problems and constantly exploring new technologies to enhance productivity and innovation.",
        "status": "Available for opportunities",
        "experience": "1 Year",
        "projects_count": "15+",
        "coffee_consumed": "∞"
    },
    "skills": {
       "frontend": [
      { "name": "HTML5", "level": 90, "icon": "🌐" },
      { "name": "CSS3", "level": 60, "icon": "🎨" },
      { "name": "JavaScript", "level": 50, "icon": "⚡" },
      { "name": "Responsive Design", "level": 88, "icon": "📱" }
    ],
    "backend": [
      { "name": "Python", "level": 88, "icon": "🐍" },
      { "name": "Django", "level": 45, "icon": "🎯" },
      { "name": "Flask", "level": 55, "icon": "🔥" },
      { "name": "Database Design", "level": 75, "icon": "🗄️" }
    ],
    "ai_ml_programming": [
      { "name": "C Programming", "level": 75, "icon": "💻" },
      { "name": "NumPy", "level": 50, "icon": "🔢" },
      { "name": "Pandas", "level": 55, "icon": "�"},
      { "name": "Matplotlib", "level": 55, "icon": "�"},
      { "name": "AI Tools Integration", "level": 65, "icon": "🤖" },
      { "name": "Data Analysis", "level": 60, "icon": "📊" }
    ],

    "WebScrapping": [
      { "name": "Requests", "level": 65, "icon": "" },
      { "name": "BeautifulSoup", "level": 55, "icon": "" },
      { "name": "Data Analysis", "level": 60, "icon": "📊" }
    ],

        "tools": [
            {"name": "Git/Github", "level": 55, "icon": "🔧"},
            {"name": "AI-Tools", "level": 75, "icon": "🐼"},
            {"name": "NO-code/Low-code", "level": 75, "icon": "🍃"},
            {"name": "Gen AI Tools ", "level": 80, "icon": "🤖"},
            # {"name": "Docker", "level": 70, "icon": "🐳"},
            # {"name": "AWS", "level": 65, "icon": "☁️"},
            # {"name": "PostgreSQL", "level": 80, "icon": "🐘"},
            # {"name": "MongoDB", "level": 75, "icon": "🍃"}
        ]
    },
    "projects": [
        
        {
      "id": 1,
      "title": "VanRakshak",
      "description": "A group project to detect forest fires using thermal mapping and Google Maps integration.",
      "technologies": ["HTML5", "CSS3", "JavaScript", "API Integration"],
      "github": "https://github.com/dimriutkarsh/VanRakshak",
      "demo": "https://dimriutkarsh.github.io/VanRakshak/",
      "category": "Frontend",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Detects forest fires through thermal mapping",
        "Uses Google Maps model",
        "Can be used for promoting plantation drives"
            ]
        },
        {
      "id": 2,
      "title": "Interactive Portfolio Website",
      "description": "A responsive portfolio website with animations, modern UI/UX, and interactive components.",
      "technologies": ["HTML5", "CSS3", "JavaScript", "Responsive Design"],
      "github": "https://github.com/dimriutkarsh/Personal-Portfolio",
      "demo": "http://personal-portfolio-production-cf5e.up.railway.app",
      "category": "Frontend",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Responsive design with CSS Grid and Flexbox",
        "Smooth scrolling and animations",
        "Interactive JavaScript components",
        "Modern UI/UX design principles"
            ]
        },
        {
      "id": 3,
      "title": "NotesNest",
      "description": "A web app for students to access notes, formulas, and extract text from images using AI.",
      "technologies": ["HTML5", "CSS3", "JavaScript", "OCR"],
      "github": "https://github.com/dimriutkarsh/NotesNest",
      "demo": "https://dimriutkarsh.github.io/NotesNest/",
      "category": "Frontend",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Search notes and formulas instantly",
        "Voice input support",
        "Extract text from images with Tesseract.js",
        "AI API integration for fetching notes",
        "Clean, responsive web design"
            ]
        },
        {
      "id": 4,
      "title": "Image-generating Chatbot",
      "description": "A chatbot that generates unique AI images from user descriptions.",
      "technologies": ["HTML5", "CSS3", "JavaScript", "API Integration"],
      "github": "https://github.com/dimriutkarsh/image-generation-chatbot",
      "demo": "https://dimriutkarsh.github.io/image-generation-chatbot/",
      "category": "Frontend",
      "status": "Completed",
      "year": "2024",
      "features": [
        "AI-powered image generation",
        "Create visuals based on user imagination"

            ]
        },
        {
      "id": 5,
      "title": "DeepShiva Chatbot",
      "description": "An AI chatbot with multilingual support and real-time intelligent responses.",
      "technologies": ["HTML5", "CSS3", "JavaScript", "API Integration"],
      "github": "https://github.com/dimriutkarsh/DeepShiva",
      "demo": "https://dimriutkarsh.github.io/DeepShiva/",
      "category": "Frontend",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Voice recognition support",
        "Multilingual responses",
        "Real-time search functionality",
        "Dark mode interface"
            ]
        },
            {
      "id": 6,
      "title": "Edu-Hub",
      "description": "An academic platform providing access to question papers, assignments, and notes.",
      "technologies": ["HTML5", "CSS3", "JavaScript", "API Integration"],
      "github": "https://github.com/dimriutkarsh/EduHub",
      "demo": "https://dimriutkarsh.github.io/EduHub/",
      "category": "Frontend",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Previous year question papers",
        "Assignments upload",
        "Regular and short notes access"
      ]
    },
        {
      "id": 7,
      "title": "AI-Powered Task Management System",
      "description": "Task management app with AI task prioritization and user authentication built using Django.",
      "technologies": ["Django", "Python", "SQLite", "AI Integration"],
      "github": "#",
      "demo": "#",
      "category": "Full-Stack",
      "status": "Completed",
      "year": "2024",
      "features": [
        "User authentication and authorization",
        "AI-powered task prioritization",
        "Real-time notifications",
        "Advanced filtering and search"
      ]
    },
        {
      "id": 8,
      "title": "Personal Blog Platform",
      "description": "A Django-based blog with SEO, comment system, and admin dashboard.",
      "technologies": ["Django", "Python", "PostgreSQL", "SEO"],
      "github": "#",
      "demo": "#",
      "category": "Full-Stack",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Rich text editor",
        "Comment moderation",
        "SEO-friendly URLs",
        "Admin content management"
      ]
    },
        {
      "id": 9,
      "title": "VidSnap AI",
      "description": "A Flask web app to generate video reels from images and text with TTS integration.",
      "technologies": ["Flask", "Python", "CSS", "HTML", "JavaScript"],
      "github": "https://github.com/dimriutkarsh/VidSnap",
      "demo": "",
      "category": "Backend",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Create video reels from images and text",
        "Text-to-speech integration using ElevenLabs API",
        "Simple and creative interface"
      ]
    },
        {
      "id": 10,
      "title": "YogFit",
      "description": "An exercise info app providing workout suggestions and fitness tracking.",
      "technologies": ["CSS", "HTML", "JavaScript"],
      "github": "https://github.com/dimriutkarsh/ExerciseInfo",
      "demo": "https://dimriutkarsh.github.io/ExerciseInfo/",
      "category": "Frontend",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Exercise information by category",
        "Daily exercise schedules",
        "Fitness record tracking"
      ]
    },
        {
      "id": 11,
      "title": "Interactive Analytics Dashboard",
      "description": "Real-time analytics dashboard with interactive charts and data export features.",
      "technologies": ["Flask", "Chart.js", "Python", "Analytics"],
      "github": "#",
      "demo": "#",
      "category": "Full-Stack",
      "status": "Completed",
      "year": "2024",
      "features": [
        "Real-time data visualization",
        "Interactive charts and graphs",
        "Data filtering and export",
        "Responsive dashboard design"
      ]
    }
    ],
    "journey": [
  {
    "year": "2025",
    "title": "AI/ML Developer & Full-Stack Project Builder",
    "company": "Self-Driven Projects",
    "description": "Currently learning Deep Learning, Data Science, and Cloud Computing while building AI-powered applications and dashboards.",
    "technologies": ["Python", "NumPy", "Flask", "Django", "AI APIs", "AWS"],
    "achievements": [
      "Created AI projects like DeepShiva, VidSnap, and Analytics Dashboard",
      "Integrated AI tools and APIs for image generation and text extraction",
      "Learning Deep Learning (neural networks, transformers), data visualization,"
    ]
  },
  {
    "year": "2024",
    "title": "Frontend Developer & Python Programmer",
    "company": "Personal Learning & Projects",
    "description": "Started my coding journey with HTML, CSS, JavaScript, and Python — gradually moved into Flask and Django for full-stack applications.",
    "technologies": ["HTML", "CSS", "JavaScript", "Python"],
    "achievements": [
      "Built projects like VanRakshak, NotesNest, EduHub, and YogFit",
      "Learned frontend design principles and responsive layouts",
      "Started working with AI APIs and automation scripts"
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