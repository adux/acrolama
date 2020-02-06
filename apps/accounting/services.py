
from accounting.models import Invoice

def get_invoice(invoice):
    # If its str or int treat it as Invoice Obj
    if isinstance(invoice, (str, int)):
        invoice_pk = int(invoice)
    else:
        return invoice

    if invoice_pk:
        try:
            book = Invoice.objects.get(pk=invoice_pk)
        except:
            return

    return book
