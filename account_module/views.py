from django.contrib.auth import login, logout
from django.template.defaulttags import comment
from django.urls import reverse
from django.utils.crypto import get_random_string

from .models import User
from django.http import HttpRequest, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from utils.email_service import send_email


from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm


# Create your views here.



class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)



    def post(self, request : HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_pass = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email
                )
                new_user.set_password(user_pass)
                new_user.save()
                activation_link = request.build_absolute_uri(reverse('activate_account_page',
                                                                     args=[new_user.email_active_code]))
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user, 'activation_link': activation_link}, 'emails/activate_account.html')
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))

        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))  # فقط در صورت موفقیت
                    else:
                        login_form.add_error('password', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)  # بازگشت به فرم لاگین با خطا


class LogoutView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
            return redirect(reverse('login_page'))
        else:
            return render(request, 'account_module/logout.html')


class ResetPasswordView(View):
    def get(self, request: HttpRequest, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_password_form = ResetPasswordForm()
        context = {
            'reset_password_form': reset_password_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, email_active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if reset_password_form.is_valid():
            if user is not None:
                new_password = reset_password_form.cleaned_data.get('new_password')
                user.set_password(new_password)
                email_active_code = get_random_string(72)
                user.email_active_code = email_active_code
                user.save()
                return redirect(reverse('login_page'))

        context = {
            'reset_password_form': reset_password_form,
            'user': user
        }

        return render(request, 'account_module/reset_password.html', context)



class ForgotPasswordView(View):
        def get(self, request: HttpRequest):
            forgot_password_form = ForgetPasswordForm()
            context = {
                'forgot_password_form': forgot_password_form
            }
            return render(request, 'account_module/forget_password.html', context)

        def post(self, request: HttpRequest):
            forget_password_form = ForgetPasswordForm(request.POST)
            if forget_password_form.is_valid():
                user_email = forget_password_form.cleaned_data.get('email')
                user: User = User.objects.filter(email__iexact=user_email).first()
                if user is not None:
                    activation_link = request.build_absolute_uri(reverse('reset_password_page',
                                                                         args=[user.email_active_code]))
                    send_email('بازیابی کلمه عبور', user.email, {'user': user, 'activation_link': activation_link}, 'emails/forget_password.html')
                    user.save()
                    return redirect(reverse('login_page'))
            context = {'forget_pass_form': forget_password_form}
            return render(request, 'account_module/forget_password.html', context)


class ActivateAccountView(View):
    def get(self, request: HttpRequest, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
            else:
                return redirect(reverse('home_page')) #kamel shavad
        else:
            raise Http404('error')