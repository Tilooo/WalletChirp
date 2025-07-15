from django.urls import path
from .views import CountryDataView, CountryListView


urlpatterns = [
    path('country/<str:country_code>/', CountryDataView.as_view(), name='country-data'),  # This matches URLs like /api/country/usa/
    path('countries/', CountryListView.as_view(), name='country-list'), # Endpoint for the full country list, e.g., /api/countries/
]