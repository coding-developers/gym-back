from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Academia CRUD API",
        default_version="v1",
        description="Documentação da API das academias — Arquitetura DDD (Companies, Students, Modalities, Financial, Administrative, Products)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="suporte@academia.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)


urlpatterns = [
    # Legacy routes (gym app)
    path("api/", include("gym.urls")),
    # DDD Bounded Context routes
    path("api/", include("company.urls")),
    path("api/", include("modalities.urls")),
    path("api/", include("financial.urls")),
    path("api/", include("administrative.urls")),
    path("api/", include("products.urls")),
    path("api/auth/", include("authentication.urls")),
    # Rotas do Swagger
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
