from django.urls import path
from django.views.generic import TemplateView
# Ensure all views are imported
from .views import (
    index,
    pdf_ocr,
    SummarizerView,
    register,
    login_view,
    appusercompany_list,
    appusercompany_create,
    appusercompany_update,
    appusercompany_delete,
    appuserdepartment_list,
    appuserdepartment_create,
    appuserdepartment_update,
    appuserdepartment_delete,
    appusergstext_list,
    appusergstext_create,
    appusergstext_update,
    appusergstext_delete,
    apifetchdata_list,
    apifetchdata_create,
    apifetchdata_update,
    apifetchdata_delete
)
# Import Django's built-in LogoutView
from django.contrib.auth.views import LogoutView

app_name = 'pdfocrsummarize'

urlpatterns = [
    path('index/', index, name='index'),  # Home page
    path('pdf_ocr/', pdf_ocr, name='pdf_ocr'),  # PDF OCR page
    path('summarizer/', SummarizerView.as_view(),
         name='summarizer'),  # Summarizer page
    path('summarizer/results/', TemplateView.as_view(template_name='summarizer_results.html'),
         name='summarizer_results'),  # Results page
    path('register/', register, name='register'),  # Registration page
    path('login/', login_view, name='login'),  # Login page
    path('logout/', LogoutView.as_view(next_page='pdfocrsummarize:login'), name='logout'),

    # AppUserCompany URLs
    path('companies/', appusercompany_list, name='appusercompany_list'),
    path('companies/create/', appusercompany_create,
         name='appusercompany_create'),
    path('companies/<pk>/update/', appusercompany_update,
         name='appusercompany_update'),
    path('companies/<pk>/delete/', appusercompany_delete,
         name='appusercompany_delete'),

    # AppUserDepartment URLs
    path('departments/', appuserdepartment_list, name='appuserdepartment_list'),
    path('departments/create/', appuserdepartment_create,
         name='appuserdepartment_create'),
    path('departments/<pk>/update/', appuserdepartment_update,
         name='appuserdepartment_update'),
    path('departments/<pk>/delete/', appuserdepartment_delete,
         name='appuserdepartment_delete'),

    # AppUserGSText URLs
    path('gstexts/', appusergstext_list, name='appusergstext_list'),
    path('gstexts/create/', appusergstext_create, name='appusergstext_create'),
    path('gstexts/<pk>/update/', appusergstext_update,
         name='appusergstext_update'),
    path('gstexts/<pk>/delete/', appusergstext_delete,
         name='appusergstext_delete'),

    # APIFetchData URLs
    path('apidata/', apifetchdata_list, name='apifetchdata_list'),
    path('apidata/create/', apifetchdata_create, name='apifetchdata_create'),
    path('apidata/<pk>/update/', apifetchdata_update, name='apifetchdata_update'),
    path('apidata/<pk>/delete/', apifetchdata_delete, name='apifetchdata_delete'),
]
