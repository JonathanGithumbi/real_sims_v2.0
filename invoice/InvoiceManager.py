from invoice.models import Invoice,Item,BalanceTable
from fees_structure.models import FeesStructureBatch

class InvoiceManager():
    """This invoice manager is in charge of invoicing one student at registration and all active students at the beginning of the term"""

    def invoice_new_student(self, student):
        """This method is applied during registration"""
        """To charge a student you must have an instance of a student and an instance of an invoice"""
        """An invoice is charged for a specific year and a specific term, against a number of items"""
        # Step 1 build the invoice

        invoice = Invoice.objects.create(
            student=student,
            year=student.year_admitted,
            term=student.term_admitted,
            grade=student.grade_admitted_to,

        )

        # Get items to charge assuming that the user checked the charge_on_registration input
        items_charged_at_registration = FeesStructureBatch.objects.filter(
            charge_on_registration=True, grades__in=[student.grade_admitted_to])
        # add those items to the invoice
        for fees_structure in items_charged_at_registration:
            Item.objects.create(
                sales_item=fees_structure.item,
                amount=fees_structure.amount,
                invoice=invoice
            )

        # create and update the balancetable
        bal_record = BalanceTable.objects.create(student=invoice.student)
        bal_record.increase_balance(invoice.get_total_amount())
        # return the charge
        return invoice

    def invoice_continuing_student(self, student):
        """This method charges a student at the start of every term"""
        # Step 1 build the invoice
        invoice = Invoice.objects.create(
            student=student,
            year=student.current_year,
            term=student.current_term,
            grade=student.grade_admitted_to,

        )
        # the items that are charged on a termly basis are either those that recurr yearly throught the year, those that recurr at
        # the current specific term, and those one time charges that happen to fall on this particular term and year

        # get items that recurr yearly throughout all the terms
        rec_yr_thr = FeesStructureBatch.objects.filter(
            grades__in=[student.current_grade], ocurrence='recurring', period='year-round')
        if rec_yr_thr:
            # add those items to the invoice
            for fees_structure in rec_yr_thr:
                Item.objets.create(
                    sales_item=fees_structure.item,
                    amount=fees_structure.amount,
                    invoice=invoice
                )

        # get items that recurr yearly at specific terms
        rec_yr_spc = FeesStructureBatch.objects.filter(
            grades__in=[student.current_grade], ocurrence='recurring', period='specific-terms', terms__in=[student.current_term])
        if rec_yr_spc:
            # add those items to the invoice
            for fees_structure in rec_yr_spc:
                Item.objets.create(
                    sales_item=fees_structure.item,
                    amount=fees_structure.amount,
                    invoice=invoice
                )
        else:
            pass

        # get onetime items if any
        one_time = FeesStructureBatch.objects.filter(
            grades__in=[student.current_grade], ocurrence='one-time', term=student.current_term, year=student.current_year)
        if one_time:
            # add those items to the invoice
            for fees_structure in rec_yr_spc:
                Item.objets.create(
                    sales_item=fees_structure.item,
                    amount=fees_structure.amount,
                    invoice=invoice
                )
        else:
            pass

        # update the balancetable
        bal_record = BalanceTable.objects.get(student=invoice.student)
        bal_record.increase_balance(invoice.get_total_amount())

        # return teh charge
        return invoice
