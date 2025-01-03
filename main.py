from downloadFileFromSharePoint import *
from importContacts import *

download_status = DownloadFileFromSharePoint()

if download_status == 200:
    import_status = ImportContacts()
    if import_status == 200:
        print("Contacts imported successfully")
    elif import_status == 0:
        print("No data to import")
    else:
        print("Failed to import contacts")