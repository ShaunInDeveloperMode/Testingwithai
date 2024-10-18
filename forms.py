from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
# Ensure you have this model for additional fields
from .models import UserProfile, AppUserCompany, AppUserDepartment, AppUserGSText, APIFetchData


class PdfForm(forms.Form):
    file = forms.FileField(label='Select a PDF file')


class SummarizerForm(forms.Form):
    text_file = forms.FileField(label='Select text file')
    sentence_count = forms.IntegerField(
        label='Desired sentence count in summary',
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={'placeholder': 'Enter sentence count'})
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password_confirmation = forms.CharField(widget=forms.PasswordInput())
    cuid = forms.CharField(widget=forms.HiddenInput())
    date_assigned = forms.CharField(widget=forms.HiddenInput())
    cash_app_name = forms.CharField(widget=forms.HiddenInput())
    google_pay_integration = forms.CharField(widget=forms.HiddenInput())
    pay_pal_integration = forms.CharField(widget=forms.HiddenInput())
    date_of_birth = forms.DateField(label="Date of Birth", required=True)

    # Updated Gender Choices
    gender = forms.ChoiceField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('non_conforming', 'Non Conforming')
        ],
        label="Gender"
    )

    # Updated Sir Name Choices
    sir_name = forms.ChoiceField(
        choices=[
            ('human', 'Human'),
            ('mr', 'Mr.'),
            ('mrs', 'Mrs.'),
            ('ms', 'Ms.')
        ],
        label="Sir Name",
        required=False
    )

    first_name = forms.CharField(label="First Name", required=True)
    middle_name = forms.CharField(label="Middle Name", required=False)
    last_name = forms.CharField(label="Last Name", required=True)

    # Updated Suffix Choices
    suffix_name = forms.ChoiceField(
        choices=[
            ('', ''),
            ('I', 'I'),
            ('II', 'II'),
            ('III', 'III'),
            ('Sr.', 'Sr.'),
            ('Jr.', 'Jr.')
        ],
        required=False
    )

    # Updated Language Choices
    language = forms.ChoiceField(
        choices=[
            ('english', 'English'),
            ('mandarin', 'Mandarin Chinese'),
            ('hindi', 'Hindi'),
            ('spanish', 'Spanish'),
            ('french', 'French'),
            ('standard_arabic', 'Standard Arabic'),
            ('bengali', 'Bengali'),
            ('portuguese', 'Portuguese'),
            ('russian', 'Russian'),
            ('urdu', 'Urdu'),
            ('indonesian', 'Indonesian'),
            ('standard_german', 'Standard German')
        ],
        label="Language"
    )

    # Updated Subscription Level Choices
    subscription_level = forms.ChoiceField(
        choices=[
            ('partner', 'Partner'),
            ('free', 'Free'),
            ('professional', 'Professional'),
            ('executive', 'Executive')
        ],
        label="Subscription Level"
    )

    address = forms.CharField(widget=forms.Textarea, required=True)
    mobile_phone = forms.CharField(label="Mobile Phone", required=True)
    date_added = forms.DateField(label="Date Added", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = [
            'email', 'password1', 'password2', 'cuid', 'date_assigned', 'cash_app_name',
            'google_pay_integration', 'pay_pal_integration', 'date_of_birth', 'gender',
            'sir_name', 'first_name', 'middle_name', 'last_name', 'suffix_name', 'language',
            'address', 'mobile_phone', 'subscription_level', 'date_added'
        ]

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob > date.today():
            raise forms.ValidationError(
                "Date of Birth cannot be in the future.")
        return dob

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get(
            'email')  # Using email as the username
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))

# elevator app table forms


class AppUserCompanyForm(forms.ModelForm):
    class Meta:
        model = AppUserCompany
        fields = ('parent_company_name', 'email', 'address', 'website')


class AppUserDepartmentForm(forms.ModelForm):
    class Meta:
        model = AppUserDepartment
        fields = ('department', 'app_company_name', 'sub_int1', 'sub_int2',
                  'sub_int3', 'sub_int4', 'sub_int5', 'sub_int6', 'sub_int7',
                  'sub_int8', 'sub_int9', 'sub_int10', 'sub_int11', 'sub_int12',
                  'sub_int13', 'sub_int14', 'sub_int15', 'sub_int16', 'sub_int17',
                  'sub_int18', 'sub_int19', 'sub_int20')


class AppUserGSTextForm(forms.ModelForm):
    class Meta:
        model = AppUserGSText
        fields = ('department', 'gstext1', 'gstext2', 'gstext3', 'gstext4',
                  'gstext5', 'gstext6', 'gstext7', 'gstext8', 'gstext9', 'gstext10',
                  'gstext11', 'gstext12', 'gstext13', 'gstext14', 'gstext15',
                  'gstext16', 'gstext17', 'gstext18', 'gstext19', 'gstext20')


class APIFetchDataForm(forms.ModelForm):
    class Meta:
        model = APIFetchData
        fields = ('department', 'api_name', 'app_store_name', 'app_company_name',
                  'addapi_newapi_drop', 'addapi_api_focus_expl', 'addapi_api_key_required',
                  'addapi_api_key', 'addapi_username', 'addapi_password',
                  'addapi_public_or_private_drop', 'addapi_url', 'addapi_query',
                  'addapi_method', 'addapi_max_attempts', 'addapi_max_per_unit',
                  'addapi_description', 'addapi_terms_and_conditions',
                  'addapi_additional_notes_drop')
