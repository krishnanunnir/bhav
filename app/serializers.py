from rest_framework import serializers

class EquitySerializer(serializers.Serializer):
    code = serializers.CharField(max_length= 6)
    name = serializers.CharField(max_length= 26)
    # Storing as Integer for future usage
    open_value = serializers.IntegerField()
    high_value = serializers.IntegerField()
    low_value = serializers.IntegerField()
    close_value = serializers.IntegerField()