from django.forms import ModelForm
from .models import Users

class UsersRadiusForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsersRadiusForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nombre"
        self.fields['name'].widget.attrs={'class': 'form-control', 'placeholder': 'Nombre y apellidos', 'required': '', 'autofocus': ''}
        self.fields['email'].label = "Email"
        self.fields['email'].widget.attrs={'class': 'form-control', 'placeholder': 'Usuario de conexion', 'required': ''}
        self.fields['description'].label = "Descripción"
        self.fields['description'].widget.attrs={'class': 'form-control', 'placeholder': 'Descripción', 'required': ''}
        self.fields['group'].label = "Grupo de Conexión"
        self.fields['group'].widget.attrs = {'class': 'form-select select2', 'required': ''}

    class Meta:
        model = Users
        fields = '__all__'