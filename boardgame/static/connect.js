var socket = io.connect();

//when you recieve a message append it to the log
socket.on('response', function(msg) {
    if(msg.room == "{{join_code}}") {
      $('#log').append('<p>Received: ' + msg.data + '</p>');
    }
});

//emit move data to server on button press
function move(type) {
    socket.emit('made_move', {data: type});
    return false;
}
