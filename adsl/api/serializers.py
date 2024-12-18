from dataclasses import field
from rest_framework import serializers
from adsl.models import Enlace, Internet
from system.templatetags.systemtags import encode_url
from system.models import Municipio, Trabajo

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ['municipio_name',]

class TrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajo
        fields = ['trabajo_name',]
        

class InternetSerializer(serializers.ModelSerializer):
    encodepk = serializers.SerializerMethodField()
    adsl = serializers.StringRelatedField(many=False)
    municipio = MunicipioSerializer(many=False)
    trabajo = TrabajoSerializer(many=False)
    create_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M", required=False, read_only=True)
    modify_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M", required=False, read_only=True)
    fecha_autorizo = serializers.DateField(format="%d/%m/%Y", required=False, read_only=True)
    vencimiento = serializers.DateField(format="%d/%m/%Y", required=False, read_only=True)
    class Meta:
        model = Internet
        fields = ['encodepk', 'adsl', 'municipio', 'trabajo', 'fecha_autorizo', 'cuota', 'ip', 'create_date', 'modify_date', 'alerta_vencimiento', 'vencimiento']
    
    def get_encodepk(self, object):
        encode_pk = encode_url(object.adsl.pk)
        return encode_pk


class EnlaceSerializer(serializers.ModelSerializer):
    encodepk = serializers.SerializerMethodField()
    municipio = MunicipioSerializer(many=False)
    trabajo = TrabajoSerializer(many=False)
    InternetAdsl= InternetSerializer(many=False, read_only=True)
    create_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M", required=False, read_only=True)
    modify_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M", required=False, read_only=True)
    tipo_conexion_display = serializers.CharField(
        source='get_tipo_conexion_display'
    )
    
    
    class Meta:
        model = Enlace
        fields = "__all__"
    
    def get_encodepk(self, object):
        encode_pk = encode_url(object.pk)
        return encode_pk