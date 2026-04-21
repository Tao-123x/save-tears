<template>
  <div class="page-wrapper">
    <header>
      <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
          <router-link to="/">
            <img
              alt="Save Tears logo"
              class="logo"
              src="../static/images/logo.png"
            />
          </router-link>

          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#mainNavbar"
            aria-controls="mainNavbar"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="mainNavbar">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <router-link to="/" class="nav-link text-white" v-if="!isLoggedIn">Home</router-link>
              </li>

              <li class="nav-item" v-if="!isLoggedIn">
                <router-link to="/login" class="nav-link text-white">Login</router-link>
              </li>

              <li class="nav-item" v-if="!isLoggedIn">
                <router-link to="/register" class="nav-link text-white">Register</router-link>
              </li>

              <li class="nav-item" v-if="isLoggedIn">
                <router-link to="/dashboard" class="nav-link text-white">Dashboard</router-link>
              </li>

              <li class="nav-item" v-if="isLoggedIn">
                <router-link to="/account" class="nav-link text-white">Account</router-link>
              </li>

              <li class="nav-item d-lg-none" v-if="isLoggedIn">
                <router-link to="/overview" class="nav-link text-white">Overview</router-link>
              </li>
              <li class="nav-item d-lg-none" v-if="isLoggedIn">
                <router-link to="/water-usage" class="nav-link text-white">Water Usage</router-link>
              </li>
              <li class="nav-item d-lg-none" v-if="isLoggedIn">
                <router-link to="/cost-estimator" class="nav-link text-white">Cost Estimator</router-link>
              </li>
              <li class="nav-item d-lg-none" v-if="isLoggedIn">
                <router-link to="/tips" class="nav-link text-white">Tips</router-link>
              </li>
              <li class="nav-item d-lg-none" v-if="isLoggedIn">
                <router-link to="/logout" class="nav-link text-white">Logout</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <main class="page-content">
      <router-view />
    </main>

    <footer>
      <p>&copy; 2026 Save Tears UK</p>
    </footer>
  </div>
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
