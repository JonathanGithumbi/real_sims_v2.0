"""
This module is a mapping of all relevant fields to and from the QBXML format
This particular class maps to account
"""
from QBWEBSERVICE.objects.base import BaseObject
from QBWEBSERVICE.validators import SchemeValidator


class Account(BaseObject):
    """The fields added here can be user for query, mod and create as needed"""
    fields = dict(
        Name=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        IsActive=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        AccountType=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Currency=dict(many=True, validator=dict(type=SchemeValidator.OBJTYPE)),

    )

    @staticmethod
    def get_service():
        from QBWEBSERVICE.services.account import AccountService
        return AccountService

class Currency(BaseObject):
    fields = dict(
        
    )