from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        # cleaned_data = super().clean() super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user = authenticate(
            username=username,
            password=password
        )
        if not self.user:
            raise forms.ValidationError(
                'Invalid login credentials'
            )
        else:
            setattr(self, 'login', self._login)

    def _login(self, request):
        django_login(request, self.user)


# class SignupForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control'
#             }
#         )
#     )
#     password = forms.CharField(
#         required=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control'
#             }
#         )
#     )
#     password2 = forms.CharField(
#         required=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control'
#             }
#         )
#     )
#     age = forms.IntegerField(
#         widget=forms.NumberInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'img_profile',
            'age',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-contol',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

