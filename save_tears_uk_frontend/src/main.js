import { createApp } from 'vue'
import App from './views/App.vue'
import './assets/styles.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import router from './router'

createApp(App).use(router).mount('#app')
