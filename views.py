import os
import pytesseract
import tempfile
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Import the user form
from .forms import (
    PdfForm,
    SummarizerForm,
    CustomUserCreationForm,
    LoginForm,
    AppUserCompanyForm,
    AppUserDepartmentForm,
    AppUserGSTextForm,
    APIFetchDataForm
)
from .pdf_ocr import pdf_ocr_process
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View
from .summarizer import Summarizer
from django.views.generic import FormView
import datetime
from django.contrib.auth import login
from .models import UserProfile, AppUserCompany, AppUserDepartment, AppUserGSText, APIFetchData
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


# Index is just to test that the Django WebServer is live
def index(request):
    if request.method == 'GET':
        return render(request, 'pdfocrsummarize/index.html')
    else:
        return HttpResponse("Invalid request method")


# This view facilitates the PDF Text and Image Extraction
def pdf_ocr(request):
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                output_filename = pdf_ocr_process(request.FILES['file'])
                output_dir = settings.PDF_OCR_OUTPUT_FOLDER
                messages.success(
                    request, f"File processed successfully. Output saved to: {os.path.join(output_dir, output_filename)}"
                )
                return redirect('pdfocrsummarize:pdf_ocr')
            except Exception as e:
                with open(settings.PDF_OCR_ERROR_LOG_PATH, 'a') as f:
                    f.write(f"Error: {str(e)}\n")
                messages.error(request, str(e))
                return redirect('pdfocrsummarize:pdf_ocr')
    else:
        form = PdfForm()
    return render(request, 'pdfocrsummarize/pdf_ocr.html', {'form': form})


# Summarizer View
class SummarizerView(FormView):
    template_name = 'pdfocrsummarize/summarizer.html'
    form_class = SummarizerForm
    success_template_name = 'pdfocrsummarize/summarizer_results.html'

    def form_valid(self, form):
        text_file = form.cleaned_data['text_file']
        sentence_count = form.cleaned_data['sentence_count']
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_file_path = f"{tmpdir}/{text_file.name}"
            with open(tmp_file_path, 'wb') as tmp_file:
                for chunk in text_file.chunks():
                    tmp_file.write(chunk)
            summarizer = Summarizer(tmp_file_path, sentence_count)
            results = summarizer.main()
            if results is not None:
                current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file_path = os.path.join(
                    settings.PDF_OCR_OUTPUT_FOLDER,
                    f"{text_file.name}_{current_datetime}_summarized.txt"
                )
                with open(output_file_path, 'w') as output_file:
                    import json
                    json.dump(results, output_file, indent=4)
                messages.success(
                    self.request, f"Summarized text saved to: {output_file_path}"
                )
                return render(self.request, self.success_template_name, {'results': results})
            else:
                messages.error(self.request, "Summarization failed.")
                return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form data.")
        return render(self.request, self.template_name, {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create the user profile
            user_profile = UserProfile(
                user=user,
                cuid=form.cleaned_data['cuid'],
                date_assigned=form.cleaned_data['date_assigned'],
                cash_app_name=form.cleaned_data['cash_app_name'],
                google_pay_integration=form.cleaned_data['google_pay_integration'],
                pay_pal_integration=form.cleaned_data['pay_pal_integration'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                sir_name=form.cleaned_data['sir_name'],
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                suffix_name=form.cleaned_data['suffix_name'],
                language=form.cleaned_data['language'],
                address=form.cleaned_data['address'],
                mobile_phone=form.cleaned_data['mobile_phone'],
                subscription_level=form.cleaned_data['subscription_level'],
                date_added=form.cleaned_data['date_added']
            )
            user_profile.save()

            # Automatically log in the user after registration
            login(request, user)
            messages.success(
                request, 'Registration successful! You are now logged in.')
            # Redirect to the index page
            return redirect('pdfocrsummarize:index')
        else:
            # If form is invalid, display errors in the template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'pdfocrsummarize/register.html', {'form': form})

# views.py


def login_view(request):  # Rename this function
    if request.method == 'POST':
        # Create a form instance with the posted data
        form = LoginForm(request.POST)
        if form.is_valid():  # Check if the form is valid
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,
                                password=password)  # Authenticate the user
            if user is not None:
                # Log the user in using the renamed function
                auth_login(request, user)
                # Redirect to a success page
                return redirect('pdfocrsummarize:index')
            else:
                # Add an error if authentication fails
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()  # Create a new form instance for GET requests

    # Render the login page with the form
    return render(request, 'pdfocrsummarize/login.html', {'form': form})

# Elevator App Tables
# AppUserCompany Views

    @login_required
    def appusercompany_list(request):
        companies = AppUserCompany.objects.all()
        return render(request, 'pdfocrsummarize/appusercompany_table.html', {'companies': companies})

    @login_required
    def appusercompany_create(request):
        # Create view for AppUserCompany
        pass

    @login_required
    def appusercompany_update(request, pk):
        company = AppUserCompany.objects.get(pk=pk)
        if request.method == 'POST':
            # Update company
            company.parent_company_name = request.POST['parent_company_name']
            company.email = request.POST['email']
            company.address = request.POST['address']
            company.website = request.POST['website']
            company.save()
        return redirect('appusercompany_list')

    @login_required
    def appusercompany_delete(request, pk):
        company = AppUserCompany.objects.get(pk=pk)
        if request.method == 'POST':
            # Delete company
            company.delete()
        return redirect('appusercompany_list')

# AppUserDepartment Views


def appuserdepartment_list(request):
    departments = AppUserDepartment.objects.all()
    return render(request, 'pdfocrsummarize/appuserdepartment_table.html', {'departments': departments})


def appuserdepartment_create(request):
    # Create view for AppUserDepartment
    pass


def appuserdepartment_update(request, pk):
    # Update view for AppUserDepartment
    pass


def appuserdepartment_delete(request, pk):
    # Delete view for AppUserDepartment
    pass


# AppUserGSText Views
def appusergstext_list(request):
    gstexts = AppUserGSText.objects.all()
    return render(request, 'pdfocrsummarize/appusergstext_table.html', {'gstexts': gstexts})


def appusergstext_create(request):
    # Create view for AppUserGSText
    pass


def appusergstext_update(request, pk):
    # Update view for AppUserGSText
    pass


def appusergstext_delete(request, pk):
    # Delete view for AppUserGSText
    pass


# APIFetchData Views
def apifetchdata_list(request):
    apidatas = APIFetchData.objects.all()
    return render(request, 'pdfocrsummarize/apifetchdata_table.html', {'apidatas': apidatas})


def apifetchdata_create(request):
    # Create view for APIFetchData
    pass


def apifetchdata_update(request, pk):
    # Update view for APIFetchData
    pass


def apifetchdata_delete(request, pk):
    # Delete view for APIFetchData
    pass

# AppUserCompany Create View


def appusercompany_create(request):
    if request.method == 'POST':
        form = AppUserCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created successfully!')
            return redirect('pdfocrsummarize:appusercompany_list')
    else:
        form = AppUserCompanyForm()
    return render(request, 'pdfocrsummarize/appusercompany_form.html', {'form': form})


# AppUserDepartment Create View
def appuserdepartment_create(request):
    if request.method == 'POST':
        form = AppUserDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('pdfocrsummarize:appuserdepartment_list')
    else:
        form = AppUserDepartmentForm()
    return render(request, 'pdfocrsummarize/appuserdepartment_form.html', {'form': form})


# AppUserGSText Create View
def appusergstext_create(request):
    if request.method == 'POST':
        form = AppUserGSTextForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'GSText created successfully!')
            return redirect('pdfocrsummarize:appusergstext_list')
    else:
        form = AppUserGSTextForm()
    return render(request, 'pdfocrsummarize/appusergstext_form.html', {'form': form})


# APIFetchData Create View
def apifetchdata_create(request):
    if request.method == 'POST':
        form = APIFetchDataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'APIFetchData created successfully!')
            return redirect('pdfocrsummarize:apifetchdata_list')
    else:
        form = APIFetchDataForm()
    return render(request, 'pdfocrsummarize/apifetchdata_form.html', {'form': form})

# AppUserCompany Update View


def appusercompany_update(request, pk):
    company = AppUserCompany.objects.get(pk=pk)
    if request.method == 'POST':
        form = AppUserCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('pdfocrsummarize:appusercompany_list')
    else:
        form = AppUserCompanyForm(instance=company)
    return render(request, 'pdfocrsummarize/appusercompany_form.html', {'form': form})


# AppUserDepartment Update View
def appuserdepartment_update(request, pk):
    department = AppUserDepartment.objects.get(pk=pk)
    if request.method == 'POST':
        form = AppUserDepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('pdfocrsummarize:appuserdepartment_list')
    else:
        form = AppUserDepartmentForm(instance=department)
    return render(request, 'pdfocrsummarize/appuserdepartment_form.html', {'form': form})


# AppUserGSText Update View
def appusergstext_update(request, pk):
    gstext = AppUserGSText.objects.get(pk=pk)
    if request.method == 'POST':
        form = AppUserGSTextForm(request.POST, instance=gstext)
        if form.is_valid():
            form.save()
            messages.success(request, 'GSText updated successfully!')
            return redirect('pdfocrsummarize:appusergstext_list')
    else:
        form = AppUserGSTextForm(instance=gstext)
    return render(request, 'pdfocrsummarize/appusergstext_form.html', {'form': form})


# APIFetchData Update View
def apifetchdata_update(request, pk):
    apidata = APIFetchData.objects.get(pk=pk)
    if request.method == 'POST':
        form = APIFetchDataForm(request.POST, instance=apidata)
        if form.is_valid():
            form.save()
            messages.success(request, 'APIFetchData updated successfully!')
            return redirect('pdfocrsummarize:apifetchdata_list')
    else:
        form = APIFetchDataForm(instance=apidata)
    return render(request, 'pdfocrsummarize/apifetchdata_form.html', {'form': form})

# AppUserCompany Delete View


def appusercompany_delete(request, pk):
    company = AppUserCompany.objects.get(pk=pk)
    if request.method == 'POST':
        company.delete()
        messages.success(request, 'Company deleted successfully!')
        return redirect('pdfocrsummarize:appusercompany_list')
    return render(request, 'pdfocrsummarize/appusercompany_confirm_delete.html', {'company': company})


# AppUserDepartment Delete View
def appuserdepartment_delete(request, pk):
    department = AppUserDepartment.objects.get(pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('pdfocrsummarize:appuserdepartment_list')
    return render(request, 'pdfocrsummarize/appuserdepartment_confirm_delete.html', {'department': department})


# AppUserGSText Delete View
def appusergstext_delete(request, pk):
    gstext = AppUserGSText.objects.get(pk=pk)
    if request.method == 'POST':
        gstext.delete()
        messages.success(request, 'GSText deleted successfully!')
        return redirect('pdfocrsummarize:appusergstext_list')
    return render(request, 'pdfocrsummarize/appusergstext_confirm_delete.html', {'gstext': gstext})


# APIFetchData Delete View
def apifetchdata_delete(request, pk):
    apidata = APIFetchData.objects.get(pk=pk)
    if request.method == 'POST':
        apidata.delete()
        messages.success(request, 'APIFetchData deleted successfully!')
        return redirect('pdfocrsummarize:apifetchdata_list')
    return render(request, 'pdfocrsummarize/apifetchdata_confirm_delete.html', {'apidata': apidata})
