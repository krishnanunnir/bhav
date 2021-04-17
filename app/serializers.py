from rest_framework import serializers
from .models import ImportDate

class ImportDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportDate
        fields = '__all__'