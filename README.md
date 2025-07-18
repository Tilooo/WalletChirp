WalletChirp 💸
Welcome to WalletChirp! This is a modern, full-stack web application designed to make exploring and comparing the economies of different countries simple, beautiful, and insightful. Using real-time data and AI-powered summaries, WalletChirp provides a comprehensive snapshot of a nation's financial health.
This project was built step-by-step, integrating a powerful Python/Django backend with a reactive Vue.js frontend.
🚀 Features
WalletChirp is packed with features to provide a rich user experience:
Dual Country Comparison: Analyze two countries side-by-side in a clean, responsive layout.
Rich Data Points: Fetches up-to-date financial metrics from the World Bank API, including:
GDP & GDP per Capita
GNI per Capita & PPP
Population & Inflation Rate
Central Government Debt (% of GDP)
AI-Powered Summaries:
Economic Chirp: An AI-generated summary of a country's economic strengths and challenges.
Tax Chirp: A concise summary of the main personal and corporate tax rates.
Data Visualization:
Bar Charts: Instantly compare key metrics between the two selected countries.
Historical Line Charts: Click on a metric to see a 20-year trend analysis for both countries.
Modern UI/UX:
Glassmorphism Design: Beautiful blurred-background cards.
Loading Skeletons: A professional loading state that improves perceived performance.
Interactive & Responsive: Smooth hover effects and a layout that works on all screen sizes.
User-Friendly Search: Autocomplete search box with a full list of countries.
🛠️ Tech Stack
This project utilizes a modern, full-stack architecture:
Backend
Python 3
Django & Django REST Framework for creating a robust API.
Google Generative AI for generating intelligent summaries.
Requests for communicating with external APIs.
python-dotenv for secure management of environment variables.
Frontend
Vue.js 3 (with the Composition API).
Vite as the blazing-fast build tool.
Tailwind CSS for a utility-first, modern design system.
Chart.js & vue-chartjs for interactive data visualizations.
Axios for making API requests to the backend.
🗺️ Future Roadmap
WalletChirp has a bright future! Here are some features planned:
Clear/Reset Button: A simple button to clear the historical trend chart.
Currency Conversion: Allow users to view monetary values in currencies other than USD.
User Accounts: Implement user registration and login to save favorite comparisons.
🙏 Acknowledgments
World Bank Open Data for providing comprehensive and free economic data.
Google AI for the powerful AI model that makes intelligent summaries possible.
