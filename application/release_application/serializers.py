from rest_framework import  serializers
from .models import ReleaseApplication

class ReleaseApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseApplication
        fields = '__all__'
