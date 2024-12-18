from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Users, Services, Device



class UsersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = "Nombre"
        self.fields['nombre'].widget.attrs = {'class': 'form-control', 'autofocus': ''}
        self.fields['apellidos'].label = "Apellidos"
        self.fields['apellidos'].widget.attrs = {'class': 'form-control'}
        self.fields['ci'].label = "Carné de Identidad"
        self.fields['ci'].widget.attrs = {'class': 'form-control'}
        self.fields['address'].label = "Dirección"
        self.fields['address'].widget.attrs = {'class': 'form-control'}
        self.fields['quota'].label = "Cuota de Correo (Mb)"
        self.fields['quota'].widget.attrs={'class':'form-control','placeholder':'En MB'}
        self.fields['telefono'].label = "Telefono personal"
        self.fields['telefono'].widget.attrs={'class':'form-control'}
        self.fields['telefono_work'].label = "Telefono de trabajo"
        self.fields['telefono_work'].widget.attrs={'class':'form-control'}
        self.fields['tipo_cuenta'].label = "Tipo de Cuenta"
        self.fields['tipo_cuenta'].widget.attrs={'class':'form-select select2'}
        self.fields['email'].label = "Usuario"
        self.fields['email'].widget.attrs = {'class': 'form-control'}
        self.fields['trabajo'].label = "Institución"
        self.fields['trabajo'].widget.attrs = {'class': 'form-select select2'}
        self.fields['municipio'].label = "Municipio"
        self.fields['municipio'].widget.attrs = {'class': 'form-select select2'}
        self.fields['ocupacion'].label = "Ocupación"
        self.fields['ocupacion'].widget.attrs = {'class': 'form-select select2'}
        self.fields['notas'].label = "Notas"
        self.fields['notas'].widget.attrs={'class':'form-control'}
        

    class Meta:
        model = Users
        #fields = '__all__'
        exclude = ['active']


class TrasladarForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrasladarForm, self).__init__(*args, **kwargs)
        self.fields['trabajo'].label = "Institución"
        self.fields['trabajo'].widget.attrs = {'class': 'form-select select2'}
        self.fields['municipio'].label = "Municipio"
        self.fields['municipio'].widget.attrs = {'class': 'form-select select2'}

    class Meta:
        model = Users
        fields = ['trabajo', 'municipio']


class DatosPersonalesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DatosPersonalesForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = "Nombre"
        self.fields['nombre'].widget.attrs = {'class': 'form-control', 'autofocus': ''}
        self.fields['apellidos'].label = "Apellidos"
        self.fields['apellidos'].widget.attrs = {'class': 'form-control'}
        self.fields['ci'].label = "Carné de Identidad"
        self.fields['ci'].widget.attrs = {'class': 'form-control'}
        self.fields['address'].label = "Dirección"
        self.fields['address'].widget.attrs = {'class': 'form-control'}
        self.fields['telefono'].label = "Telefono personal"
        self.fields['telefono'].widget.attrs={'class':'form-control'}
        self.fields['telefono_work'].label = "Telefono de trabajo"
        self.fields['telefono_work'].widget.attrs={'class':'form-control'}
        self.fields['ocupacion'].label = "Ocupación"
        self.fields['ocupacion'].widget.attrs = {'class': 'form-select'}
        self.fields['notas'].label = "Notas"
        self.fields['notas'].widget.attrs={'class':'form-control'}

    class Meta:
        model = Users
        fields = ['nombre', 'apellidos', 'ci', 'address', 'telefono', 'telefono_work', 'ocupacion', 'notas']


class ServiceForm(ModelForm):  
        sldservice = ModelMultipleChoiceField(
            queryset=Services.objects.all(),
            widget=CheckboxSelectMultiple,
            required=True)

        class Meta: 
                model = Users 
                fields = ['sldservice']


class DatosMailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DatosMailForm, self).__init__(*args, **kwargs)
        self.fields['tipo_cuenta'].label = "Tipo de Cuenta"
        self.fields['tipo_cuenta'].widget.attrs={'class':'form-select'}
        self.fields['quota'].label = "Cuota de Correo (Mb)"
        self.fields['quota'].widget.attrs={'class':'form-control','placeholder':'En MB'}

    class Meta:
        model = Users
        fields = ['tipo_cuenta', 'quota']


class DeviceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['model'].label = "Modelo"
        self.fields['model'].widget.attrs = {'class': 'form-control', 'placeholder': 'Modelo del Dispositivo', 'required': '', 'autofocus': ''}
        self.fields['marca'].label = "Marca"
        self.fields['marca'].widget.attrs = {'class': 'form-control', 'placeholder': 'Marca del Dispositivo'}
        self.fields['type_device'].label = "Tipo"
        self.fields['type_device'].widget.attrs = {'class': 'form-select'}
        self.fields['mac_address'].label = "Dirección Mac"
        self.fields['mac_address'].widget.attrs = {'class': 'form-control'}
        self.fields['os'].label = "Sistema Operativo"
        self.fields['os'].widget.attrs = {'class': 'form-select'}

    class Meta:
        model = Device
        fields = '__all__'