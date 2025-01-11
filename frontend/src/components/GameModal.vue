<template>
  <div class="modal" ref="modal" tabindex="0" @keydown.esc="resumeGame">
    <div class="modal-content">
      <span class="close" @click="resumeGame">&times;</span>
      <h2>設定</h2>
      <div class="settings">
        <div class="setting-item">
          <label>
            <input type="checkbox" v-model="musicOn" @change="toggleMusic">
            音楽
          </label>
        </div>
        <div class="setting-item">
          <label>
            <input type="checkbox" v-model="soundEffectsOn" @change="toggleSoundEffects">
            効果音
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameModal',
  data() {
    return {
      musicOn: JSON.parse(localStorage.getItem('musicOn')) || true,
      soundEffectsOn: true
    };
  },
  methods: {
    toggleMusic() {
      this.$emit('toggleMusic', this.musicOn);
      localStorage.setItem('musicOn', JSON.stringify(this.musicOn)); // 音楽のオンオフ状態を保存
    },
    toggleSoundEffects() {
      this.$emit('toggleSoundEffects', this.soundEffectsOn);
    },
    resumeGame() {
      this.$emit('resumeGame');
      this.$refs.modal.blur();
    }
  },
  mounted() {
    this.musicOn = JSON.parse(localStorage.getItem('musicOn'))
    this.$refs.modal.focus();
  }
};
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fefefe;
  padding: 20px;
  border: 1px solid #888;
  width: 300px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.settings {
  margin-top: 20px;
}

.setting-item {
  margin-bottom: 15px;
}

.setting-item label {
  font-size: 18px;
}
</style>