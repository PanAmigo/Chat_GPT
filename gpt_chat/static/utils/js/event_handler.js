// Funkcja, która wysyła pytanie do serwera i odbiera odpowiedź
function sendQuestion(my_question) {
    console.log("funkcja")
    const suffix = window.location.pathname.split('/').pop();
    console.log(suffix)
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: my_question, suffix: suffix })
    })
        .then(response => response.json())
        .then(data => {
                    console.log(data.answer);
                    if (data.answer === 'error') {
                window.location.href = "error_page.html";
                return;
                }
            // Dodanie wiadomości od AI do kontenera czatu
            const chatContainer = document.getElementById('chat-container');
            const aiMessage = document.createElement('div');
            aiMessage.classList.add('ai-message');
            aiMessage.innerText = data.answer;
            chatContainer.appendChild(aiMessage);
        });
}

// Funkcja, która obsługuje wysłanie pytania przez użytkownika
function handleSubmit(event) {
    const send_input = document.getElementById('send_input');
    send_input.setAttribute('disabled',true)
    event.preventDefault();
    const chatInput = document.getElementById('chat-input');
    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.innerText = chatInput.value;
    const chatContainer = document.getElementById('chat-container');
    chatContainer.appendChild(userMessage);
    sendQuestion(chatInput.value);
    chatInput.value = '';
    send_input.removeAttribute('disabled');
}

// Dodanie obsługi zdarzeń dla formularza czatu
const chatForm = document.getElementById('chat-form');
chatForm.addEventListener('submit', handleSubmit);


window.onload = function() {
  window.scrollTo(0, document.body.scrollHeight);
};