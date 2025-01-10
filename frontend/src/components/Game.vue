<template>
  <canvas id="gameCanvas" width="800" height="600"></canvas>
</template>

<script>
export default {
  name: 'GameComponent',
  mounted() {
    const canvas = document.getElementById('gameCanvas');
    const context = canvas.getContext('2d');

    const player = {
      width: 50,
      height: 20,
      x: canvas.width / 2 - 25,
      y: canvas.height - 30,
      color: 'blue',
      speed: 5,
      dx: 0
    };

    function drawPlayer() {
      context.fillStyle = player.color;
      context.fillRect(player.x, player.y, player.width, player.height);
    }

    function clear() {
      context.clearRect(0, 0, canvas.width, canvas.height);
    }

    function update() {
      clear();
      drawPlayer();
      player.x += player.dx;

      if (player.x < 0) {
        player.x = 0;
      }
      if (player.x + player.width > canvas.width) {
        player.x = canvas.width - player.width;
      }

      requestAnimationFrame(update);
    }

    function moveRight() {
      player.dx = player.speed;
    }

    function moveLeft() {
      player.dx = -player.speed;
    }

    function keyDown(e) {
      if (e.key === 'ArrowRight' || e.key === 'Right') {
        moveRight();
      } else if (e.key === 'ArrowLeft' || e.key === 'Left') {
        moveLeft();
      }
    }

    function keyUp(e) {
      if (e.key === 'ArrowRight' || e.key === 'Right' || e.key === 'ArrowLeft' || e.key === 'Left') {
        player.dx = 0;
      }
    }

    document.addEventListener('keydown', keyDown);
    document.addEventListener('keyup', keyUp);

    update();
  }
};
</script>

<style>
canvas {
  background: black;
  display: block;
  margin: 0 auto;
}
</style>