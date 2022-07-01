def generate_admission_number(id):
    """Returns an admission number in the format 'k+<id>.zfill(4)'"""
    return 'k'+str(id).zfill(4)


