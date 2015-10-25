var BALL_EDGES = 32
var D_ANGLE = 2*Math.PI/BALL_EDGES

function main() {
  // Get A WebGL context
  var canvas = document.getElementById("canvas");
  var gl = getWebGLContext(canvas);
  if (!gl) {
    return;
  }

  // setup GLSL program
  var program = createProgramFromScripts(gl, ["2d-vertex-shader", "2d-fragment-shader"]);
  gl.useProgram(program);

  // Create a circle 
  var angle = 0.0
  var arr = 
  arr = [0.0, 0.0]
  for(var i = 2; i < 2*(BALL_EDGES + 1) + 2; i += 2) {
    arr[i] = Math.cos(angle)
    arr[i+1] = Math.sin(angle)
    angle += D_ANGLE
  }

  // look up where the vertex data needs to go.
  var positionLocation = gl.getAttribLocation(program, "a_position");

  gl.clearColor(0.0, 0.0, 0.0, 1.0);

  // Create a buffer and put a single clipspace rectangle in
  // it (2 triangles)
  var buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(arr), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(positionLocation);
  gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

  // draw
  gl.drawArrays(gl.TRIANGLE_FAN, 0, arr.length/2);

  arr = [
        -1.0, -1.0,
        1.0, -1.0,
        -1.0,  1.0,
        -1.0,  1.0,
        1.0, -1.0,
        1.0,  1.0];

  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array(arr),
    gl.STATIC_DRAW);

    //gl.drawArrays(gl.TRIANGLE_FAN, 0, 6);
}

"use strict";
window.onload = main;
