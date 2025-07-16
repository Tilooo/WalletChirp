<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// --- STATE MANAGEMENT ---
const allCountries = ref([]); // holds a big list of countries

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
          <!-- Results Card 1 -->
          <div class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10 transition-all duration-300 ease-in-out hover:scale-105 hover:-translate-y-2 hover:shadow-2xl min-h-[300px] flex items-center justify-center">
            <div v-if="isLoading1" class="text-slate-400">Chirping...</div>
            <div v-else-if="error1" class="text-red-400 text-center"><strong>Oops!</strong><br/>{{ error1 }}</div>
            <div v-else-if="countryData1 && countryData1.country" class="w-full">
              <h2 class="text-2xl font-bold mb-4 border-b border-white/10 pb-2">{{ countryData1.country.name }}</h2>
              <ul class="space-y-3 text-sm">
                <li v-if="countryData1.population" class="flex justify-between items-center"><span class="font-semibold">Population ({{ countryData1.population.year }})</span><span class="text-lime-300 font-mono text-lg">{{ formatNumber(countryData1.population.value) }}</span></li>
                <li v-if="countryData1.gdp" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.gdp.name }} ({{ countryData1.gdp.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData1.gdp.value) }}</span></li>
                <li v-if="countryData1.gdp_per_capita" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.gdp_per_capita.name }} ({{ countryData1.gdp_per_capita.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData1.gdp_per_capita.value) }}</span></li>
                <li v-if="countryData1.gni_per_capita" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.gni_per_capita.name }} ({{ countryData1.gni_per_capita.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData1.gni_per_capita.value) }}</span></li>
                <li v-if="countryData1.ppp" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.ppp.name }} ({{ countryData1.ppp.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData1.ppp.value) }}</span></li>
                <li v-if="countryData1.inflation" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.inflation.name }} ({{ countryData1.inflation.year }})</span><span class="text-red-400 font-mono text-lg">{{ formatNumber(countryData1.inflation.value) }}%</span></li>
                <li v-if="countryData1.tax_rate" class="flex justify-between items-center"><span class="font-semibold">{{ countryData1.tax_rate.name }} ({{ countryData1.tax_rate.year }})</span><span class="text-red-400 font-mono text-lg">{{ formatNumber(countryData1.tax_rate.value) }}%</span></li>
              </ul>
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
          <!-- Results Card 2 -->
          <div class="relative p-6 rounded-xl shadow-lg bg-white/5 backdrop-blur-lg border border-white/10 transition-all duration-300 ease-in-out hover:scale-105 hover:-translate-y-2 hover:shadow-2xl min-h-[300px] flex items-center justify-center">
            <div v-if="isLoading2" class="text-slate-400">Chirping...</div>
            <div v-else-if="error2" class="text-red-400 text-center"><strong>Oops!</strong><br/>{{ error2 }}</div>
            <div v-else-if="countryData2 && countryData2.country" class="w-full">
              <h2 class="text-2xl font-bold mb-4 border-b border-white/10 pb-2">{{ countryData2.country.name }}</h2>
              <ul class="space-y-3 text-sm">
                <li v-if="countryData2.population" class="flex justify-between items-center"><span class="font-semibold">Population ({{ countryData2.population.year }})</span><span class="text-lime-300 font-mono text-lg">{{ formatNumber(countryData2.population.value) }}</span></li>
                <li v-if="countryData2.gdp" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.gdp.name }} ({{ countryData2.gdp.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData2.gdp.value) }}</span></li>
                <li v-if="countryData2.gdp_per_capita" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.gdp_per_capita.name }} ({{ countryData2.gdp_per_capita.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData2.gdp_per_capita.value) }}</span></li>
                <li v-if="countryData2.gni_per_capita" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.gni_per_capita.name }} ({{ countryData2.gni_per_capita.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData2.gni_per_capita.value) }}</span></li>
                <li v-if="countryData2.ppp" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.ppp.name }} ({{ countryData2.ppp.year }})</span><span class="text-lime-300 font-mono text-lg">${{ formatNumber(countryData2.ppp.value) }}</span></li>
                <li v-if="countryData2.inflation" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.inflation.name }} ({{ countryData2.inflation.year }})</span><span class="text-red-400 font-mono text-lg">{{ formatNumber(countryData2.inflation.value) }}%</span></li>
                <li v-if="countryData2.tax_rate" class="flex justify-between items-center"><span class="font-semibold">{{ countryData2.tax_rate.name }} ({{ countryData2.tax_rate.year }})</span><span class="text-red-400 font-mono text-lg">{{ formatNumber(countryData2.tax_rate.value) }}%</span></li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      <datalist id="country-list">
        <option v-for="country in allCountries" :key="country.id" :value="country.name"></option>
      </datalist>

    </div>
  </div>
</template>