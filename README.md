# 💸 WalletChirp 

<div align="center">
  <img src="placeholder.png" alt="WalletChirp Banner" width="800"/>
  <br/>
  <p>
    <b>A modern, full-stack web application designed to make exploring and comparing the economies of different countries simple, beautiful, and insightful.</b>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
    <img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D" alt="Vue.js" />
    <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  </p>
</div>

## ✨ Overview

WalletChirp provides a comprehensive snapshot of a nation's financial health using real-time data and AI-powered summaries. Built step-by-step with a powerful Python/Django backend and a reactive Vue.js frontend, it's designed for seamless economic comparisons.

## 🚀 Features

- **🌍 Dual Country Comparison:** Analyze two countries side-by-side in a clean, responsive layout.
- **📊 Rich Data Points:** Up-to-date metrics from the World Bank API:
  - GDP & GDP per Capita
  - GNI per Capita & PPP
  - Population & Inflation Rate
  - Central Government Debt (% of GDP)
- **🤖 AI-Powered Summaries (Gemini API):**
  - *Economic Chirp:* AI-generated summary of economic strengths and challenges.
  - *Tax Chirp:* Concise breakdown of personal and corporate tax rates.
- **📈 Data Visualization:**
  - Bar Charts: Instantly compare key metrics.
  - Historical Line Charts: Click a metric to see a 20-year trend analysis.
- **✨ Modern UI/UX:**
  - Glassmorphism Design: Beautiful blurred-background cards.
  - Loading Skeletons: Professional loading states for improved perceived performance.
  - User-Friendly Search: Autocomplete search box with a full country list.
  - Fully responsive, smooth hover effects, and accessible interactions.

## 🛠️ Tech Stack

### Backend
- **Framework:** Django & Django REST Framework
- **Language:** Python 3.10+
- **AI Integration:** Google Generative AI
- **External APIs:** World Bank API
- **Environment Management:** `python-dotenv`

### Frontend
- **Framework:** Vue.js 3 (Composition API)
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Data Visualization:** Chart.js & vue-chartjs
- **HTTP Client:** Axios
