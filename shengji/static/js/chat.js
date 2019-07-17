$(function() {
    var scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
    var socket = new ReconnectingWebSocket(scheme + '://' + window.location.host + '/chat' + window.location.pathname);

    socket.onmessage = function(message) {
        var payload = JSON.parse(message.data);
        var chatMessage = $('<p></p>').text(payload.message).addClass('chat-message')
        $('#chat-stream').append(chatMessage);
    };

    $('#chat-input').on('submit', function() {
        var payload = {
            message: $(this).find('input[name="message"]').val(),
        }
        socket.send(JSON.stringify(payload));
        $(this).find('input[name="message"]').val('').focus();
        return false;
    });
});
