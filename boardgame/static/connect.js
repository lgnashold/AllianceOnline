console.log("connected");

var socket = io.connect();

//when you recieve a message append it to the log

socket.on("update_board",function(msg) {
  console.log("ran");
  if(msg.room == "{{join_code}}") {
    console.log("recieved: " + msd);
    boardPos = JSON.parse(msg.board);
    console.log(boardPos);
    draw_board();
  }
});

socket.on('message', function(msg) {
    if(msg.room == "{{join_code}}") {
      $('#log').append('<p>Received: ' + msg.data + '</p>');
    }
});

function change_team(teamToChange) {
  socket.emit('change_team', {team: teamToChange});
}

function endTurn() {
  socket.emit('end_turn');
}

function makeMove(iPos,jPos) {
  socket.emit('make_move', {i:iPos,j:jPos});
}
