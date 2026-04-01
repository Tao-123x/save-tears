<template>
  <div>
    <div class="box">
      <h1>Register for an account</h1>
      <form>
        <div class="input-row">
          <div class="input-group">
            <label>First Name:</label>
            <input type="text" name="first_name" />
            <div>First name is required</div>
          </div>
          <div class="input-group">
            <label>Last Name:</label>
            <input type="text" name="last_name" />
            <div>Last name is required</div>
          </div>
        </div>
        <div class="input-row">
          <div class="input-group">
            <label>Email:</label>
            <input type="email" name="email" />
            <div>Email is required</div>
          </div>
          <div class="input-group">
            <label>Password:</label>
            <input type="password" name="password" />
            <div>Password is required</div>
          </div>
        </div>
        <button type="submit">Create Account</button>
      </form>
    </div>
  </div>
</template>

<script>

</script>