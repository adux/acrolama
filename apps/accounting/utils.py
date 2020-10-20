def finalize_referenz(referenzstr):
    """
    Calculates the checksum according to Luhn Algorithm but recursiv

    Also know as the modulo 10 rekursiv algorithm.
    It is used by swiss postfinance for cacluating checksums for example in ESR


    @see https://www.postfinance.ch/content/dam/pfch/doc/cust/download/efin_recdescr_man_de.pdf
    @see https://en.wikipedia.org/wiki/Luhn_algorithm
    @see http://www.hosang.ch/modulo10.aspx
    """

    check_sum = 0

    check_offset = len(referenzstr) % 2

    for i, n in enumerate(referenzstr):
        if (i + check_offset) % 2 == 0:
            n_ = n * 2
            check_sum += int(n_) - 9 if int(n_) > 9 else int(n_)
        else:
            check_sum += int(n)
            finalized_referenz = referenzstr + str(10 - (check_sum % 10))

            return " ".join(finalized_referenz[i: i + 5] for i in range(0, len(finalized_referenz), 5))
