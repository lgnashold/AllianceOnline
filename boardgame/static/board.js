var centerX = 0;
var centerY = 0;
var boardPos =[];

var ctx;

var c = document.getElementById("gameCanvas");
var ctx = c.getContext("2d");

console.log($("#info").outerHeight( true ));
ctx.canvas.width  = window.innerWidth - 16;
ctx.canvas.height = window.innerHeight - $("#info").outerHeight( true ) - 30;

var WIDTH = ctx.canvas.width;
var HEIGHT = ctx.canvas.height;
var GRID_SIZE = 300;

draw_board();

var isDragging = false;
var initMosPos;
$(document).mousedown(function(e) {
  isDragging = true;
  initMosPos = getMousePos(c,e);
  //console.log(initMosPos)
});

$(document).mouseup(function(e) {
  isDragging = false;
  gridSquare = get_col(getMousePos(c,e));
  if(gridSquare.i != -1) {
    console.log(gridSquare.i)
  }
});

$(document).mousemove(function(e) {
  //console.log(isDragging);
  if(isDragging) {
    finalMosPos = getMousePos(c,e);
    //console.log(finalMosPos.x - initMosPos.x);
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

function get_col(mousePos) {
  for(var i = 0; i < boardPos.length; i++) {
    for(var j = 0; j < boardPos[i].length; j++) {
      if(mousePos.x > (j*GRID_SIZE + centerX) && mousePos.x < (j*GRID_SIZE + centerX) + GRID_SIZE
        && mousePos.y > i*GRID_SIZE+centerY && mousePos.y < i*GRID_SIZE+centerY + GRID_SIZE) {
          return {i:i,j:j};
        }
    }
  }
  return {i:-1,j:-1};
}

function draw_board() {
  ctx.fillStyle = "lightgray";
  ctx.fillRect(0,0,WIDTH,HEIGHT);
  for(var i = 0; i < boardPos.length; i++) {
    for(var j = 0; j < boardPos[i].length; j++) {
      console.log(boardPos[i][j].color);
      ctx.fillStyle = boardPos[i][j].color;
      ctx.strokeStyle = "black";
      ctx.lineWidth = 5;
      ctx.fillRect(j*GRID_SIZE + centerX,i*GRID_SIZE+centerY,GRID_SIZE,GRID_SIZE);
      ctx.strokeRect(j*GRID_SIZE + centerX,i*GRID_SIZE+centerY,GRID_SIZE,GRID_SIZE);
    }
  }
}
