var centerX = 0;
var centerY = 0;
var boardPos =[];

var board_color = "lightgray";
var ctx;

var c = document.getElementById("gameCanvas");
var ctx = c.getContext("2d");

ctx.canvas.width  = window.innerWidth - $("#info").outerWidth( true ) - 39;
ctx.canvas.height = window.innerHeight - 20;

$(document).ready(function(){
  $(window).resize(function(){
    ctx.canvas.width  = window.innerWidth - $("#info").outerWidth( true ) - 39;
    ctx.canvas.height = window.innerHeight - 20;
    draw_board();
  });
});

var WIDTH = ctx.canvas.width;
var HEIGHT = ctx.canvas.height;
var GRID_SIZE = 50;

draw_board();

var isDragging = false;
var shouldPlace = true;
var initMosPos;
$("#gameCanvas").mousedown(function(e) {
  isDragging = true;
  shouldPlace = true;
  initMosPos = getMousePos(c,e);
  //console.log(initMosPos)
});

$("#gameCanvas").mouseup(function(e) {
  isDragging = false;
  gridSquare = get_col(getMousePos(c,e));
  if(gridSquare.i != -1 && shouldPlace) {
    makeMove(gridSquare.i,gridSquare.j);
    //console.log(gridSquare.i + " " + gridSquare.j)
  }
});

$("#gameCanvas").mousemove(function(e) {
  //console.log(isDragging);
  if(isDragging) {
    shouldPlace = false;
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
  ctx.fillStyle = board_color;
  ctx.fillRect(0,0,WIDTH,HEIGHT);
  for(var i = 0; i < boardPos.length; i++) {
    for(var j = 0; j < boardPos[i].length; j++) {

      ctx.fillStyle = boardPos[i][j].color;
      ctx.strokeStyle = "black";
      ctx.lineWidth = 5;
      ctx.fillRect(j*GRID_SIZE + centerX,i*GRID_SIZE+centerY,GRID_SIZE,GRID_SIZE);
      ctx.strokeRect(j*GRID_SIZE + centerX,i*GRID_SIZE+centerY,GRID_SIZE,GRID_SIZE);
      if(boardPos[i][j].name != null) {
        console.log(boardPos[i][j].name);
        ctx.fillStyle = "black";
        ctx.fillText(boardPos[i][j].name,j*GRID_SIZE+centerX + GRID_SIZE/5,i*GRID_SIZE+centerY + GRID_SIZE/4);
      }

    }
  }
}

function set_board_color(color) {
  background_color(LightenDarkenColor(color,5));
}

/** CREDIT: https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors **/
function LightenDarkenColor(col,amt) {
    var usePound = false;
    if ( col[0] == "#" ) {
        col = col.slice(1);
        usePound = true;
    }

    var num = parseInt(col,16);

    var r = (num >> 16) + amt;

    if ( r > 255 ) r = 255;
    else if  (r < 0) r = 0;

    var b = ((num >> 8) & 0x00FF) + amt;

    if ( b > 255 ) b = 255;
    else if  (b < 0) b = 0;

    var g = (num & 0x0000FF) + amt;

    if ( g > 255 ) g = 255;
    else if  ( g < 0 ) g = 0;

    return (usePound?"#":"") + (g | (b << 8) | (r << 16)).toString(16);
}
