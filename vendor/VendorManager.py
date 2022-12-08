from .models import Vendor


class VendorManager():
    def create_vendor(self, create_vendor_form):
        vendor_obj = create_vendor_form.save()
        return vendor_obj

    def delete_vendor(self, vendor):
        vendor.delete()
        return True

    def edit_vendor(self, edit_vendor_form):
        errors = edit_vendor_form.errors
        print(errors)
        edit_vendor_form.save()
        return True
