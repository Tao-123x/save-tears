<template>
  <div>
    <div class="box">
      <h1>Register for an account</h1>
      <form @submit.prevent="handleRegister">
        <div class="input-row">
          <div class="input-group">
            <label>Username:</label>
            <input v-model="username" placeholder="Username" />
          </div>

          <div class="input-group">
            <label>Password:</label>
            <input v-model="password" type="password" placeholder="Password" />
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label>Household ID:</label>
            <input v-model="household" placeholder="Household ID" />
          </div>
        </div>

        <div v-if="errorMessage">{{ errorMessage }}</div>
        <div v-if="successMessage">{{ successMessage }}</div>

        <button type="submit">Create Account</button>
      </form>
    </div>
  </div>
</template>

<script>
import { registerUser } from "../../services/user.service";

export default {
  data() {
    return {
      username: "",
      password: "",
      household: "",
      submitted: false,
      errorMessage: "",
      successMessage: ""
    };
  },
  methods: {
    handleRegister() {
      this.submitted = true;
      this.errorMessage = "";
      this.successMessage = "";

      const { username, password, household } = this;

      if (!(username && password && household)) {
        this.errorMessage = "Please fill in all fields";
        this.submitted = false;
        return;
      }

      registerUser(username, password, household)
        .then((response) => {
          this.successMessage = "Registration successful";

          this.username = "";
          this.password = "";
          this.household = "";
          this.submitted = false;
        })
        .catch((error) => {
          this.errorMessage = error.message || error;
          this.submitted = false;
        });
    }
  }
};
</script>