# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
# from rest_framework import permissions

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Your API Name",
#         default_version='v1',
#         description="API description",
#         terms_of_service="https://www.example.com/terms/",
#         contact=openapi.Contact(email="contact@example.com"),
#         license=openapi.License(name="Your License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# def get_schema(request):
#     return schema_view.with_ui('swagger')(request)