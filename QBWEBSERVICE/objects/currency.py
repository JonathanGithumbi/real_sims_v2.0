from QBWEBSERVICE.objects.base import BaseObject
from QBWEBSERVICE.validators import SchemeValidator


class Currency(BaseObject):
    fields = dict(
        Name=dict(required=False, validator=dict(
            type=SchemeValidator.STRTYPE)),
        IsActive=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        CurrencyCode=dict(required=False, validator=dict(
            type=SchemeValidator.STRTYPE)),
        # Add Currency Format Later
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreatedTime=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSqequence=dict(validator=dict(type=SchemeValidator.ESTYPE)),
        FullName=dict(required=True, validator=dict(
            type=SchemeValidator.STRTYPE)),
    )

    def __init__(self, Name=None, IsActive=None, **kwargs):
        if Name:
            self.Name = Name

        if IsActive:
            self.IsActive = IsActive

        super().__init__(**kwargs)

    @staticmethod
    def get_service():
        from QBWEBSERVICE.services.currency import CurrencyService
        return CurrencyService
