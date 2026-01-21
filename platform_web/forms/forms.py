# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User
# # from .models import Vacancy


# class SignupForm(forms.ModelForm):
#     password = forms.CharField(
#         label="Пароль",
#         widget=forms.PasswordInput(
#             attrs={"class": "form-control", "placeholder": "Пароль"}
#         )
#     )
#     password2 = forms.CharField(
#         label="Підтвердіть пароль",
#         widget=forms.PasswordInput(
#             attrs={"class": "form-control", "placeholder": "Підтвердіть пароль"}
#         ),
#     )

#     class Meta:
#         model = User
#         fields = ("username", "email")
#         labels = {
#             "username": "Ім'я користувача",
#             "email": "Електронна адреса",
#         }
#         widgets = {
#             "username": forms.TextInput(
#                 attrs={"class": "form-control", "placeholder": "Ім'я користувача"}
#             ),
#             "email": forms.EmailInput(
#                 attrs={"class": "form-control", "placeholder": "Електронна адреса"}
#             ),
#         }

#     def clean_password2(self):
#         password = self.cleaned_data.get("password")
#         password2 = self.cleaned_data.get("password2")
#         if password and password2 and password != password2:
#             raise forms.ValidationError("Паролі не співпадають")
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user


# class CustomAuthenticationForm(AuthenticationForm):
#     error_messages = {
#         "invalid_login": "Ви ввели невірне ім'я користувача або пароль. Будь ласка, перевірте ще раз і спробуйте знову.",
#         "inactive": "Цей обліковий запис неактивний. Будь ласка, зверніться до служби підтримки."
#     }


# # class JobForm(forms.ModelForm):
# #     class Meta:
# #         model = Vacancy
# #         fields = "__all__"
# #         labels = {
# #             "company": "Компанія",
# #             "position_title": "Назва вакансії",
# #             "location": "Місцезнаходження",
# #             "employment_type": "Тип зайнятості",
# #             "salary_from": "Мінімальна зарплата",
# #             "salary_to": "Максимальна зарплата",
# #             "salary_note": "Примітка до зарплати",
# #             "url": "Посилання",
# #             "is_active": "Активна",
# #             "publish_date": "Дата публікації",
# #             "active_until": "Актуально до",
# #             "job_description": "Опис вакансії",
# #             "experience_required": "Необхідний досвід",
# #             "education_level": "Освітній рівень",
# #             "industry": "Індустрія",
# #             "icon_id": "Іконка",
# #         }
# #         widgets = {
# #             "position_title": forms.TextInput(
# #                 attrs={"class": "form-control", "placeholder": "Введіть назву вакансії"}
# #             ),
# #             "job_description": forms.Textarea(
# #                 attrs={
# #                     "class": "form-control",
# #                     "rows": 5,
# #                     "placeholder": "Введіть опис вакансії",
# #                 }
# #             ),
# #             "location": forms.TextInput(
# #                 attrs={"class": "form-control", "placeholder": "Введіть місцезнаходження"}
# #             ),
# #             "salary_from": forms.NumberInput(
# #                 attrs={"class": "form-control", "placeholder": "Мінімальна зарплата"}
# #             ),
# #             "salary_to": forms.NumberInput(
# #                 attrs={"class": "form-control", "placeholder": "Максимальна зарплата"}
# #             ),
# #             "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
# #         }

# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         for field_name, field in self.fields.items():
# #             if field_name not in ["is_active", "employment_type"]:
# #                 field.widget.attrs["class"] = (
# #                     field.widget.attrs.get("class", "") + " form-control"
# #                 )
