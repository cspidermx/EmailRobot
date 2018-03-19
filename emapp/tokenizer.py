def __apnd (txt, frst, scnd, epty, start, plus, minus):
    idx = txt.find(frst, start) + plus
    idx2 = 0
    val = epty
    if idx != -1:
        idx2 = txt.find(scnd, idx) - minus
        if idx2 != -1:
            val = txt[idx:idx2].replace('\\r\\n', '\r\n')
        else:
            idx2 = 0
    return val, idx2


def tknzr (texto):
    tk = []
    try:
        resp, idx2 = __apnd(texto, ".gif", "*", "Sin Detalles", 0, 5, 1)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Start Date Time", "/", "Sin fecha/hora de inicio", idx2, 21, 1)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "End Date Time", "/", "Sin fecha/hora de finalización", idx2, 19, 1)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Managed Object", "/", "Sin Objeto Manejado", idx2, 20, 1)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Category", "/", "Sin Categoría", idx2, 14, 1)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Rating", "/", "Sin Valuación", idx2, 12, 1)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Status", "/", "Sin Estado", idx2, 12, 1)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Description:", "Analysis Tools:", "Sin Descripción", idx2, 21, 8)
        tk.append(resp)

    except AttributeError:
        # AAA, ZZZ not found in the original string
        tk.append(("Exception", "Not Found"))
        # found = 'Not Found'  # apply your error handling

    return tk