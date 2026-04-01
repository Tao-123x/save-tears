<template>
  <header>
    <nav>
      <img alt="Save Tears logo" class="logo" src="../static/images/logo.png"/>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
        <li><router-link to="/register">Register</router-link></li>
        <li><router-link to="/dashboard">Dashboard</router-link></li>
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
  name: 'App'
}

</script>
