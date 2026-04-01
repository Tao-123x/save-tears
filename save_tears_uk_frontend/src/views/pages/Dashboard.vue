<template>
  <div class="dashboard">
    <DashboardSideBar />

    <div class="main">
      <h2>Dashboard</h2>

      
    </div>
  </div>
</template>

<script>
import DashboardSideBar from "../components/DashboardSideBar.vue";

export default {
  components: {
    DashboardSideBar
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