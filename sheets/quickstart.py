from cgitb import reset
import imp
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive"]

def get_credentials_as_dict(credentials) -> dict:
    credentials_as_dict = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "id_token": credentials.id_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes

    }
    return credentials_as_dict

def credentials_from_dict(credentials_dict: dict) -> Credentials:
    
    creds= Credentials(
        credentials_dict["token"],
        refresh_token=credentials_dict["refresh_token"],
        token_uri=credentials_dict["token_uri"],
        client_id=credentials_dict["client_id"],
        client_secret=credentials_dict["client_secret"],
        scopes=credentials_dict["scopes"]
    )
    return creds

def get_credentials() -> Credentials:

    # file token json stores users access and refresh token and created automatic when author flow complets for the first time
    creds = None
    token_fileName = "token.json"

    if os.path.exists(token_fileName):
        with open(token_fileName, "r") as f:
            credentials_as_dict = json.loads(f)
            creds = credentials_from_dict(credentials_as_dict)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials_4.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # save the credentials for next run
        with open(token_fileName, "w") as f:
            f.write(creds.to_json())
    
    return creds

def list_files(service: None):
    # list file drive

    # call drive api v3
    results = (
        service.files().list( q= "mimeType='application/vnd.google-apps.spreadsheet'", fields="nextPageToken, files(id, name)").execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found")
    else:
        print("Files : ")
        for item in items:
            print(f'{item["name"]} ({item["id"]})')

def main():
    credentials = get_credentials()
    drive_service = build("drive", "v3", credentials=credentials)
    list_files(service=drive_service)

if __name__ == "__main__":
    main()
