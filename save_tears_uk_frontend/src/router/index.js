import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/pages/Home.vue'
import Login from '../views/pages/Login.vue'
import Register from '../views/pages/Register.vue'
import Dashboard from '../views/pages/Dashboard.vue'

// checks if user is authenticated and logged in, if not redirects to login page
const ifAuthenticated = (to, from, next) => {
    const loggedIn = localStorage.getItem("token");
    if (loggedIn) {
        next();
        return;
    }
    next("/login");
}

const ifNotAuthenticated = (to, from, next) => {
  const token = localStorage.getItem("token");

  if (token) {
    next("/dashboard");
  } else {
    next();
  }
};

const routes = [
  { path: '/', component: Home},
  { path: '/login', component: Login, beforeEnter: ifNotAuthenticated },
  { path: '/register', component: Register, beforeEnter: ifNotAuthenticated },
  { path: '/dashboard', component: Dashboard, beforeEnter: ifAuthenticated }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router