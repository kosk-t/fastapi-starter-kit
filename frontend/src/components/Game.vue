<template>
  <canvas id="gameCanvas" width="800" height="600"></canvas>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GameComponent',
  mounted() {
    const canvas = document.getElementById('gameCanvas');
    const context = canvas.getContext('2d');

    // プレイヤーオブジェクトの定義
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

    const bullets = [];

    /**
     * `aliens` 配列をエイリアンオブジェクトで埋め、グリッド状に配置します。
     * 各エイリアンの位置は、グリッド内の行と列に基づいて計算されます。
     *
     * @param {number} rows - グリッドの行数。
     * @param {number} cols - グリッドの列数。
     * @param {number} alienWidth - 各エイリアンの幅。
     * @param {number} alienHeight - 各エイリアンの高さ。
     * @param {number} alienPadding - 各エイリアン間のパディング。
     * @param {number} alienOffsetLeft - グリッド全体の左オフセット。
     * @param {number} alienOffsetTop - グリッド全体の上オフセット。
     * @param {Array} aliens - エイリアンオブジェクトで埋める配列。
     */
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const alienX = col * (alienWidth + alienPadding) + alienOffsetLeft;
        const alienY = row * (alienHeight + alienPadding) + alienOffsetTop;
        aliens.push({ x: alienX, y: alienY, width: alienWidth, height: alienHeight, color: 'green' });
      }
    }

    // プレイヤーを描画する関数
    function drawPlayer() {
      context.fillStyle = player.color;
      context.fillRect(player.x, player.y, player.width, player.height);
    }

    // エイリアンを描画する関数
    function drawAliens() {
      aliens.forEach(alien => {
        context.fillStyle = alien.color; 
        context.fillRect(alien.x, alien.y, alien.width, alien.height);
      });
    }

    // 弾を描画する関数
    function drawBullets() {
      bullets.forEach((bullet, index) => {
        context.fillStyle = bullet.color;
        context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
        bullet.y -= bullet.speed;

        // 画面外に出た弾を削除
        if (bullet.y + bullet.height < 0) {
          bullets.splice(index, 1);
        }
      });
    }

    // 弾を発射する関数
    function shootBullet() {
      const bullet = {
        x: player.x + player.width / 2 - 2.5,
        y: player.y,
        width: 5,
        height: 10,
        color: 'red',
        speed: 7
      };
      bullets.push(bullet);
    }

    // 画面をクリアする関数
    function clear() {
      context.clearRect(0, 0, canvas.width, canvas.height);
    }

    // ゲームの状態を更新する関数
    function update() {
      clear();
      drawPlayer();
      drawAliens();
      drawBullets();
      player.x += player.dx;

      // プレイヤーが画面外に出ないようにする
      if (player.x < 0) {
        player.x = 0;
      }
      if (player.x + player.width > canvas.width) {
        player.x = canvas.width - player.width;
      }

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

      requestAnimationFrame(update);
    }

    // プレイヤーを右に動かす関数
    function moveRight() {
      player.dx = player.speed;
    }

    // プレイヤーを左に動かす関数
    function moveLeft() {
      player.dx = -player.speed;
    }

    const keys = {};

    // キーが押されたときの処理
    const keyDown = (e) => {
      keys[e.key] = true;
      if (keys['ArrowRight'] || keys['Right']) {
        moveRight();
      } else if (keys['ArrowLeft'] || keys['Left']) {
        moveLeft();
      }
      if (keys[' ']) {
        shoot();
      }
    };

    // キーが離されたときの処理
    const keyUp = (e) => {
      keys[e.key] = false;
      if (!keys['ArrowRight'] && !keys['Right'] && !keys['ArrowLeft'] && !keys['Left']) {
        player.dx = 0;
      }
    };

    // スペースキーを押し続けている間に弾を撃ち続ける
    let shootingInterval;
    const shoot = () => {
      if (!shootingInterval) {
        this.saveFirstShotTime(); // 初めて弾を撃った時刻を保存
        shootingInterval = setInterval(() => {
          shootBullet();
        }, 200); // 200ミリ秒ごとに弾を発射
      }
    };

    // 弾の発射を停止する関数
    const stopShooting = () => {
      clearInterval(shootingInterval);
      shootingInterval = null;
    };

    // キーボードのイベントリスナーを追加
    document.addEventListener('keydown', (e) => {
      keyDown(e);
      if (e.key === ' ') {
        shoot();
      }
    });

    document.addEventListener('keyup', (e) => {
      keyUp(e);
      if (e.key === ' ') {
        stopShooting();
      }
    });

    // ゲームの更新を開始
    update();
  },
  methods: {
    async saveFirstShotTime() {
      try {
        await axios.post('http://localhost:8000/shots/');
      } catch (error) {
        console.error('Error saving first shot time:', error);
      }
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
</style>