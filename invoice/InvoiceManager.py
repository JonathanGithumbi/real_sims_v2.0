from invoice.models import Invoice, BalanceTable
from invoice.models import Item as InvoiceItem
from fees_structure.models import BillingItem
from item.ItemManager import ItemManager


class InvoiceManager():
    """This invoice manager is in charge of invoicing one student at registration and all active students at the beginning of the term"""

    

    def get_latest_invoice(self, student):
        latest_invoice = Invoice.objects.filter(student=student).latest()
        return latest_invoice

    def invoice_new_student(self, student):
        """this method is called by student model's post_save function after registration"""

        # Step 1 build the invoice

        invoice = Invoice.objects.create(
            student=student,
            year=student.year_admitted,
            term=student.term_admitted,
            grade=student.grade_admitted_to,

        )

        # Get items to charge assuming that the user checked the charge_on_registration input
        items_charged_at_registration = BillingItem.objects.filter(
            charge_on_registration=True, grades__in=[student.grade_admitted_to])

        # add those items to the invoice
        for bill in items_charged_at_registration:

            InvoiceItem.objects.create(
                billing_item=bill,
                invoice=invoice
            )

        # return the charge
        return invoice

    def invoice_continuing_student(self, student):
        """This method charges a student at the start of every term"""
        # Step 1 build the invoice
        invoice = Invoice.objects.create(
            student=student,
            year=student.current_year,
            term=student.current_term,
            grade=student.current_grade,

        )
        # the items that are charged on a termly basis are either those that recurr yearly throught the year, those that recurr at
        # the current specific term, and those one time charges that happen to fall on this particular term and year

        # get items that recurr yearly and also fall into this term
        from academic_calendar.CalendarManager import CalendarManager
        cal_man = CalendarManager()
        curr_term = cal_man.get_term()
        curr_year = cal_man.get_year

        rec_yr_thr = BillingItem.objects.filter(
            grades__in=[student.current_grade], ocurrence='recurring', terms__in=[curr_term.term])
        if rec_yr_thr:
            # add those items to the invoice
            for fees_structure in rec_yr_thr:
                InvoiceItem.objects.create(
                    billing_item=fees_structure,
                    invoice=invoice
                )

        # get items that recurr yearly at specific terms
        # rec_yr_spc = BillingItem.objects.filter(
        #    grades__in=[student.current_grade], ocurrence='recurring', period='specific-terms', terms__in=[student.current_term])
        # if rec_yr_spc:
        #    # add those items to the invoice
        #    for fees_structure in rec_yr_spc:
        #        InvoiceItem.objets.create(
        #            sales_item=fees_structure.item,
        #            amount=fees_structure.amount,
        #            invoice=invoice
        #        )
        # else:
        #    pass

        # get onetime items if any
        #one_timers = BillingItem.objects.filter(
        #    grades__in=[student.current_grade], ocurrence='one-time', term=student.current_term.term, year=student.current_year)
        #if one_timers:
        #    # add those items to the invoice
        #    for fees_structure in one_timers:
        #        InvoiceItem.objects.create(
        #            billing_item=fees_structure,
        #            invoice=invoice
        #        )
        #else:
        #    pass
        ## return teh charge
        return invoice

    def invoice_student_lunch(self, student):
        """This method invoices a student for lunch"""

        # Get the current term's invoice
        curr_invoice = Invoice.objects.get(
            student=student, year=student.current_year, term=student.current_term)

        # Create an invoice item for the lunch item
        item_manager = ItemManager()
        lunch_sales_item = item_manager.get_lunch_item()
        lunch_item_amount = BillingItem.objects.get(
            item=lunch_sales_item, grades__in=[student.current_grade]).amount
        lunch_item = InvoiceItem.objects.create(
            sales_item=lunch_sales_item,
            amount=lunch_item_amount,
            invoice=curr_invoice
        )
        # set the invoice balance
        curr_invoice.balance = curr_invoice.get_total_amount()
        curr_invoice.save(update_fields=['balance'])
        # Increase the balance record
        bal_record = BalanceTable.objects.get(student=student)
        bal_record.increase_balance(lunch_item_amount)

        return lunch_item

    def uninvoice_student_lunch(self, student):
        """This method uninvoices a student from lunch"""
        # Get the current term's invoice
        curr_invoice = Invoice.objects.get(
            student=student, year=student.current_year, term=student.current_term)

        # get the lunch sales item
        item_manager = ItemManager()
        lunch_sales_item = item_manager.get_lunch_item()
        # find and delete the lunch invoice item
        lunch_item = InvoiceItem.objects.get(
            invoice=curr_invoice, sales_item=lunch_sales_item)
        lunch_item.delete()
        # set the invoice balance
        curr_invoice.balance = curr_invoice.get_total_amount()
        curr_invoice.save(update_fields=['balance'])
        # decrease the student's balance
        bal_record = BalanceTable.objects.get(student=student)
        bal_record.decrease_balance(lunch_item.amount)
        return True

    def invoice_student_transport(self, student):
        """This method invoices a student for transport"""
        # Get the current term's invoice
        curr_invoice = Invoice.objects.get(
            student=student, year=student.current_year, term=student.current_term)

        # Create an invoice item for the transport item
        item_manager = ItemManager()
        transport_sales_item = item_manager.get_transport_item()
        transport_item_amount = BillingItem.objects.get(
            item=transport_sales_item, grades__in=[student.current_grade]).amount
        transport_item = InvoiceItem.objects.create(
            sales_item=transport_sales_item,
            amount=transport_item_amount,
            invoice=curr_invoice
        )
        # set the invoice balance
        curr_invoice.balance = curr_invoice.get_total_amount()
        curr_invoice.save(update_fields=['balance'])
        # Increase the balance record
        bal_record = BalanceTable.objects.get(student=student)
        bal_record.increase_balance(transport_item_amount)

        return transport_item

    def uninvoice_student_transport(self, student):
        """This method uninvoices a student from transport"""
        # Get the current term's invoice
        curr_invoice = Invoice.objects.get(
            student=student, year=student.current_year, term=student.current_term)

        # get the transport sales item
        item_manager = ItemManager()
        transport_sales_item = item_manager.get_transport_item()
        # find and delete the transport invoice item
        transport_item = InvoiceItem.objects.get(
            invoice=curr_invoice, sales_item=transport_sales_item)
        transport_item.delete()
        # set the invoice balance
        curr_invoice.balance = curr_invoice.get_total_amount()
        curr_invoice.save(update_fields=['balance'])
        # decrease the student's balance
        bal_record = BalanceTable.objects.get(student=student)
        bal_record.decrease_balance(transport_item.amount)
        return True

    def receive_payment(self, amount, invoice):
        invoice.balance = invoice.balance - amount
        invoice.save(update_fields=['balance'])
        return True
