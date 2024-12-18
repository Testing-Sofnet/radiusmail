from rest_framework import serializers
from usuarios.models import Users, Services, Ocupacion
from system.models import Municipio, Trabajo, Logs
from system.templatetags.systemtags import encode_url

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ['municipio_name',]

class TrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajo
        fields = ['trabajo_name',]

class OcupacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocupacion
        fields = ['ocupacion_name',]

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['service',]

class UsuarioSerializer(serializers.ModelSerializer):
    encodepk = serializers.SerializerMethodField()
    municipio = MunicipioSerializer(many=False)
    trabajo = TrabajoSerializer(many=False)
    ocupacion = OcupacionSerializer(many=False)
    sldservice = ServiceSerializer(read_only=True, many=True)
    class Meta:
        model = Users
        fields = "__all__"
    
    def get_encodepk(self, object):
        encode_pk = encode_url(object.pk)
        return encode_pk