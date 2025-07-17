from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"COULD NOT CONFIGURE GOOGLE AI: {e}")
    model = None


# Main view for detailed country data
class CountryDataView(APIView):
    def get(self, request, country_code):
        indicators = {
            "population": "SP.POP.TOTL",
            "gdp": "NY.GDP.MKTP.CD",
            "gdp_per_capita": "NY.GDP.PCAP.CD",
            "ppp": "NY.GDP.MKTP.PP.CD",
            "gni_per_capita": "NY.GNP.PCAP.CD",
            "inflation": "FP.CPI.TOTL.ZG",
            "tax_rate": "IC.TAX.TOTL.CP.ZS",
            "debt_to_gdp": "GC.DOD.TOTL.GD.ZS"
        }
        country_data = {"country": None}

        # World Bank Data Fetching Loop
        for key, indicator_id in indicators.items():
            url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_id}?format=json&mrnev=1"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                if data and len(data) > 1 and data[1]:
                    latest_data_point = data[1][0]
                    if country_data["country"] is None:
                        country_data["country"] = {
                            "id": latest_data_point['country']['id'],
                            "name": latest_data_point['country']['value'],
                        }
                    country_data[key] = {
                        "value": latest_data_point.get('value'),
                        "year": latest_data_point.get('date'),
                        "name": latest_data_point['indicator']['value']
                    }
                else:
                    country_data[key] = None
            except requests.exceptions.RequestException:
                return Response({"error": "Failed to fetch data from World Bank API."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Error check if no data was found at all
        if country_data["country"] is None:
            return Response({"error": f"No data found for country code: {country_code}"},
                            status=status.HTTP_404_NOT_FOUND)


        # AI tax summary section
        tax_summary = "Tax summary not available."
        country_name = country_data.get("country", {}).get("name")

        if model and country_name:
            try:
                prompt = f"Provide a brief summary of the main personal and corporate income tax rates for {country_name}. Focus on the key percentages. Be concise and start directly with the information. Example: 'Personal income tax is progressive from X% to Y%. Corporate tax is Z%.'"
                response = model.generate_content(prompt)
                tax_summary = response.text.strip()
            except Exception as e:
                print(f"AI generation failed for {country_name}: {e}")
                tax_summary = "Could not generate tax summary."

        country_data["tax_summary"] = tax_summary

        # Final, successful response
        return Response(country_data, status=status.HTTP_200_OK)


class CountryListView(APIView):
    def get(self, request):
        url = "http://api.worldbank.org/v2/country?format=json&per_page=350"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if not (data and len(data) > 1):
                return Response({"error": "Invalid response from World Bank API"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            country_list = data[1]
            filtered_countries = [
                {"id": country["id"], "name": country["name"]}
                for country in country_list if len(country["id"]) == 3
            ]
            return Response(filtered_countries)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch country list: {e}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)