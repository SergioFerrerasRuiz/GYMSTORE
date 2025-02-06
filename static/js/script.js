let chatHistory = [];

$(document).ready(function() {
    loadChatHistory();
    $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
});

function loadChatHistory() {
    let chatHistoryHtml = '';
    chatHistory.forEach(message => {
        chatHistoryHtml += `
            <div class="flex justify-end">
                <div class="bg-gray-600 text-white p-3 rounded-xl max-w-xs text-sm font-medium shadow-md">
                    <strong>Tú:</strong> ${message.user_question}
                </div>
            </div>
            <div class="flex justify-start">
                <div class="bg-gray-700 p-3 rounded-xl max-w-xs text-sm font-medium shadow-md">
                    <ul>
                        <li><strong>ChatBot:</strong> ${message.answer}</li>
                    </ul>
                </div>
            </div>
        `;
    });
    $('#chat-response').html(chatHistoryHtml);
}

$('#chat-form').on('submit', function(e) {
    e.preventDefault();
    const loadingCircle = document.querySelector('#loading-circle');
    loadingCircle.classList.remove('hidden');

    const userQuestion = $('#chat-input').val();

    $.ajax({
        type: 'POST',
        url: '/ask',
        contentType: 'application/json',
        data: JSON.stringify({ question: userQuestion }),
        success: function(response) {
            loadingCircle.classList.add('hidden');
            let answer = response && response.length > 0 ? response[0].answer : '';
            chatHistory.push({ user_question: userQuestion, answer: answer });
            loadChatHistory();
            $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            $('#chat-input').val('');
        },
        error: function(xhr, errmsg, err) {
            console.error("Error en AJAX: ", errmsg);
            loadingCircle.classList.add('hidden');
        }
    });
});

$('#clear-chat').on('click', function() {
    chatHistory = [];
    $('#chat-response').html('');
});
