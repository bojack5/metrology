from django import forms

class LoginForm(forms.Form):
    """docstring for ContactoForm"""
    usuario = forms.CharField(max_length = 10)
    contrasena = forms.CharField(max_length = 15 , widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    """docstring for RegisterForm"""
    usuario    = forms.CharField(max_length = 10)
    nombre     = forms.CharField(max_length = 10)
    apellido   = forms.CharField(max_length = 10)
    email      = forms.CharField(max_length = 10)
    contrasena = forms.CharField(max_length = 15 , widget=forms.PasswordInput())

