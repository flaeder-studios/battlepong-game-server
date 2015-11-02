var BALL_EDGES = 32
var D_ANGLE = 2*Math.PI/BALL_EDGES

var xspd = 0.1;
var yspd = -0.5;
var xpos = 0.0
var ypos = 0.0
var radius = 0.05
var dt = 0.05
var gl

function createCircle(radius, xpos, ypos) {
  var angle = 0.0;
  arr = [xpos, ypos];
  for(var i = 2; i < 2*(BALL_EDGES + 1) + 2; i += 2) {
    arr[i] = radius*Math.cos(angle) + xpos;
    arr[i+1] = radius*Math.sin(angle) + ypos;
    angle += D_ANGLE;
  }
  return arr;
}

function drawCircle(radius, xpos, ypos) {

  // setup GLSL program
  var program = createProgramFromScripts(gl, ["2d-vertex-shader", "2d-fragment-shader"]);
  gl.useProgram(program);

  // Create a circle 
  arr = createCircle(radius, xpos, ypos);

  // look up where the vertex data needs to go.
  var positionLocation = gl.getAttribLocation(program, "a_position");

  var buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(arr), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(positionLocation);
  gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

  // draw
  gl.drawArrays(gl.TRIANGLE_FAN, 0, arr.length/2);

}

function handleCollision() {
    if(xpos + radius > 1) {
        xspd = -xspd
        xpos = 0.9999 - radius
    } else if(xpos - radius < -1) {
        xspd = -xspd
        xpos = -0.9999 + radius
    } else if(ypos + radius > 1) {
        yspd = -yspd
        ypos = 0.9999 - radius
    } else if(ypos - radius < -1) {
        yspd = -yspd
        ypos = -0.9999 + radius
    } else {
        // No bounce...
    }
}

function moveCircle() {
    handleCollision()
    xpos += xspd*dt
    ypos += yspd*dt
}

function action() {
  moveCircle()
  drawCircle(radius, xpos, ypos)
}

function main() {
  // Get A WebGL context
  var canvas = document.getElementById("canvas");
  gl = getWebGLContext(canvas);
  if (!gl) {
    return;
  }
  setInterval(action, dt*1000)
}

"use strict";
window.onload = main;
