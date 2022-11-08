from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Relation
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

class UserRegistration(View):

    form_class=UserRegistrationForm
    template_name='account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            cd=form.cleaned_data
            user=User.objects.create_user(cd['username'],
                                          cd['emailAdress'],
                                          cd['password'])
            user.first_name=cd['firstname']
            user.last_name=cd['lastname']
            user.save()
            messages.success(request,"user created succefully",'success')
            return redirect('home:home')

        messages.error(request,"got error in creating user",'danger')
        return render(request, self.template_name, {'form': form})

class UserLoginView(View):

    form_class=UserLoginForm
    template_name="account/userLogin.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,f'{cd["username"]} login succesfully', 'success' )
                return redirect('home:home')

            messages.error(request,"wrong username and password",'warning')
        return render(request,self.template_name,{'form':form})

class UserLogout(LoginRequiredMixin,View):

    def get(self,request):
        messages.success(request, f'{request.user} log out successfully')
        logout(request)

        return redirect("home:home")

class ProfileUserView(LoginRequiredMixin,View):

    def get(self,request,user_id):
        is_following=False

        user=User.objects.get(pk=user_id)
        posts=user.posts.all()
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            is_following=True
        return render(request,'account/profile.html',{'user':user,'posts':posts,'is_following':is_following})



class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")



class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):

    template_name = "account/password_reset_complete.html"


class UserFollow(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            messages.error(request,"you already followed this user",'danger')
        else:
            Relation(from_user=request.user,to_user=user).save() ##or Relation.objects.create(from_user=request.user,to_user=user)

            messages.success(request,"you follow this user now" ,'success')

        return redirect("account:profile_user",user.id)

class UserUnFollow(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()

            messages.success(request, "you  unfollowed this user now", 'success')
        else:

            messages.error(request, "you hadnt follow this user ", 'danger')

        return redirect("account:profile_user", user.id)