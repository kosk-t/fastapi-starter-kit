<template>
  <div>
    <canvas id="gameCanvas" width="800" height="600"></canvas>
    <div v-if="isPaused" class="modal">
      <div class="modal-content">
        <span class="close" @click="resumeGame">&times;</span>
        <h2>設定</h2>
        <!-- 設定内容をここに追加 -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GameComponent',
  data() {
    return {
      isPaused: false,
      gameOver: false // ゲームオーバー状態を管理する変数
    };
  },
  mounted() {
    const canvas = document.getElementById('gameCanvas');
    const context = canvas.getContext('2d');
    const backgroundMusic = new Audio(require('@/assets/スペースインベーダー_BOSS_Inst.mp3')); // 音楽ファイルのパスを指定
    backgroundMusic.loop = true; // ループ再生

    const shootSound = new Audio(require('@/assets/shoot.mp3')); // 弾を撃つ効果音のパスを指定
    const hitSound = new Audio(require('@/assets/hit.mp3')); // 敵を倒した時の効果音のパスを指定

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
    const alienOffsetTop = 30; // エイリアンの開始位置を下端に近づける //todo テスト時は500, 元々は30なので、あとで修正
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
    const enemyBullets = []; // 敵の弾を管理する配列
    let score = 0; // スコアを管理する変数
    //let gameOver = false; // ゲームオーバー状態を管理する変数

    // 星を管理する配列
    const stars = [];
    const numStars = 100;

    // 星を初期化
    for (let i = 0; i < numStars; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 2,
        speed: Math.random() * 0.5 + 0.5
      });
    }

    function drawPlayer() {
      context.fillStyle = player.color;
      context.fillRect(player.x, player.y, player.width, player.height);
    }

    function drawAliens() {
      aliens.forEach(alien => {
        // エイリアンのピクセルデータ (縦縮めたバージョン)
        const pixelData = [
          [0, 1, 1, 0, 0, 1, 1, 0],
          [1, 0, 1, 1, 1, 1, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 0, 1, 1, 0, 1, 1],
          [0, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 0, 0, 0, 0, 1, 0],
          [1, 0, 1, 0, 0, 1, 0, 1],
          [0, 1, 0, 1, 1, 0, 1, 0]
        ];

        const blockWidth = alien.width / pixelData[0].length;
        const blockHeight = (alien.height / pixelData.length) * 0.9; // 高さを縮小

        // ピクセルを描画
        for (let row = 0; row < pixelData.length; row++) {
          for (let col = 0; col < pixelData[row].length; col++) {
            if (pixelData[row][col] === 1) {
              context.fillStyle = alien.color; // エイリアンの色
              context.fillRect(
                alien.x + col * blockWidth,
                alien.y + row * blockHeight,
                blockWidth,
                blockHeight
              );
            }
          }
        }
      });
    }



    function drawBullets() {
      bullets.forEach(bullet => {
        context.fillStyle = bullet.color;
        context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
      });
    }

    function drawEnemyBullets() {
      enemyBullets.forEach(bullet => {
        context.fillStyle = bullet.color;
        context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
      });
    }

    function drawScore() {
      context.fillStyle = 'white';
      context.font = '20px Arial';
      context.fillText(`Score: ${score}`, 10, 20);
    }

    function drawBackground() {
      context.fillStyle = 'black';
      context.fillRect(0, 0, canvas.width, canvas.height);

      // 星を描画
      stars.forEach(star => {
        context.beginPath();
        context.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        context.fillStyle = 'white';
        context.fill();
      });
    }

    function updateBackground() {
      stars.forEach(star => {
        star.y += star.speed;
        if (star.y > canvas.height) {
          star.y = 0;
          star.x = Math.random() * canvas.width;
        }
      });
    }

    function clear() {
      context.clearRect(0, 0, canvas.width, canvas.height);
    }

    // ゲームオーバー判定
    function checkGameOver() {
      for (let alien of aliens) {
        // エイリアンが画面下に到達した場合、またはプレイヤーとエイリアンが衝突した場合
        if (alien.y + alien.height >= canvas.height || checkCollision(alien, player)) {
          return true;
        }
      }
      return false;
    }

    function drawGameOver() {
      context.fillStyle = 'red';
      context.font = '50px Arial';
      context.textAlign = 'center'; // テキストを中央揃えに設定
      context.shadowColor = 'white'; // 影の色を設定
      context.shadowOffsetX = 4; // 影のX方向のオフセット
      context.shadowOffsetY = 4; // 影のY方向のオフセット
      context.shadowBlur = 2; // 影のぼかし効果
      context.fillText('Game Over', canvas.width / 2, canvas.height / 2);
      context.shadowColor = 'transparent'; // 影をリセット
    }

    function drawYouWin() {
      context.fillStyle = 'green';
      context.font = '50px Arial';
      context.textAlign = 'center'; // テキストを中央揃えに設定
      context.shadowColor = 'white'; // 影の色を設定
      context.shadowOffsetX = 4; // 影のX方向のオフセット
      context.shadowOffsetY = 4; // 影のY方向のオフセット
      context.shadowBlur = 2; // 影のぼかし効果
      context.fillText('You Win!!', canvas.width / 2, canvas.height / 2);
      context.shadowColor = 'transparent'; // 影をリセット
    }

    async function submitScore() {
      try {
        await axios.post('http://localhost:8000/submit_score/', { score });
        console.log('Score submitted successfully' + score);
      } catch (error) {
        console.error('Error submitting score:', error);
      }
    }

    const update = () => {
      if (this.isPaused || this.gameOver) return; // ゲームが一時停止中またはゲームオーバーの場合は更新しない

      const now = Date.now();
      clear();
      drawBackground(); // 背景を描画
      updateBackground(); // 背景を更新
      drawPlayer();
      drawAliens();
      drawBullets();
      drawEnemyBullets(); // 敵の弾を描画
      drawScore(); // スコアを描画
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
              score += 10; // スコアを10増加
              hitSound.play(); // 敵を倒した時の効果音を再生
            }
          });
        }
      });

      // 敵の弾丸を更新
      enemyBullets.forEach((bullet, bulletIndex) => {
        bullet.y += bullet.dy;
        if (bullet.y > canvas.height) {
          enemyBullets.splice(bulletIndex, 1); // 画面外に出た弾丸を削除
        } else if (checkCollision(bullet, player)) {
          drawGameOver();
          submitScore(); // ゲームオーバー時にスコアを送信
          this.gameOver = true; // ゲームオーバー状態を設定
          return;
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

      // 各列の最前面の敵のみが弾を撃つ
      if (Math.random() < 0.1) { // 10%の確率で弾を撃つ
        const frontAliens = [];
        for (let col = 0; col < cols; col++) {
          const columnAliens = aliens.filter(alien => alien.x === col * (alienWidth + alienPadding) + alienOffsetLeft);
          if (columnAliens.length > 0) {
            const frontAlien = columnAliens.reduce((prev, curr) => (prev.y > curr.y ? prev : curr));
            frontAliens.push(frontAlien);
          }
        }
        const randomAlien = frontAliens[Math.floor(Math.random() * frontAliens.length)];
        if (randomAlien) {
          shootEnemyBullet(randomAlien);
        }
      }

      if (checkGameOver()) {
        drawGameOver();
        submitScore(); // ゲームオーバー時にスコアを送信
        this.gameOver = true; // ゲームオーバー状態を設定
        return;
      }

      if (aliens.length === 0) {
        drawYouWin();
        submitScore(); // 勝利時にスコアを送信
        return;
      }

      requestAnimationFrame(update);
    };

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
      if (shootSound.paused) {
        shootSound.play(); // 弾を撃つ効果音を再生
      } else {
        shootSound.currentTime = 0; // 効果音をリセットして再生
      }
    }

    function shootEnemyBullet(alien) {
      const bullet = {
        x: alien.x + alien.width / 2 - 2.5,
        y: alien.y + alien.height,
        width: 5,
        height: 10,
        color: 'yellow',
        dy: 5
      };
      enemyBullets.push(bullet);
    }
    
    // 二つの矩形が重なっているかどうかを判定する関数
    const checkCollision = (rect1, rect2) => {
      return (
        rect1.x < rect2.x + rect2.width &&
        rect1.x + rect1.width > rect2.x &&
        rect1.y < rect2.y + rect2.height &&
        rect1.y + rect1.height > rect2.y
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
      } else if (e.key === 'Escape') {
        this.pauseGame();
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

    backgroundMusic.play(); // ゲーム開始時に音楽を再生
    update();
  },
  methods: {
    pauseGame() {
      this.isPaused = true;
    },
    resumeGame() {
      this.isPaused = false;
      this.gameOver = false; // ゲームオーバー状態をリセット
      this.update(); //todo エラー解消する必要あり this.update is not a function TypeError: this.update is not a function

    }
  }
};
</script>

<style>
canvas {
  background: black;
  display: block;
  margin: 0 auto;
}

.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>