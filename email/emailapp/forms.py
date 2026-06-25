from django import forms
from .models import EmailReply

class EmailReplyForm(forms.ModelForm):

    class Meta:
        model = EmailReply

        fields = [
            'received_email',
            'tone',
            'generated_reply'
        ]