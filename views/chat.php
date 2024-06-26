<?php
include '../loader/init.php';
Session::AuthViews();
?>
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
            border-right: 1px solid #ddd;
            z-index: 1050;
            transition: transform 0.3s ease, width 0.3s ease, border-radius 0.3s ease;
            display: flex;
            flex-direction: column;
        }

        .sidebar.collapsed {
            transform: translateX(-100%);
        }

        .sidebar.open {
            transform: translateX(0);
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
                width: 100vw;
                height: 100vh;
                border-radius: 0;
                transform: translateX(-100%);
            }

            .sidebar.open {
                transform: translateX(0);
                border-radius: 16px !important;
                padding: 0;
            }

            .chat-container {
                padding: 0;
                width: 100vw;
            }

            .chat-card {
                border-radius: 0;
                height: 100vh;
                margin: 0;
                width: 100vw;
            }

            .no-gutters {
                margin-right: 0;
                margin-left: 0;
            }

            .no-gutters>.col,
            .no-gutters>[class*="col-"] {
                padding-right: 0;
                padding-left: 0;
            }
        }

        .user-name {
            padding: 15px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #ddd;
        }

        .conversation-list {
            flex: 1;
            overflow-y: auto;
        }

        .logout-button {
            padding: 15px;
            background-color: #f8f9fa;
            border-top: 1px solid #ddd;
        }

        .close-sidebar-btn {
            display: none;
            cursor: pointer;
            font-size: 1.5rem;
            padding: 15px;
            text-align: right;
        }

        @media (max-width: 768px) {
            .close-sidebar-btn {
                display: block;
            }
        }
    </style>
</head>

<body>
    <div class="container-fluid p-0">
        <div class="row no-gutters">
            <div class="col-md-3 col-lg-3 col-xl-3 sidebar" id="sidebar">
                <div class="close-sidebar-btn" id="close-sidebar">
                    <i class="fas fa-times"></i>
                </div>
                <div class="user-name">
                    <strong>Hi <?php echo $_SESSION['name']; ?></strong>
                </div>
                <div class="conversation-list" id="conversation-list">
                    <!-- Previous conversations will be loaded here -->
                </div>
                <div class="logout-button">
                    <a href="logout" class="btn btn-danger btn-block">Logout</a>
                </div>
            </div>
            <div class="col-12 col-md-9 offset-md-3 chat-container">
                <section>
                    <div class="container-fluid p-0">
                        <div class="row no-gutters">
                            <div class="col-12">
                                <div class="card chat-card" id="chat1" style="height: 100vh;margin-right:7%">
                                    <div class="card-header d-flex justify-content-between align-items-center p-3 bg-info text-white border-bottom-0"
                                        style="border-top-left-radius: 15px; border-top-right-radius: 15px;">
                                        <p class="mb-0 fw-bold d-none d-md-block">Live chat</p>
                                        <i class="fas fa-bars toggle-button d-md-none" id="open-sidebar"></i>
                                        <button id="clear-chat" class="btn btn-info">New Chat</button>
                                    </div>
                                    <div class="card-body" id="chat-body">
                                        <!-- Chat messages will be inserted here -->
                                    </div>
                                    <div
                                        class="card-footer text-muted d-flex justify-content-start align-items-center p-3">
                                        <div class="chat-input-container">
                                            <textarea class="form-control" id="chat-input" placeholder="Type message"
                                                aria-label="Recipient's username" aria-describedby="button-addon2"
                                                rows="1"></textarea>
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
        document.addEventListener('DOMContentLoaded', function () {
            const textarea = document.querySelector('textarea');
            const sendIcon = document.querySelector('.send-icon');
            const chatBody = document.getElementById('chat-body');
            const clearChatButton = document.getElementById('clear-chat');
            const sidebar = document.getElementById('sidebar');
            const openSidebarButton = document.getElementById('open-sidebar');
            const closeSidebarButton = document.getElementById('close-sidebar');
            const userId = '<?php echo $_SESSION['user_id']; ?>';

            textarea.addEventListener('input', function () {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
                this.style.overflowY = this.scrollHeight > parseInt(window.getComputedStyle(this).maxHeight) ? 'auto' : 'hidden';
            });

            sendIcon.addEventListener('click', function () {
                const message = textarea.value;
                if (message.trim() !== '') {
                    sendMessage(message);
                    textarea.value = '';
                    textarea.style.height = 'auto';
                    textarea.style.overflowY = 'hidden';
                }
            });

            clearChatButton.addEventListener('click', function () {
                clearChat();
            });

            openSidebarButton.addEventListener('click', function () {
                sidebar.classList.add('open');
            });

            closeSidebarButton.addEventListener('click', function () {
                sidebar.classList.remove('open');
            });

            function sendMessage(message) {
                appendMessage('You', message, '../assets/images/human.jpg');
                showThinking();

                fetch('http://localhost:5000/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message, user_id: userId })
                })
                    .then(response => response.json())
                    .then(data => {
                        hideThinking();
                        appendMessage('Bot', data.response, '../assets/images/aibot.avif');
                    })
                    .catch(error => console.error('Error:', error));
            }

            function clearChat() {
                fetch('http://localhost:5000/clear', { method: 'POST' })
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
                    <p class="small mb-0">${message}</p>
                </div>
            `;
                chatBody.appendChild(messageElement);
                chatBody.scrollTop = chatBody.scrollHeight;
            }


            function showThinking() {
                const thinkingElement = document.createElement('div');
                thinkingElement.classList.add('thinking');
                thinkingElement.innerHTML = `<img src="../assets/images/chat.gif" alt="Thinking..." class="thinking-gif">`;
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
                fetch(`http://localhost:5000/conversations?user_id=${userId}`)
                    .then(response => response.json())
                    .then(data => {
                        const conversationList = document.getElementById('conversation-list');
                        conversationList.innerHTML = '';
                        data.forEach(conversation => {
                            const item = document.createElement('div');
                            item.classList.add('sidebar-item');
                            item.dataset.chatId = conversation[0];

                            const titleSpan = document.createElement('span');
                            titleSpan.textContent = conversation[1];
                            titleSpan.addEventListener('click', function () {
                                loadConversation(item.dataset.chatId);
                                if (window.innerWidth <= 768) {
                                    sidebar.classList.remove('open');
                                }
                            });

                            const trashIcon = document.createElement('i');
                            trashIcon.classList.add('fas', 'fa-trash', 'trash-icon');
                            trashIcon.addEventListener('click', function (event) {
                                event.stopPropagation();
                                deleteConversation(item.dataset.chatId);
                            });

                            item.appendChild(titleSpan);
                            item.appendChild(trashIcon);
                            conversationList.appendChild(item);
                        });
                    })
                    .catch(error => {
                        console.error('Error loading conversations:', error);
                    });
            }

            function loadConversation(chat_id) {
                fetch(`http://localhost:5000/conversation/${chat_id}?user_id=${userId}`)
                    .then(response => response.json())
                    .then(data => {
                        chatBody.innerHTML = '';
                        data.chat_history.forEach(message => {
                            appendMessage(message.sender, message.content, message.sender === 'User' ? '../assets/images/human.jpg' : '../assets/images/aibot.avif');
                        });
                    })
                    .catch(error => console.error('Error loading conversation:', error));
            }

            function deleteConversation(chat_id) {
                fetch(`http://localhost:5000/delete_conversation/${chat_id}?user_id=${userId}`, { method: 'DELETE' })
                    .then(response => response.json())
                    .then(data => {
                        loadConversations();
                    })
                    .catch(error => console.error('Error deleting conversation:', error));
            }

            loadConversations();
        });
    </script>
</body>

</html>
