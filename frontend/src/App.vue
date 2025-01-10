<template>
  <div id="app">
    <h1>Item List</h1>
    <ul>
      <li v-for="item in items" :key="item.id">{{ item.name }}</li>
    </ul>
    <h2>Create Item</h2>
    <input v-model="newItem.name" placeholder="Item name" />
    <button @click="createItem">Create</button>
  </div>
</template>

<script>
import api from './api';

export default {
  data() {
    return {
      items: [],
      newItem: {
        name: ''
      }
    };
  },
  methods: {
    async fetchItems() {
      const response = await api.getItems();
      this.items = response.data;
    },
    async createItem() {
      await api.createItem(this.newItem);
      this.newItem.name = '';
      this.fetchItems();
    }
  },
  created() {
    this.fetchItems();
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}
</style>