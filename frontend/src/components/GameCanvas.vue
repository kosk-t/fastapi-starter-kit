<template>
  <canvas id="gameCanvas" width="800" height="600"></canvas>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GameCanvas',
  data() {
    return {
      isPaused: false,
      gameOver: false, // ゲームオーバー状態を管理する変数
      score: 0, // スコアを管理する変数
      player: {
        width: 50,
        height: 20,
        x: 0,
        y: 0,
        color: 'blue',
        speed: 5,
        dx: 0
      },
      aliens: [],
      bullets: [],
      enemyBullets: [],
      stars: [],
      keys: {},
      alienDirection: 1, // エイリアンの移動方向（1: 右, -1: 左）
      alienMoveCounter: 0, // エイリアンの移動カウンター
      lastShootTime: 0,
      canvas: null,
      context: null,
      now: null,
      shootSound: null,
      hitSound: null,
      alienHeight:20, 
      alienPadding: 10,
      soundEffectsOn: true,
      backgroundMusic: null,
      musicOn: JSON.parse(localStorage.getItem('musicOn')) || true, // 音楽のオンオフ状態を復元
    };
  },
  mounted() {
    this.initializeGame();
  },
  methods: {
    initializeGame() {
      this.musicOn = JSON.parse(localStorage.getItem('musicOn'))
      this.canvas = document.getElementById('gameCanvas');
      this.context = this.canvas.getContext('2d');
      this.backgroundMusic = new Audio(require('@/assets/スペースインベーダー_BOSS_Inst.mp3')); // 音楽ファイルのパスを指定
      this.backgroundMusic.loop = true; // ループ再生

      this.shootSound = new Audio(require('@/assets/shoot.mp3')); // 弾を撃つ効果音のパスを指定
      this.hitSound = new Audio(require('@/assets/hit.mp3')); // 敵を倒した時の効果音のパスを指定

      this.player.x = this.canvas.width / 2 - this.player.width / 2;
      this.player.y = this.canvas.height - this.player.height - 10;

      const rows = 3;
      const cols = 5;
      const alienWidth = 40;
      const alienOffsetTop = 30;
      const alienOffsetLeft = 30;

      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          const alienX = col * (alienWidth + this.alienPadding) + alienOffsetLeft;
          const alienY = row * (this.alienHeight + this.alienPadding) + alienOffsetTop;
          this.aliens.push({ x: alienX, y: alienY, width: alienWidth, height: this.alienHeight, color: 'green' });
        }
      }

      const numStars = 100;
      for (let i = 0; i < numStars; i++) {
        this.stars.push({
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          radius: Math.random() * 2,
          speed: Math.random() * 0.5 + 0.5
        });
      }

      document.addEventListener('keydown', this.keyDown);
      document.addEventListener('keyup', this.keyUp);

      if (this.musicOn) {
        this.backgroundMusic.play(); // ゲーム開始時に音楽を再生
      }
      this.update();
    },
    keyDown(e) {
      this.keys[e.key] = true;
      if (this.keys['ArrowRight'] || this.keys['Right']) {
        this.moveRight();
      } else if (this.keys['ArrowLeft'] || this.keys['Left']) {
        this.moveLeft();
      } else if (e.key === 'Escape') {
        // エスケープキー押したらゲームを一時停止してモーダルを表示
        this.pauseGame();
      }
    },
    keyUp(e) {
      this.keys[e.key] = false;
      if (!this.keys['ArrowRight'] && !this.keys['Right'] && !this.keys['ArrowLeft'] && !this.keys['Left']) {
        this.player.dx = 0;
      } else if (this.keys['ArrowRight'] || this.keys['Right']) {
        this.moveRight();
      } else if (this.keys['ArrowLeft'] || this.keys['Left']) {
        this.moveLeft();
      }
    },
    pauseGame() {
      this.isPaused = true;
      this.$emit('pauseGame');
    },
    resumeGame() {
      this.isPaused = false;
      this.gameOver = false; // ゲームオーバー状態をリセット
      this.update(); // ゲームループを再開
    },
    async submitScore() {
      try {
        await axios.post('http://localhost:8000/submit_score/', { score: this.score });
        console.log('Score submitted successfully' + this.score);
      } catch (error) {
        console.error('Error submitting score:', error);
      }
    },
    update() {
      if (this.isPaused || this.gameOver) return; // ゲームが一時停止中またはゲームオーバーの場合は更新しない

      this.now = Date.now();
      this.clear();
      this.drawBackground(); // 背景を描画
      this.updateBackground(); // 背景を更新
      this.drawPlayer();
      this.drawAliens();
      this.drawBullets();
      this.drawEnemyBullets(); // 敵の弾を描画
      this.drawScore(); // スコアを描画
      this.player.x += this.player.dx;

      if (this.player.x < 0) {
        this.player.x = 0;
      }
      if (this.player.x + this.player.width > this.canvas.width) {
        this.player.x = this.canvas.width - this.player.width;
      }

      // 弾丸を更新
      this.bullets.forEach((bullet, bulletIndex) => {
        bullet.y -= bullet.dy;
        if (bullet.y < 0) {
          this.bullets.splice(bulletIndex, 1); // 画面外に出た弾丸を削除
        } else {
          // エイリアンとの衝突判定
          this.aliens.forEach((alien, alienIndex) => {
            if (this.checkCollision(bullet, alien)) {
              this.bullets.splice(bulletIndex, 1); // 弾丸を削除
              this.aliens.splice(alienIndex, 1); // エイリアンを削除
              this.score += 10; // スコアを加算
              if(this.soundEffectsOn){
                this.hitSound.play(); // 効果音を再生
              }
            }
          });
        }
      });

      // 敵の弾丸を更新
      this.enemyBullets.forEach((bullet, bulletIndex) => {
        bullet.y += bullet.dy; // 弾丸を下方向に移動させる
        if (bullet.y > this.canvas.height) {
          this.enemyBullets.splice(bulletIndex, 1); // 画面外に出た弾丸を削除
        } else {
          // プレイヤーとの衝突判定
          if (this.checkCollision(bullet, this.player)) {
            this.enemyBullets.splice(bulletIndex, 1); // 弾丸を削除
            this.drawGameOver();
            this.submitScore(); // ゲームオーバー時にスコアを送信
            this.gameOver = true; // ゲームオーバー状態を設定
            return;
          }
        }
      });

      // エイリアンを同じ方向に動かす
      this.alienMoveCounter++;
      if (this.alienMoveCounter % 30 === 0) { // 30フレームごとにエイリアンを動かす
        let changeDirection = false;
        this.aliens.forEach(alien => {
          alien.x += this.alienDirection * 10; // 10ピクセルずつ動かす
          if (alien.x < 0 || alien.x + alien.width > this.canvas.width) {
            changeDirection = true;
          }
        });

        if (changeDirection) {
          this.alienDirection *= -1; // 方向を反転
          this.aliens.forEach(alien => {
            alien.y += this.alienHeight + this.alienPadding; // エイリアンを下に移動
          });
        }
      }

      // 各敵がランダムに弾を撃つ
      if (Math.random() < 0.1) { // 10%の確率で弾を撃つ
        const randomAlien = this.aliens[Math.floor(Math.random() * this.aliens.length)];
        if (randomAlien) {
          this.shootEnemyBullet(randomAlien);
        }
      }

      if (this.keys[' '] && this.now - this.lastShootTime > 500) { // 0.5秒間隔で弾を発射
        this.shoot();
        this.lastShootTime = this.now;
      }

      if (this.checkGameOver()) {
        this.drawGameOver();
        this.submitScore(); // ゲームオーバー時にスコアを送信
        this.gameOver = true; // ゲームオーバー状態を設定
        return;
      }

      if (this.aliens.length === 0) {
        this.drawYouWin();
        this.submitScore(); // 勝利時にスコアを送信
        return;
      }

      requestAnimationFrame(this.update);
    },
    clear() {
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    },
    drawBackground() {
      this.context.fillStyle = 'black';
      this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

      // 星を描画
      this.stars.forEach(star => {
        this.context.beginPath();
        this.context.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        this.context.fillStyle = 'white';
        this.context.fill();
      });
    },
    updateBackground() {
      this.stars.forEach(star => {
        star.y += star.speed;
        if (star.y > this.canvas.height) {
          star.y = 0;
          star.x = Math.random() * this.canvas.width;
        }
      });
    },
    drawPlayer() {
      this.context.fillStyle = this.player.color;
      this.context.fillRect(this.player.x, this.player.y, this.player.width, this.player.height);
    },
    drawAliens() {
      this.aliens.forEach(alien => {
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
              this.context.fillStyle = alien.color; // エイリアンの色
              this.context.fillRect(
                alien.x + col * blockWidth,
                alien.y + row * blockHeight,
                blockWidth,
                blockHeight
              );
            }
          }
        }
      });
    },
    drawBullets() {
      this.bullets.forEach(bullet => {
        this.context.fillStyle = bullet.color;
        this.context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
      });
    },
    drawEnemyBullets() {
      this.enemyBullets.forEach(bullet => {
        this.context.fillStyle = bullet.color;
        this.context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
      });
    },
    drawScore() {
      this.context.fillStyle = 'white';
      this.context.font = '20px Arial';
      this.context.fillText(`Score: ${this.score}`, 10, 20);
    },
    checkGameOver() {
      for (let alien of this.aliens) {
        if (alien.y + alien.height >= this.canvas.height || this.checkCollision(alien, this.player)) {
          return true;
        }
      }
      return false;
    },
    drawGameOver() {
      this.context.fillStyle = 'red';
      this.context.font = '50px Arial';
      this.context.textAlign = 'center';
      this.context.shadowColor = 'white';
      this.context.shadowOffsetX = 4;
      this.context.shadowOffsetY = 4;
      this.context.shadowBlur = 2;
      this.context.fillText('Game Over', this.canvas.width / 2, this.canvas.height / 2);
      this.context.shadowColor = 'transparent';
    },
    drawYouWin() {
      this.context.fillStyle = 'green';
      this.context.font = '50px Arial';
      this.context.textAlign = 'center';
      this.context.shadowColor = 'white';
      this.context.shadowOffsetX = 4;
      this.context.shadowOffsetY = 4;
      this.context.shadowBlur = 2;
      this.context.fillText('You Win!!', this.canvas.width / 2, this.canvas.height / 2);
      this.context.shadowColor = 'transparent';
    },
    checkCollision(rect1, rect2) {
      return (
        rect1.x < rect2.x + rect2.width &&
        rect1.x + rect1.width > rect2.x &&
        rect1.y < rect2.y + rect2.height &&
        rect1.y + rect1.height > rect2.y
      );
    },
    shoot() {
      const bullet = {
        x: this.player.x + this.player.width / 2 - 2.5,
        y: this.player.y,
        width: 5,
        height: 10,
        color: 'red',
        dy: 5
      };
      this.bullets.push(bullet);
      if (this.shootSound.paused && this.soundEffectsOn) {
        this.shootSound.play(); // 弾を撃つ効果音を再生
      } else {
        this.shootSound.currentTime = 0; // 効果音をリセットして再生
      }
    },
    shootEnemyBullet(alien) {
      const bullet = {
        x: alien.x + alien.width / 2 - 2.5,
        y: alien.y + alien.height,
        width: 5,
        height: 10,
        color: 'yellow',
        dy: 5
      };
      this.enemyBullets.push(bullet);
    },
    moveRight() {
      this.player.dx = this.player.speed;
    },
    moveLeft() {
      this.player.dx = -this.player.speed;
    },
    toggleMusic(musicOn) {
      this.musicOn = musicOn;
      if (musicOn) {
        this.backgroundMusic.play();
      } else {
        this.backgroundMusic.pause();
      }
    },
    toggleSoundEffects(soundEffectsOn) {
      this.soundEffectsOn = soundEffectsOn;
    }
  }
};
</script>