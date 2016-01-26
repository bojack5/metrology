#!/usr/bin/env python
from django import forms

class ContactoForm(forms.Form):
    """docstring for ContactoForm"""
    empresa = forms.CharField(max_length = 50)
    asunto  = forms.CharField(max_length = 50)
    email   = forms.EmailField()
    mensaje = forms.CharField(widget = forms.Textarea)	