from django.forms import ModelForm
from .models import *


class EnlacesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnlacesForm, self).__init__(*args, **kwargs)
        self.fields['alias'].label = "Alias del enlace"
        self.fields['alias'].widget.attrs = {'class': 'form-control', 'required': '', 'autofocus': ''}
        self.fields['ipwan'].label = "IP WAN"
        self.fields['ipwan'].widget.attrs = {'class': 'form-control'}
        self.fields['ipwan_netmask'].label = "Mascara"
        self.fields['ipwan_netmask'].widget.attrs = {'class': 'form-select select2'}
        self.fields['iplan'].label = "IP LAN"
        self.fields['iplan'].widget.attrs = {'class': 'form-control'}
        self.fields['iplan_netmask'].label = "Mascara"
        self.fields['iplan_netmask'].widget.attrs = {'class': 'form-select select2'}
        self.fields['ed'].label = "ED"
        self.fields['ed'].widget.attrs = {'class': 'form-control'}
        self.fields['ab'].label = "AB"
        self.fields['ab'].widget.attrs = {'class': 'form-control'}
        self.fields['um_ab'].label = "UM"
        self.fields['um_ab'].widget.attrs = {'class': 'form-select select2'}
        self.fields['tipo_conexion'].label = "Conexión"
        self.fields['tipo_conexion'].widget.attrs = {'class': 'form-select select2'}
        self.fields['municipio'].label = "Municipio"
        self.fields['municipio'].widget.attrs = {'class': 'form-select select2'}
        self.fields['trabajo'].label = "Institución"
        self.fields['enrutamiento'].label = "Enrutado"
        self.fields['enrutamiento'].widget.attrs = {'class': 'form-check-input'}

    class Meta:
        model = Enlace
        fields = '__all__'


class TrasladarEnlaceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrasladarEnlaceForm, self).__init__(*args, **kwargs)
        self.fields['trabajo'].label = "Institución"
        self.fields['trabajo'].widget.attrs = {'class': 'form-select select2'}
        self.fields['municipio'].label = "Municipio"
        self.fields['municipio'].widget.attrs = {'class': 'form-select select2'}
        self.fields['alias'].label = "Alias del enlace"
        self.fields['alias'].widget.attrs = {'class': 'form-control', 'required': '', 'autofocus': ''}

    class Meta:
        model = Enlace
        fields = ['trabajo', 'municipio', 'alias']


class CambioIPForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CambioIPForm, self).__init__(*args, **kwargs)
        self.fields['iplan'].label = "Bloque IP LAN"
        self.fields['iplan'].widget.attrs = {'class': 'form-control'}
        self.fields['iplan_netmask'].label = "Mascara"
        self.fields['iplan_netmask'].widget.attrs = {'class': 'form-select'}

    class Meta:
        model = Enlace
        fields = ['iplan', 'iplan_netmask']


class CambioABForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CambioABForm, self).__init__(*args, **kwargs)
        self.fields['ab'].label = "AB"
        self.fields['ab'].widget.attrs = {'class': 'form-control'}
        self.fields['um_ab'].label = "UM"
        self.fields['um_ab'].widget.attrs = {'class': 'form-select'}

    class Meta:
        model = Enlace
        fields = ['ab', 'um_ab']


class CambioTecForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CambioTecForm, self).__init__(*args, **kwargs)
        self.fields['tipo_conexion'].label = "Tecnología"
        self.fields['tipo_conexion'].widget.attrs = {'class': 'form-select'}

    class Meta:
        model = Enlace
        fields = ['tipo_conexion']


class CambioIpInternetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CambioIpInternetForm, self).__init__(*args, **kwargs)
        self.fields['ip'].label = "IP con Internet"
        self.fields['ip'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = Internet
        fields = ['ip']


class AsignarInternetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AsignarInternetForm, self).__init__(*args, **kwargs)
        self.fields['fecha_autorizo'].label = "Fecha de autorizo"
        self.fields['fecha_autorizo'].widget.attrs = {'class': 'form-control'}
        self.fields['cuota'].label = "Cuota Internet (MB)"
        self.fields['cuota'].widget.attrs = {'class': 'form-control'}
        self.fields['ip'].label = "IP con Internet"
        self.fields['ip'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = Internet
        fields = ['ip', 'fecha_autorizo', 'cuota']

class UpdateInternetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateInternetForm, self).__init__(*args, **kwargs)
        self.fields['fecha_autorizo'].label = "Fecha de autorizo"
        self.fields['fecha_autorizo'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = Internet
        fields = ['fecha_autorizo']