<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import ComparisonChart from './ComparisonChart.vue';
import ResultsCardSkeleton from './ResultsCardSkeleton.vue';

// --- STATE MANAGEMENT ---
const allCountries = ref([]); // holds a big list of countries
const historicalChartData = ref(null);
const historicalChartTitle = ref('');
const isHistoricalLoading = ref(false);

// Country 1
const countryCode1 = ref('usa');
const countryName1 = ref('');
const countryData1 = ref(null);
const isLoading1 = ref(false);
const error1 = ref(null);

// Country 2
const countryCode2 = ref('deu');
const countryName2 = ref('');
const countryData2 = ref(null);
const isLoading2 = ref(false);
const error2 = ref(null);

// --- API FUNCTIONS ---
const fetchAllCountries = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/countries/');
    allCountries.value = response.data;
  } catch (error) {
    console.error("Failed to fetch country list:", error);
    // to show an error to the user here
  }
};

const fetchData = async (countryNumber) => {
  const isCountry1 = countryNumber === 1;

  // to find the country code from the selected name
  const selectedName = isCountry1 ? countryName1.value : countryName2.value;
  const country = allCountries.value.find(c => c.name.toLowerCase() === selectedName.toLowerCase());

  // If a name is typed but not found, shows an error.
  if (selectedName && !country) {
      const errorMsg = `Country "${selectedName}" not found.`;
      if (isCountry1) { error1.value = errorMsg; } else { error2.value = errorMsg; }
      return;
  }

  // to use the found code, or the default if nothing is typed.
  const countryCodeToFetch = country ? country.id : (isCountry1 ? countryCode1.value : countryCode2.value);

  if (!countryCodeToFetch) { return; } // Don't fetch if there's no code

  // Reset state
  if (isCountry1) {
    isLoading1.value = true;
    error1.value = null;
  } else {
    isLoading2.value = true;
    error2.value = null;
  }

  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/country/${countryCodeToFetch.toLowerCase()}/`);
    if (isCountry1) {
      countryData1.value = response.data;
    } else {
      countryData2.value = response.data;
    }
  } catch (err) {
    let errorMsg = 'An error occurred.';
    if (err.response && err.response.status === 404) {
      errorMsg = `Could not find data for code: "${countryCodeToFetch}".`;
    }
    if (isCountry1) { error1.value = errorMsg; } else { error2.value = errorMsg; }
  } finally {
    if (isCountry1) { isLoading1.value = false; } else { isLoading2.value = false; }
  }
};

const fetchHistoricalData = async (indicatorName, indicatorCode) => {
  isHistoricalLoading.value = true;
  historicalChartTitle.value = indicatorName;
  historicalChartData.value = null; // Clear old data

  try {
    // data for both countries at the same time
    const [response1, response2] = await Promise.all([
      axios.get(`http://127.0.0.1:8000/api/historical/${countryData1.value.country.id}/${indicatorCode}/`),
      axios.get(`http://127.0.0.1:8000/api/historical/${countryData2.value.country.id}/${indicatorCode}/`)
    ]);

    const data1 = response1.data;
    const data2 = response2.data;

    // Combine all years from both datasets to create the labels
    const allYears = [...new Set([...data1.map(d => d.year), ...data2.map(d => d.year)])].sort();

    const createDataset = (data, allYears) => {
        const dataMap = new Map(data.map(d => [d.year, d.value]));
        return allYears.map(year => dataMap.get(year) || null); // null for missing years to create gaps in the line
    };

    // The data for chart component
    historicalChartData.value = {
        labels: allYears,
        datasets: [
            { label: countryData1.value.country.name, data: createDataset(data1, allYears), borderColor: '#84cc16', tension: 0.1 },
            { label: countryData2.value.country.name, data: createDataset(data2, allYears), borderColor: '#22c55e', tension: 0.1 }
        ]
    };

  } catch (error) {
    console.error("Failed to fetch historical data:", error);
  } finally {
    isHistoricalLoading.value = false;
  }
};

// --- HELPER FUNCTION ---
const formatNumber = (num) => {
  if (num === null || num === undefined) return 'N/A';
  return Number(num).toLocaleString('en-US', { maximumFractionDigits: 2 });
};


// --- LIFECYCLE HOOK ---
onMounted(async () => {
  // When the component first loads...
  await fetchAllCountries(); // Get the list of all countries

  // to set the initial names for default codes
  countryName1.value = allCountries.value.find(c => c.id.toLowerCase() === countryCode1.value)?.name || '';
  countryName2.value = allCountries.value.find(c => c.id.toLowerCase() === countryCode2.value)?.name || '';

  // to fetch the data for the default countries
  fetchData(1);
  fetchData(2);
});

</script>

<template>
  <div
    class="text-slate-200 min-h-screen p-4 sm:p-8 flex flex-col items-center bg-cover bg-center bg-fixed"
    style="background-image: url('/background.jpg')"
  >
    <!-- Dark overlay for readability -->
    <div class="absolute inset-0 bg-slate-900/70 z-0"></div>

    <div class="relative z-10 w-full flex flex-col items-center">
      <header class="text-center mb-10">
        <h1 class="text-4xl sm:text-5xl font-extrabold">
          <span class="text-white">Wallet</span><span class="bg-gradient-to-r from-lime-400 to-green-500 bg-clip-text text-transparent">Chirp</span>
        </h1>
        <p class="text-slate-400 mt-2">Compare the economies of the world.</p>
      </header>

      <main class="w-full max-w-7xl grid grid-cols-1 md:grid-cols-2 gap-8">

        <!-- ================== COLUMN 1 ================== -->
        <div class="flex flex-col gap-8">
          <!-- Input Card 1 -->
          <div class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10 transition-all duration-300 ease-in-out hover:scale-105 hover:-translate-y-2 hover:shadow-2xl">
            <label for="country1" class="block text-sm font-medium text-slate-300 mb-2">Country 1</label>
            <div class="flex gap-4">
              <input id="country1" v-model="countryName1" @keyup.enter="fetchData(1)" list="country-list" placeholder="Type a country name..." class="w-full bg-slate-900/50 border border-white/20 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-lime-500" />
              <button @click="fetchData(1)" :disabled="isLoading1" class="relative group overflow-hidden px-6 py-2 rounded-md text-white font-bold transition-all duration-300 disabled:bg-slate-500 disabled:cursor-not-allowed">
                <span class="absolute inset-0 bg-gradient-to-r from-lime-500 to-green-600 group-hover:from-lime-600 group-hover:to-green-700 transition-all duration-300"></span>
                <span class="relative"><span v-if="isLoading1">...</span><span v-else>Analyze</span></span>
              </button>
            </div>
          </div>

          <!-- Results Card 1 Section -->
            <ResultsCardSkeleton v-if="isLoading1" />
            <div v-else class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10 transition-all duration-300 ease-in-out hover:scale-105 hover:-translate-y-2 hover:shadow-2xl min-h-[300px] flex items-center justify-center">
              <div v-if="error1" class="text-red-400 text-center"><strong>Oops!</strong><br/>{{ error1 }}</div>
              <div v-else-if="countryData1 && countryData1.country" class="w-full">
                <h2 class="text-2xl font-bold mb-4 border-b border-white/10 pb-2">{{ countryData1.country.name }}</h2>
                <ul class="space-y-3 text-sm">
                  <li v-if="countryData1.gdp_per_capita" class="flex justify-between items-center">
                    <span @click="fetchHistoricalData('GDP per Capita', 'NY.GDP.PCAP.CD')" class="font-semibold cursor-pointer hover:text-lime-300 transition-colors">{{ countryData1.gdp_per_capita.name }} ({{ countryData1.gdp_per_capita.year }})</span>
                    <span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData1.gdp_per_capita.value) }}</span>
                  </li>
                  <li v-if="countryData1.inflation" class="flex justify-between items-center">
                    <span @click="fetchHistoricalData('Inflation (Annual %)', 'FP.CPI.TOTL.ZG')" class="font-semibold cursor-pointer hover:text-lime-300 transition-colors">{{ countryData1.inflation.name }} ({{ countryData1.inflation.year }})</span>
                    <span class="text-red-400 font-mono text-lg">{{ formatNumber(countryData1.inflation.value) }}%</span>
                  </li>
                  <li v-if="countryData1.debt_to_gdp" class="flex justify-between items-center">
                    <span @click="fetchHistoricalData('Debt (% of GDP)', 'GC.DOD.TOTL.GD.ZS')" class="font-semibold cursor-pointer hover:text-lime-300 transition-colors">Debt (% of GDP) ({{ countryData1.debt_to_gdp.year }})</span>
                    <span class="text-red-400 font-mono text-lg">{{ formatNumber(countryData1.debt_to_gdp.value) }}%</span>
                  </li>
                  <li v-if="countryData1.gdp" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.gdp.name }} ({{ countryData1.gdp.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData1.gdp.value) }}</span></li>
                  <li v-if="countryData1.gni_per_capita" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.gni_per_capita.name }} ({{ countryData1.gni_per_capita.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData1.gni_per_capita.value) }}</span></li>
                  <li v-if="countryData1.ppp" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.ppp.name }} ({{ countryData1.ppp.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData1.ppp.value) }}</span></li>
                </ul>
                <div v-if="countryData1.economic_summary" class="mt-4 pt-4 border-t border-white/10"><h3 class="font-semibold text-lime-300 mb-1">Economic Chirp</h3><p class="text-sm text-slate-300 italic">"{{ countryData1.economic_summary }}"</p></div>
                <div v-if="countryData1.tax_summary" class="mt-4 pt-4 border-t border-white/10"><h3 class="font-semibold text-lime-300 mb-1">Tax Chirp</h3><p class="text-sm text-slate-300">{{ countryData1.tax_summary }}</p></div>
              </div>
            </div>
          </div>
        </div>

        <!-- ================== COLUMN 2 ================== -->
        <div class="flex flex-col gap-8">
          <!-- Input Card 2 -->
          <div class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10 transition-all duration-300 ease-in-out hover:scale-105 hover:-translate-y-2 hover:shadow-2xl">
            <label for="country2" class="block text-sm font-medium text-slate-300 mb-2">Country 2</label>
            <div class="flex gap-4">
              <input id="country2" v-model="countryName2" @keyup.enter="fetchData(2)" list="country-list" placeholder="Type a country name..." class="w-full bg-slate-900/50 border border-white/20 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-lime-500" />
              <button @click="fetchData(2)" :disabled="isLoading2" class="relative group overflow-hidden px-6 py-2 rounded-md text-white font-bold transition-all duration-300 disabled:bg-slate-500 disabled:cursor-not-allowed">
                <span class="absolute inset-0 bg-gradient-to-r from-lime-500 to-green-600 group-hover:from-lime-600 group-hover:to-green-700 transition-all duration-300"></span>
                <span class="relative"><span v-if="isLoading2">...</span><span v-else>Analyze</span></span>
              </button>
            </div>
          </div>

          <!-- Results Card 2 Section -->
            <ResultsCardSkeleton v-if="isLoading2" />
            <div v-else class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10 transition-all duration-300 ease-in-out hover:scale-105 hover:-translate-y-2 hover:shadow-2xl min-h-[300px] flex items-center justify-center">
              <div v-if="error2" class="text-red-400 text-center"><strong>Oops!</strong><br/>{{ error2 }}</div>
              <div v-else-if="countryData2 && countryData2.country" class="w-full">
                <h2 class="text-2xl font-bold mb-4 border-b border-white/10 pb-2">{{ countryData2.country.name }}</h2>
                <ul class="space-y-3 text-sm">
                  <li v-if="countryData2.gdp_per_capita" class="flex justify-between items-center">
                    <span @click="fetchHistoricalData('GDP per Capita', 'NY.GDP.PCAP.CD')" class="font-semibold cursor-pointer hover:text-lime-300 transition-colors">{{ countryData2.gdp_per_capita.name }} ({{ countryData2.gdp_per_capita.year }})</span>
                    <span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData2.gdp_per_capita.value) }}</span>
                  </li>
                  <li v-if="countryData2.inflation" class="flex justify-between items-center">
                    <span @click="fetchHistoricalData('Inflation (Annual %)', 'FP.CPI.TOTL.ZG')" class="font-semibold cursor-pointer hover:text-lime-300 transition-colors">{{ countryData2.inflation.name }} ({{ countryData2.inflation.year }})</span>
                    <span class="text-red-400 font-mono text-lg">{{ formatNumber(countryData2.inflation.value) }}%</span>
                  </li>
                  <li v-if="countryData2.debt_to_gdp" class="flex justify-between items-center">
                    <span @click="fetchHistoricalData('Debt (% of GDP)', 'GC.DOD.TOTL.GD.ZS')" class="font-semibold cursor-pointer hover:text-lime-300 transition-colors">Debt (% of GDP) ({{ countryData2.debt_to_gdp.year }})</span>
                    <span class="text-red-400 font-mono text-lg">{{ formatNumber(countryData2.debt_to_gdp.value) }}%</span>
                  </li>
                  <li v-if="countryData2.gdp" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.gdp.name }} ({{ countryData2.gdp.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData2.gdp.value) }}</span></li>
                  <li v-if="countryData2.gni_per_capita" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.gni_per_capita.name }} ({{ countryData2.gni_per_capita.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData2.gni_per_capita.value) }}</span></li>
                  <li v-if="countryData2.ppp" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.ppp.name }} ({{ countryData2.ppp.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData2.ppp.value) }}</span></li>
                </ul>
                <div v-if="countryData2.economic_summary" class="mt-4 pt-4 border-t border-white/10"><h3 class="font-semibold text-lime-300 mb-1">Economic Chirp</h3><p class="text-sm text-slate-300 italic">"{{ countryData2.economic_summary }}"</p></div>
                <div v-if="countryData2.tax_summary" class="mt-4 pt-4 border-t border-white/10"><h3 class="font-semibold text-lime-300 mb-1">Tax Chirp</h3><p class="text-sm text-slate-300">{{ countryData2.tax_summary }}</p></div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- * Visual comparison section (BAR CHARTS) * -->
      <section v-if="countryData1 && countryData2" class="w-full max-w-7xl mt-8">
        <h2 class="text-3xl font-bold text-center mb-6 text-white">Visual Comparison</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-if="countryData1.gdp_per_capita && countryData2.gdp_per_capita" class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10">
            <h3 class="font-semibold text-lg text-center mb-4">GDP per Capita (USD)</h3>
            <ComparisonChart chartTitle="GDP per Capita" :label1="countryData1.country.name" :data1="countryData1.gdp_per_capita.value" :label2="countryData2.country.name" :data2="countryData2.gdp_per_capita.value" />
          </div>
          <div v-if="countryData1.inflation && countryData2.inflation" class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10">
            <h3 class="font-semibold text-lg text-center mb-4">Inflation (Annual %)</h3>
            <ComparisonChart chartTitle="Inflation" :label1="countryData1.country.name" :data1="countryData1.inflation.value" :label2="countryData2.country.name" :data2="countryData2.inflation.value" />
          </div>
          <div v-if="countryData1.debt_to_gdp && countryData2.debt_to_gdp" class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10">
            <h3 class="font-semibold text-lg text-center mb-4">Debt (% of GDP)</h3>
            <ComparisonChart chartTitle="Debt" :label1="countryData1.country.name" :data1="countryData1.debt_to_gdp.value" :label2="countryData2.country.name" :data2="countryData2.debt_to_gdp.value" />
          </div>
        </div>
      </section>

      <!-- * Historical trend section (LINE CHART) * -->
      <section v-if="historicalChartData || isHistoricalLoading" class="w-full max-w-7xl mt-8">
        <div class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10">
          <h2 class="text-3xl font-bold text-center mb-6 text-white">{{ historicalChartTitle }} Trend (20-Year History)</h2>
          <div v-if="isHistoricalLoading" class="text-center text-slate-400">Chirping for historical trends...</div>
          <div v-else>
            <ComparisonChart chartType="line" :chartData="historicalChartData" />
          </div>
        </div>
      </section>

      <datalist id="country-list">
        <option v-for="country in allCountries" :key="country.id" :value="country.name"></option>
      </datalist>

    </div>
  </div>
</template>