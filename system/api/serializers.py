from rest_framework import serializers
from django.contrib.auth.models import User
from system.models import Logs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',]

class LogsSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=False)
    access_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M", required=False, read_only=True)
    msg_type_display = serializers.CharField(
        source='get_msg_type_display'
    )
    class Meta:
        model = Logs
        fields = "__all__"