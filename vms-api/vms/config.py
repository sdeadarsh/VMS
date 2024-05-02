from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Snippets API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@snippets.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(AllowAny,),
# )


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),

)

# Define the token authentication scheme
token_auth = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Token-based authentication",
    type=openapi.TYPE_STRING
)

# Include the token authentication scheme in the Swagger documentation
schema_view.public = True  # Allow unauthorized access to Swagger UI
schema_view.authentication_classes = []  # Disable authentication for Swagger UI
schema_view.permission_classes = []  # Disable permission checks for Swagger UI
schema_view.exclude_from_schema = []  # Include all views in schema, including those with permission classes
schema_view.public_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']  # Define allowed HTTP methods

schema_view.schema = None  # Clear default security definitions
schema_view.security = [{'Token': []}]  # Define the 'Token' security requirement
schema_view.components = {'securitySchemes': {'Token': token_auth}}  # Define the 'Token' security scheme
