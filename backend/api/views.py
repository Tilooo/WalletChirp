from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.cache import cache


class CountryDataView(APIView):
    def get(self, request, country_code):
        WORLD_BANK_API_BASE = "http://api.worldbank.org/v2/country"
        indicators = {
            "gdp": "NY.GDP.MKTP.CD",
            "gdp_per_capita": "NY.GDP.PCAP.CD",
            "ppp": "NY.GDP.MKTP.PP.CD",
            "population": "SP.POP.TOTL"
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


COUNTRY_LIST_CACHE_KEY = "country_list_data"


class CountryListView(APIView):
    """
    Provides a list of all available countries with their names and codes.
    """

    def get(self, request):
        cached_countries = cache.get(COUNTRY_LIST_CACHE_KEY)
        if cached_countries:
            return Response(cached_countries, status=status.HTTP_200_OK)

        url = "http://api.worldbank.org/v2/country?format=json&per_page=300"
        countries = []

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # The API returns a list; [0] is metadata, [1] is the data
            if data and len(data) > 1:
                for country in data[1]:
                    # Only want countries with an iso2Code, which are real countries
                    if country.get('iso2Code') and country['iso2Code'] != 'NA':
                        countries.append({
                            'id': country['id'],  # This is the 3-letter code, e.g., 'LTU'
                            'name': country['name'],  # pvz. 'Lithuania'
                        })

            # Stores the freshly fetched list in the cache for 24 hours (86400 seconds)
            cache.set(COUNTRY_LIST_CACHE_KEY, countries, 86400)

            return Response(countries, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to fetch country list from World Bank API: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )