from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import get_user_model


class customUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'enter password'}))

    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Again enter password'}))

    first_name = forms.CharField(label="First Name", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'E-mail'})}
    


class custom_login(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'autofocus': True}),
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class CustomChangeProfileForm(UserChangeForm):
    # email = forms.EmailField(label='E-mail',widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': True}))
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'profile_image']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control',}),
        }

   