from QBWEBSERVICE import QUICKBOOKS_ENUMS
from QBWEBSERVICE.objects.invoice import ItemService
from QBWEBSERVICE.processors import ResponseProcessor


class ItemServiceQueryResponseProcessor(ResponseProcessor):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    obj_class = ItemService

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False

        return True
