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

        # * AI summaries section *
        economic_summary = "Economic summary not available."
        tax_summary = "Tax summary not available."
        country_name = country_data.get("country", {}).get("name")

        if model and country_name:
            # Generate the Economic Chirp
            try:
                data_points = []
                gdp_pc_data = country_data.get('gdp_per_capita')
                if gdp_pc_data and gdp_pc_data.get('value') is not None:
                    try:
                        gdp_pc_value = int(gdp_pc_data['value'])
                        data_points.append(f"GDP per Capita of ${gdp_pc_value:,}")
                    except (ValueError, TypeError):
                        pass

                inflation_data = country_data.get('inflation')
                if inflation_data and inflation_data.get('value') is not None:
                    try:
                        inflation_value = float(inflation_data['value'])
                        data_points.append(f"an inflation rate of {inflation_value:.2f}%")
                    except (ValueError, TypeError):
                        pass

                debt_data = country_data.get('debt_to_gdp')
                if debt_data and debt_data.get('value') is not None:
                    try:
                        debt_value = float(debt_data['value'])
                        data_points.append(f"government debt at {debt_value:.2f}% of GDP")
                    except (ValueError, TypeError):
                        pass

                if data_points:
                    data_summary_string = ", ".join(data_points)
                    prompt_economic = (
                        f"You are 'WalletChirp', an economic analysis AI. For {country_name}, with {data_summary_string}, "
                        f"write a concise, one-paragraph 'Economic Chirp'. Analyze these figures for a non-expert, "
                        f"highlighting one strength and one challenge. Keep it brief and insightful."
                    )
                    response_economic = model.generate_content(prompt_economic)
                    economic_summary = response_economic.text.strip()
                else:
                    economic_summary = "Not enough data to generate a summary."
            except Exception as e:
                print(f"AI economic summary generation failed for {country_name}: {e}")
                economic_summary = "Could not generate economic summary."

            # Generate the Tax Chirp
            try:
                prompt_tax = (
                    f"For {country_name}, provide a brief summary of the main personal and corporate income tax rates. "
                    f"Focus on the key percentages. Be concise and start directly with the information. "
                    f"Example: 'Personal income tax is progressive from X% to Y%. Corporate tax is Z%.'"
                )
                response_tax = model.generate_content(prompt_tax)
                tax_summary = response_tax.text.strip()
            except Exception as e:
                print(f"AI tax summary generation failed for {country_name}: {e}")
                tax_summary = "Could not generate tax summary."

        # BOTH summaries to response data
        country_data["economic_summary"] = economic_summary
        country_data["tax_summary"] = tax_summary

        # successful response
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


class HistoricalDataView(APIView):
    def get(self, request, country_code, indicator_code):
        # Defined the last 20 years.
        date_range = "2004:2024"

        url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json&date={date_range}&per_page=50"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if not (data and len(data) > 1 and data[1]):
                # an empty list if no data is found
                return Response([], status=status.HTTP_200_OK)

            # The World Bank returns the most recent year first.
            historical_data = [
                {"year": item["date"], "value": item["value"]}
                for item in reversed(data[1]) if item.get("value") is not None
            ]

            return Response(historical_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch historical data: {e}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)