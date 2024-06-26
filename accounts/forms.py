from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .widgets.checkbox_input_with_label import CheckboxInputWithLabel
from django.utils.safestring import mark_safe

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='Nome')
    last_name = forms.CharField(required=True, label='Sobrenome')
    accept_terms = forms.BooleanField(
        required=True, 
        label='', 
        widget=CheckboxInputWithLabel(attrs={
            'label': mark_safe(
                'Eu aceito os '
                '<a href="{% url \'terms_of_service\' %}">Termos de Serviço</a>'
                ' e a '
                '<a href="{% url \'privacy_policy\' %}">Política de Privacidade</a>'
            )
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'accept_terms']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        password1 = cleaned_data.get('password1')

        if first_name and last_name and first_name.lower() == last_name.lower():
            raise forms.ValidationError("O nome e sobrenome não podem ser iguais.")

        if password1:
            from django.contrib.auth.password_validation import validate_password
            try:
                validate_password(password1, self.instance)
            except ValidationError as e:
                self.add_error('password1', e)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['first_name'].upper()
        user.last_name = self.cleaned_data['last_name'].upper()
        if commit:
            user.save()
        return user


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
