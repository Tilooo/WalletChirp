<script setup>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { computed } from 'vue';

// The components to use with Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  chartTitle: {
    type: String,
    required: true,
  },
  label1: {
    type: String,
    default: 'Country 1',
  },
  data1: {
    type: Number,
    default: 0,
  },
  label2: {
    type: String,
    default: 'Country 2',
  },
  data2: {
    type: Number,
    default: 0,
  }
});

// here formating the data for Chart.js.
const chartData = computed(() => ({
  labels: [props.chartTitle], // The label for the data group (pvz., "GDP per Capita")
  datasets: [
    {
      label: props.label1, // The label for the first bar (pvz., "United States")
      backgroundColor: '#84cc16', // A lime green color
      data: [props.data1], // The numeric data for the first bar
      borderRadius: 4,
    },
    {
      label: props.label2, // The label for the second bar (pvz., "Germany")
      backgroundColor: '#22c55e', // A darker green color
      data: [props.data2], // The numeric data for the second bar
      borderRadius: 4,
    }
  ]
}));

// Chart.js configuration options.
// a customize look and feel of the chart.
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: '#cbd5e1' // Color for the legend text (pvz., "United States", "Germany")
      }
    },
    title: {
      display: false // a title outside the chart
    }
  },
  scales: {
    y: {
      ticks: {
        color: '#94a3b8' // color for the Y-axis labels
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.1)' // color for the grid lines
      }
    },
    x: {
      ticks: {
        color: '#94a3b8' // color for the X-axis labels
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.1)' // color for the grid lines
      }
    }
  }
};
</script>

<template>
  <!-- The chart render -->
  <div class="h-64">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>