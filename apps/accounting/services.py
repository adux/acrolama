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
        except Exception:
            return

    return book


def check_is_book_payed(bookid):
    if Invoice.objects.get(book=bookid).status == "PY":
        return True
    else:
        return False
