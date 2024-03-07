from collections import OrderedDict
from .users import get_user
from .date import format_date


def request_representation(instance):
    """
    single request representation
    Args:
        instance (obj): request object

    Returns:
        (OrderedDict): ordered dictionary of the request
    """
    return OrderedDict(
        id=instance.id,
        created_at=format_date(instance.created_at),
        updated_at=format_date(instance.updated_at),
        recipient=get_user(instance.recipient),
        amount=instance.amount,
        reason=instance.reason,
        status=instance.status,
        cancellation_reason=instance.cancellation_reason
    )
