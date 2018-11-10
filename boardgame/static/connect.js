console.log("connected");

var socket = io.connect();

//when you recieve a message append it to the log

socket.on("update_board",function(msd) {
  console.log("recieved: " + msd);
  boardPos = JSON.parse(msd);
  console.log(boardPos);
  draw_board();
});
