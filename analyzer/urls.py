from django.urls import path
from . import views

urlpatterns = [
    path('', views.AiAnalyzer.as_view(), name='analyzer'),
    path('result', views.result, name='result'),
    path('raw_result', views.raw_result, name='raw_result'),
    path('analisador_store/', views.analyzer_store, name='analyzer_store'),
    path('get_result', views.get_result, name='get_result'),
    path('get_raw_result', views.get_raw_result, name='get_raw_result'),
    path('download/<str:file_type>', views.download_file, name='download'),
    path('error', views.error, name='error'),
    # path('download/<str:results_path>', views.download_file, name='download'),
]
