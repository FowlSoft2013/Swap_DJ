from rest_framework import serializers

class SpotifyTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    token_type = serializers.CharField(required=True)
    expires_in = serializers.IntegerField(required=True)
    refresh_token = serializers.CharField(required=True)
    scope = serializers.CharField(required=False, allow_blank=True)
