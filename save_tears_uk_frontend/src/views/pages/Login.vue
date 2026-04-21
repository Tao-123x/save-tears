<template>
  <div class="auth-page">
    <div class="box auth-box">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="input-row">
          <div class="input-group">
            <label>Username:</label>
            <input v-model="username" type="text" placeholder="Username" />
          </div>

          <div class="input-group">
            <label>Password:</label>
            <input v-model="password" type="password" placeholder="Password" />
          </div>
        </div>

        <div v-if="errorMessage">{{ errorMessage }}</div>

        <button type="submit">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
import { loginUser } from "../../services/user.service";

export default {
  data() {
    return {
      username: "",
      password: "",
      submitted: false,
      errorMessage: ""
    };
  },
  methods: {
    handleLogin() {
      this.submitted = true;
      this.errorMessage = "";

      const { username, password } = this;

      if (!(username && password)) {
        this.errorMessage = "Please enter username and password";
        this.submitted = false;
        return;
      }

      loginUser(username, password)
        .then(() => {
          this.$router.push("/dashboard");
        })
        .catch((error) => {
          this.errorMessage = "Invalid username or password";
          this.submitted = false;
        });
    }
  }
};
</script>