<template>
  <div>
    <GameCanvas ref="gameCanvas" @pauseGame="pauseGame" :musicOn="musicOn" :soundEffectsOn="soundEffectsOn"/>
    <GameModal v-if="isPaused" @resumeGame="resumeGame" @toggleMusic="toggleMusic" @toggleSoundEffects="toggleSoundEffects"/>
  </div>
</template>

<script>
import GameCanvas from './GameCanvas.vue';
import GameModal from './GameModal.vue';

export default {
  name: 'GameComponent',
  components: {
    GameCanvas,
    GameModal
  },
  data() {
    return {
      isPaused: false,
      gameOver: false,
      musicOn: true,
      soundEffectsOn: true
    };
  },
  methods: {
    pauseGame() {
      this.isPaused = true;
    },
    resumeGame() {
      this.isPaused = false;
      this.$refs.gameCanvas.resumeGame();
    },
    toggleMusic(musicOn) {
      this.musicOn = musicOn;
      this.$refs.gameCanvas.toggleMusic(musicOn);
    },
    toggleSoundEffects(soundEffectsOn) {
      this.soundEffectsOn = soundEffectsOn;
      this.$refs.gameCanvas.toggleSoundEffects(soundEffectsOn);
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