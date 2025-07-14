from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


class CountryDataView(APIView):
    def get(self, request, country_code):
        WORLD_BANK_API_BASE = "http://api.worldbank.org/v2/country"
        indicators = {
            "gdp": "NY.GDP.MKTP.CD",
            "gdp_per_capita": "NY.GDP.PCAP.CD",
            "ppp": "NY.GDP.MKTP.PP.CD"
        }
        country_data = {
            "country": None,
        }

        for key, indicator_id in indicators.items():
            url = f"{WORLD_BANK_API_BASE}/{country_code}/indicator/{indicator_id}?format=json&mrnev=1"
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