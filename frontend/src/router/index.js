import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/HelloWorld.vue';
import GameComponent from '../components/Game.vue'; // ここを変更

const routes = [
  { path: '/', component: Home },
  { path: '/game', component: GameComponent } // ここを変更
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;