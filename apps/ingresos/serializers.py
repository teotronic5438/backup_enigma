
from rest_framework import serializers
from .models import Remitos

class RemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remitos
        fields = '__all__'
