from django.db import models

# Create your models here.


class UserMaster(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    otp = models.IntegerField()
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)


class Candidate(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE, default=0)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    min_salary = models.BigIntegerField(null=True, blank=True)
    max_salary = models.BigIntegerField(null=True, blank=True)
    job_type = models.CharField(max_length=150,default='')
    jobcategory = models.CharField(max_length=150,default='')
    country = models.CharField(max_length=150,default='')
    highestedu = models.CharField(max_length=150, default="")
    experience = models.CharField(max_length=150, default="")
    website = models.CharField(max_length=150, default="")
    shift = models.CharField(max_length=150, default="")
    jobdescription = models.CharField(max_length=500, default="")
    profile_pic = models.ImageField(upload_to="app/img/candidate")


class Company(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    company_name = models.CharField(max_length=150)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    website = models.CharField(max_length=150, default="")
    description = models.CharField(max_length=500, default="")
    logo_pic = models.ImageField(upload_to="app/img/company", default="")


class JobDetails(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default="")
    jobname = models.CharField(max_length=250, default="")
    companyname = models.CharField(max_length=250, default="")
    companyaddress = models.CharField(max_length=250, default="")
    jobdescription = models.TextField(max_length=500, default="")
    qualification = models.CharField(max_length=250, default="")
    responsibities = models.CharField(max_length=250, default="")
    location = models.CharField(max_length=250, default="")
    companywebsite = models.CharField(max_length=250, default="")
    companyemail = models.CharField(max_length=250, default="")
    companycontact = models.CharField(max_length=250, default="")
    salarypackage = models.CharField(max_length=250, default="")
    experience = models.IntegerField()
    logo = models.ImageField(upload_to="app/img/jobpost", default="")


class ApplyList(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(JobDetails, on_delete=models.CASCADE)
    education = models.CharField(max_length=200, default="")
    experience = models.IntegerField(default=0)
    min_salary = models.CharField(max_length=200)
    max_salary = models.CharField(max_length=200)
    resume = models.FileField(upload_to="app/resume")
