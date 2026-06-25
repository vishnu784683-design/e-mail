from rest_framework import serializers

from .models import EmailReply


class EmailReplySerializer(serializers.ModelSerializer):

    class Meta:

        model = EmailReply

        fields = '__all__'

        read_only_fields = [
            'user',
            'created_at',
        ]