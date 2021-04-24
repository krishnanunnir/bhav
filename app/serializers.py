from rest_framework import serializers

class EquitySerializer(serializers.Serializer):
    code = serializers.CharField(max_length= 6)
    name = serializers.CharField(max_length= 26)
    # Storing as Integer for future usage
    open_value = serializers.FloatField()
    high_value = serializers.FloatField()
    low_value = serializers.FloatField()
    close_value = serializers.FloatField()