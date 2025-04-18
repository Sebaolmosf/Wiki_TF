from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password

class RegistroUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control border-0'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control border-0'}),
        label="Confirmar contraseña"
    )

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control border-0'})
    )

    class Meta:
        model = Usuario
        fields = ['email'] 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password1")
        pass2 = cleaned_data.get("password2")

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
