from django.urls import path
from .views import CountryDataView

urlpatterns = [
    # This matches URLs like /api/country/usa/
    path('country/<str:country_code>/', CountryDataView.as_view(), name='country-data'),
]