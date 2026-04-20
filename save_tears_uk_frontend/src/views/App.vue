<template>
  <header>
    <nav>
      <img alt="Save Tears logo" class="logo" src="../static/images/logo.png"/>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link v-if="!isLoggedIn" to="/login">Login</router-link></li>
        <li><router-link v-if="!isLoggedIn" to="/register">Register</router-link></li>
        <li><router-link v-if="isLoggedIn"to="/dashboard">Dashboard</router-link></li>
        <li v-if="isLoggedIn">
            <button @click="logout">Logout</button>
        </li>
      </ul>
    </nav>
  </header>
  <router-view />
  <footer>
    <p>&copy; 2026 Save Tears UK</p>
  </footer>
</template>

<script>
export default {
  name: 'App',

  data() {
    return {
      isLoggedIn: !!localStorage.getItem('token')
    }
  },
  watch: {
    // Watch for changes in localStorage to update isLoggedIn status
    '$route'(to, from) {
      this.isLoggedIn = !!localStorage.getItem('token');
    }
  }

}
</script>
