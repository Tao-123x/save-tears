<template>
  <div class="sidebar">
    <ul>
      <li>Overview</li>
      <li>Water Usage</li>
      <li>Cost Estimator</li>
      <li>Tips</li>
      <li><button class="btn bg-dark text-white">Logout</button></li>
    </ul>
  </div>
</template>

<style>
.sidebar {
  width: 200px;
  height: 100vh;
  background-color: #BBCFDA;
  padding: 20px;
}

.sidebar h2 {
  margin-bottom: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 15px;
  cursor: pointer;
}

.sidebar li:hover {
  color: #4E8FCC;
}
</style>