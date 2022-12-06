
class FeesStructureManager():
    def create_feesstructure(self, create_feesstructure_form):
        fees_obj = create_feesstructure_form.save()
        return fees_obj

    def delete_feesstructure(self, feesstructure):
        feesstructure.delete()
        return True
