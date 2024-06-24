<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <title>Chatbot Interface</title>
    <style>
        .chat-input-container {
            position: relative;
            width: 100%;
        }
        .chat-input-container textarea {
            width: 100%;
            height: auto;
            max-height: 150px;
            overflow-y: hidden;
            resize: none;
            padding-right: 50px;
            box-sizing: border-box;
        }
        .chat-input-container .send-icon {
            position: absolute;
            right: 15px;
            bottom: 10px;
            cursor: pointer;
            color: #17a2b8;
            font-size: 1.5rem;
        }
        #chat-body {
            height: calc(100vh - 160px);
            overflow-y: auto;
        }
        .thinking-gif {
            width: 50px;
            height: 50px;
        }
        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            height: 100%;
            width: 250px;
            background-color: rgba(248, 249, 250, 0.95);
            overflow-y: auto;
            border-right: 1px solid #ddd;
            z-index: 1050;
            transition: transform 0.3s ease, width 0.3s ease, border-radius 0.3s ease;
        }
        .sidebar.collapsed {
            transform: translateX(-100%);
        }
        .sidebar.open {
            width: 100%;
            border-radius: 15px;
        }
        .sidebar-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            cursor: pointer;
        }
        .sidebar-item:hover {
            background-color: #e9ecef;
        }
        .trash-icon {
            cursor: pointer;
            color: #dc3545;
        }
        .toggle-button {
            display: none;
            cursor: pointer;
            font-size: 1.5rem;
        }
        @media (max-width: 768px) {
            .toggle-button {
                display: block;
            }
            .sidebar {
                width: 100%;
                height: 100vh;
                border-radius: 0;
                transform: translateX(-100%);
            }
            .sidebar.open {
                transform: translateX(0);
                width: 100%;
                border-radius: 15px;
                padding-left: 7%;
                padding-right: 10%;
                margin-left: 5%;
                margin-right: 5%;
            }
            .chat-container {
                padding: 0;
                width: 100%;
            }
            .chat-card {
                border-radius: 0;
                height: 100vh;
                margin: 0;
                width: 100%;
            }
            .no-gutters {
                margin-right: 0;
                margin-left: 0;
            }
            .no-gutters > .col,
            .no-gutters > [class*="col-"] {
                padding-right: 0;
                padding-left: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row no-gutter">
            <div class="sidebar" id="sidebar">
                <div class="d-flex justify-content-end p-2">
                    <i class="fas fa-times toggle-button" id="close-sidebar"></i>
                </div>
                <!-- Previous conversations will be loaded here -->
            </div>
            <div class="col-md-9 offset-md-3 chat-container">
                <section>
                    <div class="container">
                        <div class="row d-flex justify-content-center">
                            <div class="col-md-8 col-lg-6 col-xl-4">
                                <div class="card chat-card" id="chat1" style="border-radius: 15px; height: 100vh;">
                                    <div class="card-header d-flex justify-content-between align-items-center p-3 bg-info text-white border-bottom-0"
                                        style="border-top-left-radius: 15px; border-top-right-radius: 15px;">
                                        <p class="mb-0 fw-bold d-none d-md-block">Live chat</p>
                                        <i class="fas fa-bars toggle-button d-md-none" id="open-sidebar"></i>
                                        <button id="clear-chat" class="btn btn-info">New Chat</button>
                                    </div>
                                    <div class="card-body" id="chat-body">
                                        <!-- Chat messages will be inserted here -->
                                    </div>
                                    <div class="card-footer text-muted d-flex justify-content-start align-items-center p-3">
                                        <div class="chat-input-container">
                                            <textarea class="form-control" id="chat-input" placeholder="Type message" aria-label="Recipient's username"
                                                aria-describedby="button-addon2" rows="1"></textarea>
                                            <i class="fas fa-paper-plane send-icon" id="button-addon2"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>
    <!-- Bootstrap JS (optional) -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const textarea = document.querySelector('textarea');
            const sendIcon = document.querySelector('.send-icon');
            const chatBody = document.getElementById('chat-body');
            const clearChatButton = document.getElementById('clear-chat');
            const sidebar = document.getElementById('sidebar');
            const openSidebarButton = document.getElementById('open-sidebar');
            const closeSidebarButton = document.getElementById('close-sidebar');

            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
                
                if (this.scrollHeight > parseInt(window.getComputedStyle(this).maxHeight)) {
                    this.style.overflowY = 'auto';
                } else {
                    this.style.overflowY = 'hidden';
                }
            });

            sendIcon.addEventListener('click', function() {
                const message = textarea.value;
                if (message.trim() !== '') {
                    sendMessage(message);
                    textarea.value = '';
                    textarea.style.height = 'auto';
                    textarea.style.overflowY = 'hidden';
                }
            });

            clearChatButton.addEventListener('click', function() {
                clearChat();
            });

            openSidebarButton.addEventListener('click', function() {
                sidebar.classList.add('open');
            });

            closeSidebarButton.addEventListener('click', function() {
                sidebar.classList.remove('open');
            });

            function sendMessage(message) {
                appendMessage('You', message, 'human.jpg');
                showThinking();
                
                fetch('http://localhost:5000/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    hideThinking();
                    appendMessage('Bot', data.response, 'aibot.avif');
                })
                .catch(error => console.error('Error:', error));
            }

            function clearChat() {
                fetch('http://localhost:5000/clear', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    chatBody.innerHTML = '';
                    loadConversations();
                })
                .catch(error => console.error('Error:', error));
            }

            function appendMessage(sender, message, avatar) {
                const messageElement = document.createElement('div');
                messageElement.classList.add('d-flex', 'flex-row', 'justify-content-start', 'mb-4');
                messageElement.innerHTML = `
                    <img src="${avatar}" alt="${sender} avatar" style="width: 45px; height: 100%;">
                    <div class="p-3 ms-3" style="border-radius: 15px; background-color: rgba(57, 192, 237,.2);">
                        <p class="small mb-0"><strong>${sender}:</strong> ${message}</p>
                    </div>
                `;
                chatBody.appendChild(messageElement);
                chatBody.scrollTop = chatBody.scrollHeight;
            }

            function showThinking() {
                const thinkingElement = document.createElement('div');
                thinkingElement.classList.add('thinking');
                thinkingElement.innerHTML = `
                    <img src="chat.gif" alt="Thinking..." class="thinking-gif">
                `;
                chatBody.appendChild(thinkingElement);
                chatBody.scrollTop = chatBody.scrollHeight;
            }

            function hideThinking() {
                const thinkingElement = chatBody.querySelector('.thinking');
                if (thinkingElement) {
                    chatBody.removeChild(thinkingElement);
                }
            }

            function loadConversations() {
                fetch('http://localhost:5000/conversations')
                .then(response => response.json())
                .then(data => {
                    sidebar.innerHTML = '<div class="d-flex justify-content-end p-2"><i class="fas fa-times toggle-button" id="close-sidebar"></i></div>';
                    data.forEach(conversation => {
                        const item = document.createElement('div');
                        item.classList.add('sidebar-item');
                        item.dataset.chatId = conversation[0];  // Assuming chat_id is at index 0

                        const titleSpan = document.createElement('span');
                        titleSpan.textContent = conversation[1];  // Assuming chat_title is at index 1
                        titleSpan.addEventListener('click', function() {
                            loadConversation(item.dataset.chatId);
                            if (window.innerWidth <= 768) {
                                sidebar.classList.remove('open');
                            }
                        });

                        const trashIcon = document.createElement('i');
                        trashIcon.classList.add('fas', 'fa-trash', 'trash-icon');
                        trashIcon.addEventListener('click', function(event) {
                            event.stopPropagation();
                            deleteConversation(item.dataset.chatId);
                        });

                        item.appendChild(titleSpan);
                        item.appendChild(trashIcon);
                        sidebar.appendChild(item);
                    });

                    document.getElementById('close-sidebar').addEventListener('click', function() {
                        sidebar.classList.remove('open');
                    });
                })
                .catch(error => console.error('Error:', error));
            }

            function loadConversation(chat_id) {
                fetch(`http://localhost:5000/conversation/${chat_id}`)
                .then(response => response.json())
                .then(data => {
                    chatBody.innerHTML = '';
                    data.chat_history.forEach(message => {
                        appendMessage(message.sender, message.content, message.sender === 'User' ? 'human.jpg' : 'aibot.avif');
                    });
                })
                .catch(error => console.error('Error:', error));
            }

            function deleteConversation(chat_id) {
                fetch(`http://localhost:5000/delete_conversation/${chat_id}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    loadConversations();
                })
                .catch(error => console.error('Error:', error));
            }

            loadConversations();
        });
    </script>
</body>
</html>
