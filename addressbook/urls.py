from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactList.as_view(), name='addressbooklist_list'),
    path(
        'create_contact/',
        views.ContactCreate.as_view(template_name="addressbook/addressbooklist_create.html"),
        name='addressbooklist_create'
    ),
    path('update_contact/<int:pk>/',
         views.ContactUpdate.as_view(template_name="addressbook/addressbooklist_update.html"),
         name='addressbooklist_update'),
    path('delete_contact/<int:pk>/',
         views.ContactDelete.as_view(template_name="addressbook/addressbooklist_delete.html"),
         name='addressbooklist_delete'),
    path('upload-csv/',
         views.CSVImportView.as_view(),
         name='addressbooklist_import'),
    path('download-csv/',
         views.CSVExportView.as_view(),
         name='addressbooklist_export'),
]
