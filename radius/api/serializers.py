from rest_framework import serializers
from radius.models import Users, Group
from system.templatetags.systemtags import encode_url

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['group_name',]

class UsersSerializer(serializers.ModelSerializer):
    encodepk = serializers.SerializerMethodField()
    group = GroupSerializer(many=False)
    create_date = serializers.DateField(format="%d/%m/%Y", required=False, read_only=True)
    modify_date = serializers.DateField(format="%d/%m/%Y", required=False, read_only=True)
    
    class Meta:
        model = Users
        fields = "__all__"
    
    def get_encodepk(self, object):
        encode_pk = encode_url(object.pk)
        return encode_pk