from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.cache import cache


class CountryDataView(APIView):
    def get(self, request, country_code):
        # list of indicators
        indicators = {
            "population": "SP.POP.TOTL",
            "gdp": "NY.GDP.MKTP.CD",
            "gdp_per_capita": "NY.GDP.PCAP.CD",
            "ppp": "NY.GDP.MKTP.PP.CD",
            "gni_per_capita": "NY.GNP.PCAP.CD",
            "inflation": "FP.CPI.TOTL.ZG",
            "tax_rate": "IC.TAX.TOTL.CP.ZS"
        }
        country_data = {
            "country": None,
        }

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

        if country_data["country"] is None:
            return Response({"error": f"No data found for country code: {country_code}"},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(country_data, status=status.HTTP_200_OK)


# The list of all countries for the dropdown
class CountryListView(APIView):
    def get(self, request):
        url = "http://api.worldbank.org/v2/country?format=json&per_page=350"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # The second element ([1]) contains the list of countries
            if not (data and len(data) > 1):
                return Response({"error": "Invalid response from World Bank API"}, status=500)

            country_list = data[1]

            # Filter out non-country aggregates by checking for a valid 3-letter code.
            filtered_countries = [
                {"id": country["id"], "name": country["name"]}
                for country in country_list if len(country["id"]) == 3
            ]

            return Response(filtered_countries)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch country list: {e}"}, status=500)