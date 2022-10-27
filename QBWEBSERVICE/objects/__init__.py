from django.utils.module_loading import import_string

from QBWEBSERVICE.exceptions import QBObjectNotImplemented

ALTERNATIVES = {
    'ItemService': ('Item',),
}


def import_object_cls(resource_name):
    for class_name, alternatives in ALTERNATIVES.items():
        if resource_name in alternatives:
            resource_name = class_name

    try:
        return import_string('%s.%s' % (__package__, resource_name))
    except ImportError:
        raise QBObjectNotImplemented


from QBWEBSERVICE.objects.customer import \
    Customer

from QBWEBSERVICE.objects.address import \
    BillAddress, \
    ShipAddress

from QBWEBSERVICE.objects.invoice import \
    ItemService, \
    InvoiceLine, \
    Invoice
