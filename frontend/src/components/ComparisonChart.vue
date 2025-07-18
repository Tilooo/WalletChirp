<script setup>
import { Bar, Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, LineElement, PointElement } from 'chart.js';
import { computed } from 'vue';

// The components to use with Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, LineElement, PointElement);

const props = defineProps({
  chartType: {
    type: String,
    default: 'bar',
  },
  // Prop specifically for line charts
  chartData: {
    type: Object,
    default: () => ({}),
  },
  // Props specifically for bar charts
  chartTitle: {
    type: String,
    required: false,
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
const chartData = computed(() => {
  if (props.chartType === 'line') {
    return props.chartData;
  }

  return {
    labels: [props.chartTitle],
    datasets: [
      {
        label: props.label1,
        backgroundColor: '#84cc16',
        data: [props.data1],
        borderRadius: 4,
      },
      {
        label: props.label2,
        backgroundColor: '#22c55e',
        data: [props.data2],
        borderRadius: 4,
      }
    ]
  };
});

// Chart.js configuration options
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
  <div class="h-64">
    <Bar v-if="props.chartType === 'bar'" :data="chartData" :options="chartOptions" />
    <Line v-if="props.chartType === 'line'" :data="chartData" :options="chartOptions" />
  </div>
</template>