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

    const aliens = [];
    const rows = 3;
    const cols = 5;
    const alienWidth = 40;
    const alienHeight = 20;
    const alienPadding = 10;
    const alienOffsetTop = 30;
    const alienOffsetLeft = 30;
    let alienDirection = 1; // エイリアンの移動方向（1: 右, -1: 左）
    let alienMoveCounter = 0; // エイリアンの移動カウンター

    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const alienX = col * (alienWidth + alienPadding) + alienOffsetLeft;
        const alienY = row * (alienHeight + alienPadding) + alienOffsetTop;
        aliens.push({ x: alienX, y: alienY, width: alienWidth, height: alienHeight, color: 'green' });
      }
    }

    const bullets = [];

    function drawPlayer() {
      context.fillStyle = player.color;
      context.fillRect(player.x, player.y, player.width, player.height);
    }

    function drawAliens() {
      aliens.forEach(alien => {
        context.fillStyle = alien.color;
        context.fillRect(alien.x, alien.y, alien.width, alien.height);
      });
    }

    function drawBullets() {
      bullets.forEach(bullet => {
        context.fillStyle = bullet.color;
        context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
      });
    }

    function clear() {
      context.clearRect(0, 0, canvas.width, canvas.height);
    }

    function update() {
      const now = Date.now();
      clear();
      drawPlayer();
      drawAliens();
      drawBullets();
      player.x += player.dx;

      if (player.x < 0) {
        player.x = 0;
      }
      if (player.x + player.width > canvas.width) {
        player.x = canvas.width - player.width;
      }

      // 弾丸を更新
      bullets.forEach((bullet, bulletIndex) => {
        bullet.y -= bullet.dy;
        if (bullet.y + bullet.height < 0) {
          bullets.splice(bulletIndex, 1); // 画面外に出た弾丸を削除
        } else {
          // エイリアンとの衝突判定
          aliens.forEach((alien, alienIndex) => {
            if (checkCollision(bullet, alien)) {
              bullets.splice(bulletIndex, 1); // 弾丸を削除
              aliens.splice(alienIndex, 1); // エイリアンを削除
            }
          });
        }
      });

      // エイリアンを同じ方向に動かす
      alienMoveCounter++;
      if (alienMoveCounter % 30 === 0) { // 30フレームごとにエイリアンを動かす
        let changeDirection = false;
        aliens.forEach(alien => {
          alien.x += alienDirection * 10; // 10ピクセルずつ動かす
          if (alien.x < 0 || alien.x + alien.width > canvas.width) {
            changeDirection = true;
          }
        });

        if (changeDirection) {
          alienDirection *= -1; // 方向を反転
          aliens.forEach(alien => {
            alien.y += alienHeight + alienPadding; // エイリアンを下に移動
          });
        }
      }

      if (keys[' '] && now - lastShootTime > 500) { // 0.5秒間隔で弾を発射
        shoot();
        lastShootTime = now;
      }

      requestAnimationFrame(update);
    }

    function moveRight() {
      player.dx = player.speed;
    }

    function moveLeft() {
      player.dx = -player.speed;
    }

    function shoot() {
      const bullet = {
        x: player.x + player.width / 2 - 2.5,
        y: player.y,
        width: 5,
        height: 10,
        color: 'red',
        dy: 5
      };
      bullets.push(bullet);
    }

    const checkCollision = (bullet, alien) => {
      return (
        bullet.x < alien.x + alien.width &&
        bullet.x + bullet.width > alien.x &&
        bullet.y < alien.y + alien.height &&
        bullet.y + bullet.height > alien.y
      );
    };

    const keys = {};
    let lastShootTime = 0;

    const keyDown = (e) => {
      keys[e.key] = true;
      if (keys['ArrowRight'] || keys['Right']) {
        moveRight();
      } else if (keys['ArrowLeft'] || keys['Left']) {
        moveLeft();
      }
    };

    const keyUp = (e) => {
      keys[e.key] = false;
      if (!keys['ArrowRight'] && !keys['Right'] && !keys['ArrowLeft'] && !keys['Left']) {
        player.dx = 0;
      } else if (keys['ArrowRight'] || keys['Right']) {
        moveRight();
      } else if (keys['ArrowLeft'] || keys['Left']) {
        moveLeft();
      }
    };

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