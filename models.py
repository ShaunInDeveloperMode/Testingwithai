from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cuid = models.CharField(max_length=255, blank=False)
    date_assigned = models.DateField(null=True, blank=True)
    cash_app_name = models.CharField(max_length=255, blank=True)
    google_pay_integration = models.BooleanField(default=False)
    pay_pal_integration = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_conforming', 'Non Conforming')
    ])
    sir_name = models.CharField(max_length=20, choices=[
        ('human', 'Human'),
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
        ('ms', 'Ms.')
    ], blank=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    suffix_name = models.CharField(max_length=20, choices=[
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('Sr.', 'Sr.'),
        ('Jr.', 'Jr.')
    ], blank=True)
    language = models.CharField(max_length=50, choices=[
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
    ])
    address = models.TextField()
    mobile_phone = models.CharField(max_length=20)
    subscription_level = models.CharField(max_length=20, choices=[
        ('partner', 'Partner'),
        ('free', 'Free'),
        ('professional', 'Professional'),
        ('executive', 'Executive')
    ])
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AppUserCompany(models.Model):
    client_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_company_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    website = models.CharField(max_length=255)


class AppUserDepartment(models.Model):
    client_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    app_company_name = models.CharField(max_length=255)
    sub_int1 = models.CharField(max_length=255)
    sub_int2 = models.CharField(max_length=255)
    sub_int3 = models.CharField(max_length=255)
    sub_int4 = models.CharField(max_length=255)
    sub_int5 = models.CharField(max_length=255)
    sub_int6 = models.CharField(max_length=255)
    sub_int7 = models.CharField(max_length=255)
    sub_int8 = models.CharField(max_length=255)
    sub_int9 = models.CharField(max_length=255)
    sub_int10 = models.CharField(max_length=255)
    sub_int11 = models.CharField(max_length=255)
    sub_int12 = models.CharField(max_length=255)
    sub_int13 = models.CharField(max_length=255)
    sub_int14 = models.CharField(max_length=255)
    sub_int15 = models.CharField(max_length=255)
    sub_int16 = models.CharField(max_length=255)
    sub_int17 = models.CharField(max_length=255)
    sub_int18 = models.CharField(max_length=255)
    sub_int19 = models.CharField(max_length=255)
    sub_int20 = models.CharField(max_length=255)

    def get_sub_ints(self):
        return [getattr(self, f'sub_int{i}') for i in range(1, 21)]


class AppUserGSText(models.Model):
    client_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    gstext1 = models.CharField(max_length=255)
    gstext2 = models.CharField(max_length=255)
    gstext3 = models.CharField(max_length=255)
    gstext4 = models.CharField(max_length=255)
    gstext5 = models.CharField(max_length=255)
    gstext6 = models.CharField(max_length=255)
    gstext7 = models.CharField(max_length=255)
    gstext8 = models.CharField(max_length=255)
    gstext9 = models.CharField(max_length=255)
    gstext10 = models.CharField(max_length=255)
    gstext11 = models.CharField(max_length=255)
    gstext12 = models.CharField(max_length=255)
    gstext13 = models.CharField(max_length=255)
    gstext14 = models.CharField(max_length=255)
    gstext15 = models.CharField(max_length=255)
    gstext16 = models.CharField(max_length=255)
    gstext17 = models.CharField(max_length=255)
    gstext18 = models.CharField(max_length=255)
    gstext19 = models.CharField(max_length=255)
    gstext20 = models.CharField(max_length=255)

    def get_gstexts(self):
        return [getattr(self, f'gstext{i}') for i in range(1, 21)]


class APIFetchData(models.Model):
    client_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=255, null=True, blank=True)
    api_name = models.CharField(max_length=255)
    app_store_name = models.CharField(max_length=255, null=True, blank=True)
    app_company_name = models.CharField(max_length=255, null=True, blank=True)
    addapi_newapi_drop = models.BooleanField(null=True, blank=True)
    addapi_api_focus_expl = models.CharField(
        max_length=255, null=True, blank=True)
    addapi_api_key_required = models.BooleanField(null=True, blank=True)
    addapi_api_key = models.CharField(max_length=255, null=True, blank=True)
    addapi_username = models.CharField(max_length=255, null=True, blank=True)
    addapi_password = models.CharField(max_length=255, null=True, blank=True)
    addapi_public_or_private_drop = models.CharField(
        max_length=255, null=True, blank=True)
    addapi_url = models.CharField(max_length=255, null=True, blank=True)
    addapi_query = models.CharField(max_length=255, null=True, blank=True)
    addapi_method = models.CharField(max_length=255, null=True, blank=True)
    addapi_max_attempts = models.IntegerField(null=True, blank=True)
    addapi_max_per_unit = models.CharField(
        max_length=255, null=True, blank=True)
    addapi_description = models.CharField(
        max_length=255, null=True, blank=True)
    addapi_terms_and_conditions = models.CharField(
        max_length=255, null=True, blank=True)
    addapi_additional_notes_drop = models.CharField(
        max_length=255, null=True, blank=True)
