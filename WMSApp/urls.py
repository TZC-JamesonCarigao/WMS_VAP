# WMSApp/urls.py
from django.urls import path
from .views import (
    ProductionRecordListView, ProductionRecordCreateView,
    ProductionRecordUpdateView, ProductionRecordDeleteView,
    dashboard_view, export_to_excel, ImportDataView
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('reports/', ProductionRecordListView.as_view(), name='report_list'),
    path('reports/create/', ProductionRecordCreateView.as_view(), name='create'),
    path('reports/edit/<int:pk>/', ProductionRecordUpdateView.as_view(), name='edit'),
    path('reports/delete/<int:pk>/', ProductionRecordDeleteView.as_view(), name='delete'),
    path('reports/export/', export_to_excel, name='export_excel'),
    path('reports/import/', ImportDataView.as_view(), name='import_data'),
]