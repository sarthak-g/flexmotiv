from django import forms

class AccountTypeForm(forms.Form):
    c  = [("1","Main"),("2","BIRAC")]
    choices = forms.ChoiceField(choices=c, label="Select Account Type")
