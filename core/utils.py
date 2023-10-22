from django.utils.translation import activate

from rest_framework import permissions
from rest_framework.request import Request
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def translate(request: Request):
    try:
        request.LANGUAGE_CODE = request.headers['Accept_Language']
        activate(request.LANGUAGE_CODE)
    except:
        request.LANGUAGE_CODE = 'en-us'


# swagger
schema_view = get_schema_view(
   openapi.Info(
      title="BackendTask API",
      default_version='v1',
      description="BackendTask API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
