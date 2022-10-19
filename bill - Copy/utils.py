def generate_bill_number(id):
    """Returns a bill number in the format 'B+<id>.zfill(4)'"""
    return 'B'+str(id).zfill(4)


