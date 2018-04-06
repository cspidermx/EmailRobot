import os
# file_path = os.path.join('C:\\Users\\Charly\\Desktop\\SapMails', cliente, str(idmail) + ".html")
# with open(file_path, 'wb') as f:
#     f.write(get_body(raw))


def storedata(emldta, tokens, i):
    dsktop = 'C:\\Users\\Charly\\Desktop\\SapMails'
    file_path = os.path.join(dsktop, "emails.txt")
    if not os.path.isfile(file_path):
        mode = 'wb'
    else:
        mode = 'ab'
    with open(file_path, mode) as f:
        if mode == 'wb':
            f.write('ID|To|From|Subject|Date|Cliente|MsgID'.encode('utf-8') + b'\r\n')
        f.write((str(i) + '|').encode('utf-8') + '|'.join(map(str, emldta)).encode('utf-8') + b'\r\n')
    file_path = os.path.join(dsktop, "data.txt")
    if not os.path.isfile(file_path):
        mode = 'wb'
    else:
        mode = 'ab'
    with open(file_path, mode) as f:
        if mode == 'wb':
            f.write('ID|Alert Details|Start Date Time|End Date Time|Managed Object|Category|Rating|Status|Description|Analysis Tools'.encode('utf-8') + b'\r\n')
        f.write((str(i) + '|').encode('utf-8') + '|'.join(map(str, tokens)).encode('utf-8') + b'\r\n')