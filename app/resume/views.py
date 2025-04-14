from django.shortcuts import render,redirect
from .models import *
from random import randint

# Create your views here.


def IndexPage(request):
   return render(request, "app/index.html")


def SignupPage(request):
   return render(request, "app/signup.html")


def RegisterUser(request):
   if request.POST["role"] == "Candidate":
      role = request.POST["role"]
      fname = request.POST["firstname"]
      lname = request.POST["lastname"]
      email = request.POST["email"]
      password = request.POST["password"]
      cpassword=request.POST["cpassword"]

      # server-side validation
      user = UserMaster.objects.filter(email=email)
      if user:
         message = "User already exist"
         return render(request, "app/signup.html", {"msg": message})
      else:
         if password == cpassword:
            otp = randint(100000, 999999)
            newuser = UserMaster.objects.create(
               role=role, otp=otp, email=email, password=password
               )
            newcand = Candidate.objects.create(
               user_id=newuser, firstname=fname, lastname=lname
               )
            return render(request, "app/otpverify.html",{'email':email})
   else:
      if request.POST["role"]=="Company":
         role=request.POST['role']
         fname=request.POST['firstname']
         lname=request.POST['lastname']
         email=request.POST['email']
         password=request.POST['password']
         cpassword=request.POST['cpassword']
         
         user1=UserMaster.objects.filter(email=email)
         if user1:
            message="Company already exist"
            return render(request, "app/signup.html", {"msg":message})
         else:
            if password==cpassword:
               otp=randint(100000,999999)
               newuser1=UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
               newcomp=Company.objects.create(user_id=newuser1,firstname=fname,lastname=lname)
               return render(request, "app/otpverify.html",{'email':email})

def OTPPage(request):
   return render(request,"app/otpverify.html")

def Otpverify(request):
   email=request.POST['email']
   otp=int(request.POST['otp'])
   
   user=UserMaster.objects.get(email=email)
   if user:
      if user.otp==otp:
         message="Otp Verification Successful"
         return render(request,"app/login.html", {'msg':message})
      else:
         message="Otp is incorrect"
         return render(request,"app/otpverify.html",{'msg':message})
   else:
      return render(request,"app/signup.html")

def Loginpage(request):
   return render(request,"app/login.html")


def LoginUser(request):
   if request.method == "POST":
      # Validate 'role' key existence and non-empty value
      role = request.POST.get("role", None)
      if not role:
         message = "Please select a role."
         return render(request, "app/login.html", {"msg": message})

      email = request.POST.get("email")
      password = request.POST.get("password")

      try:
         # Match the user from the database
         user = UserMaster.objects.get(email=email)
         if user and user.password == password and user.role == role:
            if role == "Candidate":
               can = Candidate.objects.get(user_id=user)
               # Create sessions
               request.session["id"] = user.id
               request.session["role"] = user.role
               request.session["firstname"] = can.firstname
               request.session["lastname"] = can.lastname
               request.session["email"] = user.email
               return redirect("index")
            else:
               if role == "Company":
                  com=Company.objects.get(user_id=user)
                  # Create sessions
                  request.session["id"] = user.id
                  request.session["role"] = user.role
                  request.session["firstname"] = com.firstname
                  request.session["lastname"] = com.lastname
                  request.session["email"] = user.email
                  request.session['password'] = user.password
                  return redirect("companyindex")
         else:
            message = "Invalid email or password."
      except UserMaster.DoesNotExist:
         message = "User does not exist."

      return render(request, "app/login.html", {"msg": message})
   else:
      return render(request, "app/login.html")

def ProfilePage(request,pk):
   user=UserMaster.objects.get(pk=pk) 
   can=Candidate.objects.get(user_id=user)
   return render(request,"app/profile.html",{'user':user, 'can':can})

def UpdateProfile(request,pk):
   user=UserMaster.objects.get(pk=pk)
   if user.role=="Candidate":
      can=Candidate.objects.get(user_id=user)
      # breakpoint()
      can.country=request.POST['country'] #first country belongs to database field and second field is belongs to html input name
      can.state=request.POST['state']
      can.city=request.POST['city']
      can.job_type=request.POST['job_type']
      can.jobcategory=request.POST['jobcategory']
      can.highestedu=request.POST['highestedu']
      can.experience=request.POST['experience']
      can.website=request.POST['website']
      can.shift=request.POST['shift']
      can.jobdescription=request.POST['jobdescription']
      can.min_salary=request.POST['min_salary']
      can.max_salary=request.POST['max_salary']
      can.contact=request.POST['contact']
      can.gender=request.POST['gender']
      if 'image' in request.FILES:
         can.profile_pic=request.FILES['image']
      can.save()
      url=f'/profile/{pk}' #formatting url
      return redirect(url)

def JobListPage(request):
   all_job=JobDetails.objects.all() 
   return render(request,"app/company/jobpostlist.html",{'all_job':all_job})

def CandidateJobListPage(request):
   all_job=JobDetails.objects.all() 
   return render(request,"app/job-list.html",{'all_job':all_job})

def ApplyPage(request,pk):
   user=request.session['id']
   if user:
      cand=Candidate.objects.get(user_id=user)
      job=JobDetails.objects.get(id=pk)
   return render(request,"app/apply.html",{'user':user,'cand':cand,'job':job})

def apply_job(request,pk):
   user=request.session['id']
   if user:
      can=Candidate.objects.get(user_id=user)
      job=JobDetails.objects.get(id=pk)
      edu=request.POST['education']
      exp=request.POST['experience']
      min_salary = request.POST['minsalary']
      max_salary = request.POST['maxsalary']
      resume = request.FILES['resume']
      newapply=ApplyList.objects.create(candidate=can,education=edu,experience=exp,job=job,min_salary=min_salary,max_salary=max_salary,resume=resume)
      message="Job Applied successful"
      return render(request,"app/apply.html",{'msg':message})

########## Company Side ###########

def CompanyIndexPage(request):
   return render(request,"app/company/index.html")

def CompanyProfile(request,pk):
   user=UserMaster.objects.get(pk=pk)
   comp=Company.objects.get(user_id=user)
   return render(request,"app/company/profile.html",{'user':user,'comp':comp})

def CompanyProfileUpdate(request, pk):
   user = UserMaster.objects.get(pk=pk)
   if user.role == "Company":
      comp = Company.objects.get(user_id=user)
      comp.firstname = request.POST['firstname']
      comp.lastname = request.POST['lastname']
      comp.company_name = request.POST['company_name']
      comp.state = request.POST['state']
      comp.city = request.POST['city']
      comp.contact = request.POST['contact']
      comp.address = request.POST['address']
      comp.website = request.POST['website']
      comp.description = request.POST['description']

      # Handling file upload (image)
      if 'image' in request.FILES:
         comp.logo_pic = request.FILES['image']
      comp.save()
      url = f"/companyProfile/{pk}"
      return redirect(url)

def JobPostPage(request):
   return render(request,"app/company/jobpost.html")

def JobDetailSubmit(request):
   user_id=request.session.get('id')
   user = UserMaster.objects.get(id=user_id)
   if user.role == "Company":
      comp = Company.objects.get(user_id=user)
      jobname = request.POST["jobname"]
      companyname = request.POST["companyname"]
      companyaddress = request.POST["companyaddress"]
      companyemail = request.POST["companyemail"]
      jobdescription = request.POST["jobdescription"]
      qualification = request.POST["qualification"]
      companycontact = request.POST["companycontact"]
      responsibities = request.POST["responsibities"]
      location = request.POST["location"]
      companywebsite = request.POST["companywebsite"]
      salarypackage = request.POST["salarypackage"]
      experience = request.POST["experience"]
      logo = request.FILES.get("image")


      newjob = JobDetails.objects.create(
            company_id=comp,
            jobname=jobname,
            companyname=companyname,
            companyaddress=companyaddress,
            jobdescription=jobdescription,
            qualification=qualification,
            responsibities=responsibities,
            companywebsite=companywebsite,
            location=location,
            companyemail=companyemail,
            companycontact=companycontact,
            salarypackage=salarypackage,
            experience=experience,
            logo=logo
         )
      
      message="Job Posted Successfully"
      return render(request,"app/company/jobpost.html",{'msg':message})

def JobApplyList(request):
   all_jobapply=ApplyList.objects.all()
   return render(request,"app/company/applyjoblist.html",{'all_job':all_jobapply})

def CompanyLogout(request):
   del request.session['email']
   del request.session['password']
   return redirect('index')


############################ ADMIN SIDE #######################################

def admin_login_page(request):
   return render(request,"app/admin/login.html")

def admin_index_page(request):
   if 'username' in request.session and 'password' in request.session:
      return render(request,"app/admin/index.html")
   else:
      return redirect('adminloginpage')

def admin_login(request):
   username=request.POST['username']
   password=request.POST['password']
   if username=="admin" and password=="admin":
      request.session['username']=username
      request.session['password']=password
      return redirect('adminindex')
   else:
      message="Username and Password does'nt match"
      return render(request,"app/admin/login.html",{'msg':message})

def admin_user_list(request):
   all_user=UserMaster.objects.filter(role="Candidate")
   return render(request,"app/admin/userlist.html",{'alluser':all_user})

def admin_company_list(request):
   all_company=UserMaster.objects.filter(role="Company")
   return render(request,"app/admin/companylist.html",{'allcompany':all_company})

def user_delete(request,pk):
   user=UserMaster.objects.get(pk=pk)
   user.delete()
   return redirect('userlist')

def verify_company_page(request,pk):
   company=UserMaster.objects.get(pk=pk)
   if company:
      return render(request,"app/admin/verify.html",{'company':company})

def verify_company(request, pk):
   company = UserMaster.objects.get(pk=pk)
   if request.method == 'POST':
      verify_status = request.POST.get('verify')
      if verify_status == 'True':
         company.is_verified = True 
      elif verify_status == 'False':
         company.is_verified = False
      company.save()
      return redirect('companylist')  
   return render(request, "app/admin/verify.html", {'company': company})


def company_delete(request,pk):
   company=UserMaster.objects.get(pk=pk)
   company.delete()
   return redirect('companylist')