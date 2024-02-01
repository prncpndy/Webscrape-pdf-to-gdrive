import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import os
SCOPES = ["https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive.metadata.readonly",]
# Authenticate with Google Drive
flow = InstalledAppFlow.from_client_secrets_file('credential.json', SCOPES)
credentials = flow.run_local_server(port=0)
service = build('drive', 'v3', credentials=credentials)

# Set the webpage URL and Google Drive folder ID
url = 'WEBSITE_HOSTING_THE_PDF'  # Replace with the actual URL
folder_id = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'  # Replace with your folder ID

# Get the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all PDF links and extract link names
pdf_links = []
for link in soup.find_all('a', href=True):
    if link['href'].endswith('.pdf'):
        filename = link.text.strip()  # Extract link text as filename
        pdf_links.append((link['href'], filename))

# Download and upload each PDF to Google Drive
for link, filename in pdf_links:
    with requests.get(link, stream=True) as r:
        r.raise_for_status()  # Raise an exception for bad status codes

        with open("temp_pdf.pdf", "wb") as f:  # Create a temporary file
            f.write(r.content)

            file_metadata = {
        'name': filename + '.pdf',
        'parents': [folder_id]
    }

            file = service.files().create(body=file_metadata,      media_body="temp_pdf.pdf", fields='id').execute()
            print(f'PDF "{filename}" uploaded to Google Drive with ID: {file.get("id")}')