from django.core.validators import MinValueValidator
from rest_framework import serializers
from helpers.serialization_errors import error_dict
from .models import Payment


class PaymentSentSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Payment objects."""
    mobile_no = serializers.RegexField(
        regex='^(?:\B\+ ?254|\b0)(?: *[(-]? *\d(?:[ \d]*\d)?)? *(?:[)-] *)?\d+ *(?:[/)-] *)?\d+ *(?:[/)-] *)?\d+(?: *- *\d+)?',
        allow_null=False,
        required=True,
        min_length=10,
        max_length=15,
        error_messages={
            'required': error_dict['required'],
            'min_length': error_dict['min_length'].format("Phone number", "10"),
            'max_length': error_dict['max_length'].format("Phone number", "15"),
            'invalid': error_dict['invalid_phone_no']
        }
    )
    amount = serializers.IntegerField(required=True,
                                      allow_null=False,
                                      validators=[
                                          MinValueValidator(1, 'Amount cannot be zero or negative')])

    class Meta:
        model = Payment
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['mobile_no', 'amount']
