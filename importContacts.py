import requests
import json
import os
import csv

url = "https://api.hubapi.com/crm/v3/imports"

YOUR_ACCESS_TOKEN = 'pat-na1-2c184c47-a115-4095-9cdf-38b2b52f0d78'

# Content-Type header will be set automatically by the requests library
headers = {
  'authorization': 'Bearer %s' % YOUR_ACCESS_TOKEN
}

data = {
  "name": "Daily contacts import from QGiv",
  "importOperations": {
    "0-1": "CREATE"
  },
  "dateFormat": "DAY_MONTH_YEAR",
  "files": [
    {
      "fileName": "qGivDonorsDataReport.csv",
      "fileFormat": "CSV",
      "fileImportPage": {
        "hasHeader": True,
        "columnMappings": [
          {
            "columnObjectTypeId": "0-1",
            "columnName": "firstName",
            "propertyName": "firstname"
          },
          {
            "columnObjectTypeId": "0-1",
            "columnName": "lastName",
            "propertyName": "lastname"
          },
          {
            "columnObjectTypeId": "0-1",
            "columnName": "contactEmail",
            "propertyName": "email",
            "columnType": "HUBSPOT_ALTERNATE_ID"
          },
           {
            "columnObjectTypeId": "0-1",
            "columnName": "phone",
            "propertyName": "phone"  
          },
          {
            "columnObjectTypeId": "0-1",
            "columnName": "dataSource",
            "propertyName": "datasourcename"
          }
        ]
      }
    }
  ]
}

def file_has_data(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        # Skip the header row
        headers = next(reader, None)
        # Check if there's any additional row after the header
        for row in reader:
            if any(cell.strip() for cell in row):  # Ensure it's not an empty row
                return True
        return False


def ImportContacts():
    
    response_code = 0
    datastring = json.dumps(data)

    payload = {"importRequest": datastring}

    file_path = "qGivDonorsDataReport.csv"

    files = [
        ('files', open(file_path, 'rb'))
    ]
    if file_has_data(file_path):
        response = requests.request("POST", url, data=payload, files=files, headers=headers)
        response_code = response.status_code

    return response_code


#url = "https://api.hubapi.com/crm/v3/properties/contacts" # This is the endpoint to get all the properties of a contact
#response = requests.request("GET",url, headers=headers)

