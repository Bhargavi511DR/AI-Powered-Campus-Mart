// AI Chat Functionality
class AIChat {
    constructor() {
        this.chatContainer = document.getElementById('ai-chat-container');
        this.messageInput = document.getElementById('ai-message-input');
        this.sendButton = document.getElementById('ai-send-btn');
        this.quickQuestions = document.querySelectorAll('.quick-question');
        
        this.init();
    }

    init() {
        // Event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Quick question buttons
        this.quickQuestions.forEach(button => {
            button.addEventListener('click', () => {
                const question = button.getAttribute('data-question');
                this.messageInput.value = question;
                this.sendMessage();
            });
        });

        // Auto-focus on input
        this.messageInput.focus();
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send message to backend AI agent
            const response = await fetch('/ai-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            if (data.success) {
                this.addMessage(data.response, 'ai');
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'ai');
            }

        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage('Sorry, I\'m having trouble connecting. Please check your internet connection.', 'ai');
        }
    }

    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ${sender}-message fade-in`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'ai' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (sender === 'ai') {
            messageContent.innerHTML = `<strong>AI Assistant:</strong> ${this.formatResponse(content)}`;
        } else {
            messageContent.innerHTML = `<strong>You:</strong> ${content}`;
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        this.chatContainer.appendChild(messageDiv);

        // Scroll to bottom
        this.scrollToBottom();
    }

    formatResponse(response) {
        // Convert line breaks to HTML
        return response.replace(/\n/g, '<br>');
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'ai-message';
        typingDiv.id = 'typing-indicator';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    AI Assistant is typing
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;

        this.chatContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
}

// Initialize AI Chat when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('ai-chat-container')) {
        new AIChat();
    }
});