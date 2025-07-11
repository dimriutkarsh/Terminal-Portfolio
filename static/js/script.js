// Enhanced Terminal Portfolio JavaScript

class TerminalPortfolio {
    constructor() {
        this.commandHistory = [];
        this.historyIndex = -1;
        this.isTyping = false;
        this.particleCount = 0;
        this.maxParticles = 50;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createMatrixRain();
        this.startBootSequence();
        this.setupAnimations();
        this.initializeParticleSystem();
        this.setupAdvancedEffects();
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

            // Keep terminal focused with enhanced interaction
            document.addEventListener('click', (e) => {
                if (!e.target.closest('a') && !e.target.closest('button') && !e.target.closest('.profile-card')) {
                    terminalInput.focus();
                }
            });
        }

        // Profile title click
        const profileTitle = document.querySelector('.profile-title');
        if (profileTitle) {
            profileTitle.addEventListener('click', (e) => {
                e.stopPropagation();
                this.animatePageTransition('/about');
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
                this.displayOutput(`\n<span class="text-cyan">Possible commands:</span> ${matches.join(', ')}\n`);
            }
        }
    }

    processCommand(command) {
        this.commandHistory.push(command);
        this.historyIndex = -1;
        this.isTyping = true;

        // Display command
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
            this.animateTerminalClear();
            setTimeout(() => {
                terminalContent.innerHTML = '';
                this.displayWelcomeMessage();
            }, 300);
            return;
        }

        const outputDiv = document.createElement('div');
        outputDiv.className = 'command-output';

        if (data.redirect) {
            outputDiv.innerHTML = `<div class="success-output">${data.output}</div>`;
            terminalContent.appendChild(outputDiv);
            this.scrollToBottom();
            
            // Loading animation
            setTimeout(() => {
                this.showLoadingAnimation();
            }, 1000);
            
            setTimeout(() => {
                this.animatePageTransition(data.redirect);
            }, 2000);
        } else if (typeof data.output === 'object') {
            outputDiv.innerHTML = this.formatObjectOutput(data.output);
            terminalContent.appendChild(outputDiv);
        } else {
            outputDiv.innerHTML = `<div class="terminal-output">${data.output}</div>`;
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
        let html = '<div class="terminal-output"><div class="text-cyan mb-3 glow-text">Available Commands:</div>';
        html += '<div class="grid grid-cols-1 md:grid-cols-2 gap-3">';
        
        for (const [cmd, desc] of Object.entries(commands)) {
            html += `
                <div class="flex items-center p-2 rounded">
                    <span class="text-yellow font-semibold w-20 glow-text">${cmd}</span>
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
                <div class="text-cyan mb-3 glow-text">Directory contents:</div>
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
                <div class="text-cyan mb-3 glow-text">📄 ${filename}</div>
                <div class="bg-gray-900 p-4 rounded-lg border-l-4 border-green-400">
                    <pre class="text-gray-300 whitespace-pre-wrap">${content}</pre>
                </div>
            </div>
        `;
    }

    displayError(message) {
        const terminalContent = document.getElementById('terminal-content');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-output';
        errorDiv.innerHTML = `<div class="text-red">⚠️ Error: ${message}</div>`;
        terminalContent.appendChild(errorDiv);
        this.scrollToBottom();
    }

    displayOutput(message) {
        const terminalContent = document.getElementById('terminal-content');
        const outputDiv = document.createElement('div');
        outputDiv.className = 'terminal-output';
        outputDiv.innerHTML = message;
        terminalContent.appendChild(outputDiv);
        this.scrollToBottom();
    }

    showLoadingAnimation() {
        const terminalContent = document.getElementById('terminal-content');
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'terminal-output';
        loadingDiv.innerHTML = `
            <div class="flex items-center">
                <div class="loading mr-2"></div>
                <span class="text-cyan">Loading...</span>
            </div>
        `;
        terminalContent.appendChild(loadingDiv);
        this.scrollToBottom();
    }

    animatePageTransition(url) {
        window.location.href = url;
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
            this.createToggleParticles();
        }
    }

    startBootSequence() {
        const terminalContent = document.getElementById('terminal-content');
        if (terminalContent) {
            this.displayEnhancedWelcomeMessage();
        }
    }

    displayEnhancedWelcomeMessage() {
        const welcomeMessage = `
            <div>
                <div class="text-green-400 mb-4 glow-text">
                    ╔═══════════════════════════════════════════════════════════════════════════════╗
                    ║                     🚀 Welcome to Terminal Portfolio v2.0 🚀                 ║
                    ║                               Utkarsh Dimri                                  ║
                    ║                            AI/ML Engineer                                    ║
                    ╚═══════════════════════════════════════════════════════════════════════════════╝
                </div>
                <div class="text-cyan mb-2">System initialized successfully...</div>
                <div class="text-yellow mb-2">Loading modules...</div>
                <div class="text-purple mb-2">AI/ML framework loaded ✓</div>
                <div class="text-green-400 mb-2">Portfolio system ready ✓</div>
                <div class="text-gray-400 mb-4">Type 'help' to see available commands</div>
            </div>
        `;
        
        const terminalContent = document.getElementById('terminal-content');
        if (terminalContent) {
            terminalContent.innerHTML = welcomeMessage;
        }
    }

    displayWelcomeMessage() {
        this.displayEnhancedWelcomeMessage();
    }

    setupAnimations() {
        // Minimal animations setup
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
        
        const fontSize = 12;
        const columns = canvas.width / fontSize;
        
        const drops = [];
        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }
        
        const draw = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Create gradient effect
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#00ff00');
            gradient.addColorStop(0.5, '#00cc00');
            gradient.addColorStop(1, '#008800');
            
            ctx.fillStyle = gradient;
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                const x = i * fontSize;
                const y = drops[i] * fontSize;
                
                // Add glow effect
                ctx.shadowColor = '#00ff00';
                ctx.shadowBlur = 10;
                ctx.fillText(text, x, y);
                ctx.shadowBlur = 0;
                
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        };
        
        setInterval(draw, 35);
        
        // Enhanced resize handler
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
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

// Initialize enhanced terminal portfolio
document.addEventListener('DOMContentLoaded', () => {
    // Initialize terminal portfolio
    window.terminalPortfolio = new TerminalPortfolio();
});

// Export enhanced class
window.TerminalPortfolio = TerminalPortfolio;