<template>
  <div class="dashboard">
    <DashboardSideBar />

    <main class="container main-content">
      <div class="main">
        <h2>Dashboard</h2>
        <p>Welcome {{ username }} !!</p>
      </div>

      <div class="row">
        <div class="col-12 col-xl-6 mb-4">
          <div class="dashboard-card">
            <h5>Water Usage Chart</h5>
            <canvas id="waterChart"></canvas>
          </div>
        </div>
        <div class="col-12 col-xl-6 mb-4">
          <div class="dashboard-card">
            <h5 class="card-title"> Daily Usage Overview</h5>
            <p>Toddays Usage</p>
            <P><strong>150l</strong></P>
            <p>Average Daily Usage</p>
            <P><strong>150l</strong></P>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12 col-md-6 col-xl-4 mb-4">
          <div class="dashboard-card">
            <h5 class="card-title">Cost Estimator</h5>
            <p>Use our cost estimator to see how much you could save by reducing your water usage. Enter your current usage and see the potential savings!</p>
          </div>
        </div>
        <div class="col-12 col-md-6 col-xl-4 mb-4">
          <div class="dashboard-card">
            <h5 class="card-title">Tips to Save Water</h5>
            <ul>
              <li>Take shorter showers</li>
              <li>Turn off the tap while brushing your teeth</li>
              <li>Fix leaking taps quickly</li>
              <li>Use washing machines only with full loads</li>
            </ul>
          </div>
        </div>
        <div class="col-12 col-md-6 col-xl-4 mb-4">
          <div class="dashboard-card">
            <h5 class="card-title">Recent Activity</h5>
            <p><strong>Shower</strong>  8 mins, 80 L, £1.20</p>
            <p><strong>Washing dishes</strong> 20 L,  £0.30</p>
            <p><strong>Laundry</strong>  50 L,  £0.75</p>
            <p><strong>Hand wash</strong> 10 L, £0.15</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import DashboardSideBar from "../components/DashboardSideBar.vue";
import { Chart } from "chart.js/auto";

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

    const ctx = document.getElementById("waterChart");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
          {
            label: "Water Usage (Litres)",
            data: [120, 150, 100, 180, 140, 200, 130],
            backgroundColor: "#BBCFDA",
          },
        ],
      },
      options: {
        responsive: true,
      },
    });
  }
}
</script>

