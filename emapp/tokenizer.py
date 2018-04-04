def __apnd (txt, frst, scnd, epty, start):
    idx = txt.find(frst, start) + len(frst)
    idx2 = 0
    val = epty
    if idx != -1:
        idx2 = txt.find(scnd, idx)
        if idx2 != -1:
            val = txt[idx:idx2].replace('\\r\\n', '\r\n')
            val = val.replace('\\n', '')
            val = val.strip()
        else:
            idx2 = 0
    return val, idx2


def tknzr (texto):
    tk = []
    try:
        resp, idx2 = __apnd(texto, "Alert Details", "Start Date Time", "Sin Detalles", 0)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Start Date Time", "End Date Time", "Sin fecha/hora de inicio", idx2)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "End Date Time", "Managed Object", "Sin fecha/hora de finalización", idx2)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Managed Object", "System Login", "Sin Objeto Manejado", idx2)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Category", "Rating", "Sin Categoría", idx2)
        tk.append(resp)
        resp, idx2 = __apnd(texto, "Rating", "Status", "Sin Valuación", idx2)
        tk.append(resp)
        resp, idx3 = __apnd(texto, "Status", "Measured Metrics", "Sin Estado", idx2)
        if resp.find("Alert Description") != -1:
            resp, idx2 = __apnd(texto, "Status", "Alert Description", "Sin Estado", idx2)
            tk.append(resp)
            resp, idx3 = __apnd(texto, "Description:", "Measured Metrics", "Sin Descripcion", idx2)
            if resp.find("Analysis Tools:") != -1:
                resp, idx2 = __apnd(texto, "Description:", "Analysis Tools:", "Sin Descripcion", idx2)
                tk.append(resp)
                resp, idx2 = __apnd(texto, "Analysis Tools:", "Measured Metrics", "Sin Analisis", idx2)
                tk.append(resp)
            else:
                tk.append(resp)
                tk.append("Sin Analisis")
        else:
            if resp.find("Analysis Tools:") != -1:
                tk.append("Sin Descripcion")
                resp, idx2 = __apnd(texto, "Analysis Tools:", "Measured Metrics", "Sin Descripcion", idx2)
                tk.append(resp)
            else:
                tk.append(resp)
                tk.append("Sin Descripcion")
                tk.append("Sin Analisis")

    except AttributeError:
        # AAA, ZZZ not found in the original string
        tk.append(("Exception", "Not Found"))
        # found = 'Not Found'  # apply your error handling

    return tk