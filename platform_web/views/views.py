from django.views.generic import TemplateView, ListView, DetailView
from platform_web.forms import CustomLoginForm, CustomSignupForm

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout

# from .models import Vacancy
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic.edit import FormView
from django.contrib.auth import login as auth_login
from django.contrib import messages

from django.shortcuts import redirect



# class HomeView(TemplateView):
#     template_name = "website/pages/home.html"


# class ContactView(TemplateView):
#     template_name = "website/pages/contact.html"


# class CustomLoginView(LoginView):
#     template_name = "website/account/login.html"
#     authentication_form = CustomAuthenticationForm
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         return reverse_lazy("home")


# class SignupView(FormView):
#     template_name = "website/account/signup.html"
#     form_class = SignupForm
#     success_url = reverse_lazy("home")

#     def form_valid(self, form):
#         user = form.save()
#         auth_login(self.request, user)
#         messages.success(self.request, "Signup successful. You are now logged in.")
#         return super().form_valid(form)





# class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Vacancy
#     template_name = "website/pages/job_confirm_delete.html"
#     success_url = reverse_lazy("jobs")

#     def test_func(self):
#         return self.request.user.is_staff


# class JobsView(ListView):
#     model = Vacancy
#     template_name = "website/pages/jobs.html"
#     context_object_name = "vacancies"

#     def get_queryset(self):
#         return Vacancy.objects.filter(is_active=True).order_by("-publish_date")


# class JobDetailView(DetailView):
#     model = Vacancy
#     template_name = "website/pages/job_single.html"
#     context_object_name = "vacancy"
#     pk_url_kwarg = "id"

#     def get_object(self, queryset=None):
#         return super().get_object(queryset)


# class JobCreateView(LoginRequiredMixin, CreateView):
#     model = Vacancy
#     form_class = JobForm
#     template_name = "website/pages/job_add.html"

#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(self.get_success_url())


# class JobEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Vacancy
#     form_class = JobForm
#     template_name = "website/pages/job_edit.html"
#     context_object_name = "form"
#     pk_url_kwarg = "pk"

#     def test_func(self):
#         return self.request.user.is_staff

#     def get_success_url(self):
#         return reverse_lazy("job_single", kwargs={"id": self.get_object().pk})
