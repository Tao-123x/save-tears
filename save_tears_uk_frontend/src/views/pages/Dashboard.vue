<template>
  <div class="dashboard">
    <DashboardSideBar />

    <div class="container main-content">
      <div class="main">
        <h3>Dashboard</h3>
        <p>Welcome {{ username }} !!</p>
      </div>

      <div class="row">
        <div class="col-md-6">
          <div class="dashboard-card">
            <h5>Water Usage Chart</h5>
          </div>
        </div>
        <div class="col-md-6">
          <div class="dashboard-card">
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-4">
          <div class="dashboard-card">
          </div>
        </div>
        <div class="col-md-4">
          <div class="dashboard-card">
          </div>
        </div>
        <div class="col-md-4">
          <div class="dashboard-card">
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import DashboardSideBar from "../components/DashboardSideBar.vue";

export default {
  components: {
    DashboardSideBar
  },
  data() {
    return {
      username: ""
    };
  },
  mounted() {
    this.username = localStorage.getItem("username") || "";
  }
}
</script>

<style>
.dashboard {
  display: flex;
}

.main {
  flex: 1;
  padding: 20px;
}
</style>

<script>

</script>