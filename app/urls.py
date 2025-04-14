from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.IndexPage, name="index"),
    path("signup/", views.SignupPage, name="signup"),
    path("register/", views.RegisterUser, name="register"),
    path("otppage/", views.OTPPage, name="otppage"),
    path("otp/", views.Otpverify, name="otp"),
    path("loginpage/", views.LoginPage, name="loginpage"),
    path("loginuser/", views.LoginUser, name="login"),
    path("profile/<int:pk>", views.ProfilePage, name="profile"),
    path("updateprofile/<int:pk>", views.UpdateProfile, name="updateprofile"),
    path("joblist/", views.CandidateJobListPage, name="joblist"),
    path("logout/", views.LogoutUser, name="logout"),
    path("apply/<int:pk>",views.ApplyPage,name="apply"),
    path("applyjob/<int:pk>",views.ApplyJob,name="applyjob"),

    ############## company side ##################
    path("companyindex/", views.CompanyIndexPage, name="companyindex"),
    path("companyprofile/<int:pk>", views.CompanyProfile, name="companyprofile"),
    path(
        "updatecompanyprofile/<int:pk>",
        views.CompanyProfileUpdate,
        name="updatecompanyprofile",
    ),
    path("jobpostpage", views.JobPostPage, name="jobpostpage"),
    path("jobpost/", views.JobDetailSubmit, name="jobpost"),
    path("jobpostlistpage/", views.JobListPage, name="joblistpage"),
    path("companylogout/", views.CompanyLogout, name="companylogout"),
    path("applyjoblist/",views.JobApplyList,name="applylist"),

    ############## Admin Side ####################
    path("adminloginpage/",views.AdminLoginPage,name="adminloginpage"),
    path("adminindex/",views.AdminIndexPage,name="adminindex"),
    path("adminlogin/",views.AdminLogin,name="adminlogin"),
    path("adminuserlist/",views.AdminUserList,name="userlist"),
    path("admincompanylist/",views.AdminCompanyList,name="companylist"),
    path("deleteuser/<int:pk>",views.UserDelete,name="userdelete"),
    path("verifycompanypage/<int:pk>",views.VerifyCompanyPage,name="verifypage"),
    path("verifycompany/<int:pk>",views.VerifyCompany,name="verify"),
    path("deletecompany/<int:pk>",views.CompanyDelete,name="companydelete"),
    path("logoutadmin/",views.LogoutAdmin,name="logoutadmin"),
]
