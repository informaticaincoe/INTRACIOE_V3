from rest_framework import serializers

class AuthResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField(required=False)
    token = serializers.CharField(required=False)
    roles = serializers.ListField(child=serializers.CharField(), required=False)
    error = serializers.CharField(required=False)
    details = serializers.CharField(required=False)

