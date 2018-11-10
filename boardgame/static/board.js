var centerX = 0;
var centerY = 0;
var boardPos = [[{color:"#ff0000"},{color:"#00ff00"}, {color:"#ff0000"}],[{color:"#00ff00"},{color:"#00ff00"},{color:"#ff0000"}],[{color:"#ff0000"},{color:"#ff0000"},{color:"#ff0000"}]];

var ctx;

var c = document.getElementById("gameCanvas");
var ctx = c.getContext("2d");

ctx.canvas.width  = window.innerWidth - 16;
ctx.canvas.height = window.innerHeight - document.getElementById("info").offsetHeight - 22;

var WIDTH = ctx.canvas.width;
var HEIGHT = ctx.canvas.height;
var GRID_SIZE = 300;

draw_board();

var isDragging = false;
var initMosPos;
$(document).mousedown(function(e) {
  isDragging = true;
  initMosPos = getMousePos(c,e);
  console.log(initMosPos)
});

$(document).mouseup(function(e) {
  isDragging = false;
});

$(document).mousemove(function(e) {
  console.log(isDragging);
  if(isDragging) {
    finalMosPos = getMousePos(c,e);
    console.log(finalMosPos.x - initMosPos.x);
    centerX += (finalMosPos.x - initMosPos.x);
    centerY += (finalMosPos.y - initMosPos.y);
    initMosPos = finalMosPos;

    draw_board();
  }
});

function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
}

function draw_board() {
  ctx.fillStyle = "lightgray";
  ctx.fillRect(0,0,WIDTH,HEIGHT);
  for(var i = 0; i < boardPos.length; i++) {
    for(var j = 0; j < boardPos[i].length; j++) {
      console.log(boardPos[i][j].color);
      ctx.fillStyle = boardPos[i][j].color;
      ctx.fillRect(j*GRID_SIZE + centerX,i*GRID_SIZE+centerY,GRID_SIZE,GRID_SIZE);
    }
  }
}
