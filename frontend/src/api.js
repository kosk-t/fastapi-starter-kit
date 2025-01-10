import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  getItems() {
    return apiClient.get('/items/');
  },
  getItem(itemId) {
    return apiClient.get(`/items/${itemId}`);
  },
  createItem(item) {
    return apiClient.post('/items/', item);
  }
};