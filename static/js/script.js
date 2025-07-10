// Enhanced Terminal Portfolio JavaScript

class TerminalPortfolio {
    constructor() {
        this.commandHistory = [];
        this.historyIndex = -1;
        this.isTyping = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createMatrixRain();
        this.startBootSequence();
        this.setupAnimations();
    }

    setupEventListeners() {
        const terminalForm = document.getElementById('terminal-form');
        const terminalInput = document.getElementById('terminal-input');
        const terminalContent = document.getElementById('terminal-content');

        if (terminalForm) {
            terminalForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const command = terminalInput.value.trim();
                if (command && !this.isTyping) {
                    this.processCommand(command);
                    terminalInput.value = '';
                }
            });
        }

        if (terminalInput) {
            terminalInput.addEventListener('keydown', (e) => {
                this.handleKeyDown(e);
            });

            // Keep terminal focused
            document.addEventListener('click', (e) => {
                if (!e.target.closest('a') && !e.target.closest('button') && !e.target.closest('.profile-card')) {
                    terminalInput.focus();
                }
            });
        }

        // Setup profile card interactions
        const profileCard = document.getElementById('profile-card');
        if (profileCard) {
            profileCard.addEventListener('click', () => {
                this.toggleProfileCard();
            });
        }

        // Setup profile title click
        const profileTitle = document.querySelector('.profile-title');
        if (profileTitle) {
            profileTitle.addEventListener('click', (e) => {
                e.stopPropagation();
                window.location.href = '/about';
            });
        }
    }

    handleKeyDown(e) {
        const terminalInput = document.getElementById('terminal-input');
        
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (this.historyIndex < this.commandHistory.length - 1) {
                this.historyIndex++;
                terminalInput.value = this.commandHistory[this.commandHistory.length - 1 - this.historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (this.historyIndex > 0) {
                this.historyIndex--;
                terminalInput.value = this.commandHistory[this.commandHistory.length - 1 - this.historyIndex];
            } else if (this.historyIndex === 0) {
                this.historyIndex = -1;
                terminalInput.value = '';
            }
        } else if (e.key === 'Tab') {
            e.preventDefault();
            this.handleTabCompletion(terminalInput);
        }
    }

    handleTabCompletion(input) {
        const commands = ['help', 'about', 'projects', 'skills', 'journey', 'contact', 'resume', 'ls', 'cat', 'clear', 'date', 'pwd', 'tree'];
        const currentValue = input.value.toLowerCase();
        
        if (currentValue) {
            const matches = commands.filter(cmd => cmd.startsWith(currentValue));
            if (matches.length === 1) {
                input.value = matches[0];
            } else if (matches.length > 1) {
                this.displayOutput(`\nPossible commands: ${matches.join(', ')}\n`);
            }
        }
    }

    processCommand(command) {
        this.commandHistory.push(command);
        this.historyIndex = -1;
        this.isTyping = true;

        // Display command with typewriter effect
        this.displayCommandWithTypewriter(command);

        // Process command via API
        fetch('/api/terminal/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: command })
        })
        .then(response => response.json())
        .then(data => {
            setTimeout(() => {
                this.handleCommandResponse(data);
                this.isTyping = false;
            }, 800);
        })
        .catch(error => {
            console.error('Error:', error);
            this.displayError('Network error occurred. Please try again.');
            this.isTyping = false;
        });
    }

    displayCommandWithTypewriter(command) {
        const terminalContent = document.getElementById('terminal-content');
        const commandDiv = document.createElement('div');
        commandDiv.className = 'terminal-output';
        commandDiv.innerHTML = `
            <div class="flex items-center mb-2">
                <span class="terminal-prompt">utkarsh@portfolio:~$ </span>
                <span class="command-text text-white ml-2">${command}</span>
            </div>
        `;
        terminalContent.appendChild(commandDiv);
        this.scrollToBottom();
    }

    handleCommandResponse(data) {
        const terminalContent = document.getElementById('terminal-content');

        if (data.output === 'CLEAR_TERMINAL') {
            terminalContent.innerHTML = '';
            this.displayWelcomeMessage();
            return;
        }

        const outputDiv = document.createElement('div');
        outputDiv.className = 'command-output animate-fade-in';

        if (data.redirect) {
            outputDiv.innerHTML = `<div class="success-output typewriter-output">${data.output}</div>`;
            terminalContent.appendChild(outputDiv);
            this.scrollToBottom();
            
            // Show loading animation
            setTimeout(() => {
                this.showLoadingAnimation();
            }, 1000);
            
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 2000);
        } else if (typeof data.output === 'object') {
            outputDiv.innerHTML = this.formatObjectOutput(data.output);
            terminalContent.appendChild(outputDiv);
        } else {
            outputDiv.innerHTML = `<div class="terminal-output typewriter-output">${data.output}</div>`;
            terminalContent.appendChild(outputDiv);
        }

        this.scrollToBottom();
    }

    formatObjectOutput(output) {
        switch (output.type) {
            case 'help':
                return this.formatHelpOutput(output.commands);
            case 'ls':
                return this.formatLsOutput(output.sections);
            case 'tree':
                return this.formatTreeOutput(output.structure);
            case 'file':
                return this.formatFileOutput(output.filename, output.content);
            default:
                return `<div class="terminal-output">${JSON.stringify(output)}</div>`;
        }
    }

    formatHelpOutput(commands) {
        let html = '<div class="terminal-output"><div class="text-cyan mb-3">Available Commands:</div>';
        html += '<div class="grid grid-cols-2 gap-2">';
        
        for (const [cmd, desc] of Object.entries(commands)) {
            html += `
                <div class="flex">
                    <span class="text-yellow font-semibold w-16">${cmd}</span>
                    <span class="text-gray-300 ml-2">${desc}</span>
                </div>
            `;
        }
        
        html += '</div></div>';
        return html;
    }

    formatLsOutput(sections) {
        return `
            <div class="terminal-output">
                <div class="text-cyan mb-2">Directory contents:</div>
                <div class="file-tree">
                    ${sections.map(section => {
                        const isDirectory = section.endsWith('/');
                        const className = isDirectory ? 'directory' : 'file';
                        const icon = isDirectory ? '📁' : '📄';
                        return `<div class="${className}">${icon} ${section}</div>`;
                    }).join('')}
                </div>
            </div>
        `;
    }

    formatTreeOutput(structure) {
        return `
            <div class="terminal-output">
                <div class="file-tree">
                    ${structure.map(line => `<div>${line}</div>`).join('')}
                </div>
            </div>
        `;
    }

    formatFileOutput(filename, content) {
        return `
            <div class="terminal-output">
                <div class="text-cyan mb-2">📄 ${filename}</div>
                <div class="bg-gray-900 p-4 rounded border-l-4 border-green-400">
                    <pre class="text-gray-300 whitespace-pre-wrap">${content}</pre>
                </div>
            </div>
        `;
    }

    displayError(message) {
        const terminalContent = document.getElementById('terminal-content');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-output animate-fade-in';
        errorDiv.innerHTML = `<div class="text-red typewriter-output">Error: ${message}</div>`;
        terminalContent.appendChild(errorDiv);
        this.scrollToBottom();
    }

    displayOutput(message) {
        const terminalContent = document.getElementById('terminal-content');
        const outputDiv = document.createElement('div');
        outputDiv.className = 'terminal-output animate-fade-in';
        outputDiv.innerHTML = message;
        terminalContent.appendChild(outputDiv);
        this.scrollToBottom();
    }

    showLoadingAnimation() {
        const terminalContent = document.getElementById('terminal-content');
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'terminal-output animate-fade-in';
        loadingDiv.innerHTML = `
            <div class="flex items-center">
                <div class="loading mr-2"></div>
                <span class="text-cyan">Loading...</span>
            </div>
        `;
        terminalContent.appendChild(loadingDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        const terminalContent = document.getElementById('terminal-content');
        if (terminalContent) {
            terminalContent.scrollTop = terminalContent.scrollHeight;
        }
    }

    toggleProfileCard() {
        const profileCard = document.getElementById('profile-card');
        if (profileCard) {
            profileCard.classList.toggle('expanded');
        }
    }

    startBootSequence() {
        const terminalContent = document.getElementById('terminal-content');
        if (terminalContent) {
            this.displayWelcomeMessage();
        }
    }

    displayWelcomeMessage() {
        const welcomeMessage = `
            <div class="animate-typewriter">
                <div class="text-green-400 mb-4">
                    ╔═══════════════════════════════════════════════════════════════════════════════╗
                    ║                        Welcome to Terminal Portfolio v2.0                     ║
                    ║                               Utkarsh Dimri                                  ║
                    ║                            AI/ML Engineer                                    ║
                    ╚═══════════════════════════════════════════════════════════════════════════════╝
                </div>
                <div class="text-cyan mb-2">System initialized successfully...</div>
                <div class="text-yellow mb-2">Type 'help' to see available commands</div>
                <div class="text-gray-400 mb-4">Use TAB for command completion, UP/DOWN arrows for history</div>
                <div class="text-green-400">Ready for input.</div>
            </div>
        `;
        
        const terminalContent = document.getElementById('terminal-content');
        if (terminalContent) {
            terminalContent.innerHTML = welcomeMessage;
        }
    }

    setupAnimations() {
        // Setup intersection observer for animations
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        });

        animatedElements.forEach(element => {
            observer.observe(element);
        });

        // Setup skill bar animations
        const skillBars = document.querySelectorAll('.skill-progress-fill');
        const skillObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const width = entry.target.getAttribute('data-width');
                    if (width) {
                        entry.target.style.width = width + '%';
                    }
                }
            });
        });

        skillBars.forEach(bar => {
            skillObserver.observe(bar);
        });
    }

    createMatrixRain() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.className = 'matrix-rain';
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '-1';
        canvas.style.opacity = '0.1';
        
        document.body.appendChild(canvas);
        
        const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()_+-=[]{}|;:,.<>?";
        const matrixArray = matrix.split("");
        
        const fontSize = 10;
        const columns = canvas.width / fontSize;
        
        const drops = [];
        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }
        
        const draw = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#00ff00';
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        };
        
        setInterval(draw, 35);
        
        // Resize handler
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }

    // Utility functions
    typeWriter(element, text, speed = 50) {
        let i = 0;
        element.innerHTML = '';
        
        const type = () => {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        };
        
        type();
    }

    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    generateId() {
        return Math.random().toString(36).substr(2, 9);
    }
}

// Initialize the terminal portfolio when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.terminalPortfolio = new TerminalPortfolio();
});

// Export for use in other scripts
window.TerminalPortfolio = TerminalPortfolio;