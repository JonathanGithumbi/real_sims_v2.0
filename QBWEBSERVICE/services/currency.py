from QBWEBSERVICE import QUICKBOOKS_ENUMS
from QBWEBSERVICE.services.base import Service


class CurrencyService(Service):
    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_CURRENCY, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_CURRENCY, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_CURRENCY)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_CURRENCY, id)
