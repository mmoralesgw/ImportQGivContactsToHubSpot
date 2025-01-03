import os
import requests
from readConfigFile import *

# Azure AD app registration credentials
client_id = GetClientId()
client_secret = GetClientSecret()
tenant_id = GetTenantId()

# SharePoint Online site and library information
site_id = ""
drive_id = ''
access_token = ""

# Authenticate and get an access token
auth_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
}
response = requests.post(auth_url, data=data)
access_token = response.json()['access_token']


# Get the SharePoint site id using the Microsoft Graph API
def GetSiteId():
    get_site_url = 'https://graph.microsoft.com/v1.0/sites/root:/sites/HubSpotSite/'
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(get_site_url, headers=headers)
    if response.status_code == 200:
        global site_id
        site_id = response.json()['id']
    else:
        print(f"Request failed with status code: {response.status_code}")


# Get the SharePoint drive id using the Microsoft Graph API
def GetDriveId():
    get_drive_id_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(get_drive_id_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        global drive_id
        drive_id = data['value'][1]['id']
    else:
        print(f"Request failed with status code: {response.status_code}")


# Download a file from the SharePoint document library using the Microsoft Graph API
def DownloadFileFromSharePoint():
    GetSiteId()
    GetDriveId()

    file_name = 'qGivDonorsDataReport.csv'  # File name to download
    folder_name = 'QGivDonorsData'  # Folder where the file is located
    download_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{folder_name}/{file_name}:/content'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Send GET request to download the file
    response = requests.get(download_url, headers=headers)
    status = 0
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"File {file_name} downloaded successfully")
        status = 200
    else:
        status = 500
        print(f"Failed to download file: {response.status_code}")
        
    return status

