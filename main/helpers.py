from __future__ import print_function
import os
import json
from PyPDF2 import PdfReader,PdfWriter
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings
from django.shortcuts import get_object_or_404
from celery import shared_task
from .models import Assignment,Material
from datetime import timedelta, date
from .prompt import enrich_format_message
from messenger.llm import query_gpt
import shutil

SCOPES = {
    'drive': ['https://www.googleapis.com/auth/drive'],
    'docs':['https://www.googleapis.com/auth/documents']
}
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'


def generate_credentials_json():
    creds = {
        "installed": {
            "client_id": f"{os.getenv('client_id').strip()}",
            "project_id": f"{os.getenv('project_id').strip()}",
            "auth_uri": f"{os.getenv('auth_uri').strip()}",
            "token_uri": f"{os.getenv('token_uri').strip()}",
            "auth_provider_x509_cert_url": f"{os.getenv('auth_provider_x509_cert_url').strip()}",
            "client_secret": f"{os.getenv('client_secret').strip()}",
            "redirect_uris": ["http://localhost"]
        }
    }
    drive = {
        "token":f"{os.getenv('drive_token').strip()}",
        "refresh_token":f"{os.getenv('drive_refresh_token').strip()}",
        "token_uri":f"{os.getenv('token_uri').strip()}",
        "client_id":f"{os.getenv('client_id').strip()}",
        "client_secret":f"{os.getenv('client_secret').strip()}",
        "scopes":["https://www.googleapis.com/auth/drive"]
        # "expiry":"2023-01-23T14:43:45.007305Z"
        
    }
    docs = {
        "token":f"{os.getenv('docs_token').strip()}",
        "refresh_token":f"{os.getenv('docs_refresh_token').strip()}",
        "token_uri":f"{os.getenv('token_uri').strip()}",
        "client_id":f"{os.getenv('client_id').strip()}",
        "client_secret":f"{os.getenv('client_secret').strip()}",
        "scopes":['https://www.googleapis.com/auth/documents']
        # "expiry":"2023-01-23T14:43:45.007305Z"
        
    }
    with open("drive.json","w") as write_file:
        json.dump(drive,write_file)

    with open("docs.json","w") as write_file:
        json.dump(docs,write_file)

    with open("credentials.json", 'w') as outfile:
        json.dump(creds, outfile)
    
    if not os.path.exists('media/'):
        os.makedirs('media/')
    
    if not os.path.exists('media/downloads/'):
        os.makedirs('media/downloads/')




def get_creds(token_file,credentials_file,scopes):
    # The file token_drive.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # import pdb;pdb.set_trace()
    # generate_credentials_json()
    creds = None
    token_json = os.path.join(settings.BASE_DIR, token_file)
    credentials_json = os.path.join(settings.BASE_DIR, credentials_file)
    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(token_json, SCOPES[scopes])
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json, SCOPES[scopes])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_json, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def handle_uploaded_file(f):
    with open('media/downloads/downloaded.pdf', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(file_obj):
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = get_creds('drive.json','credentials.json','drive')
    temp_path = None
    if hasattr(file_obj,'temporary_file_path'):
        temp_path = file_obj.temporary_file_path()
    else:
        handle_uploaded_file(file_obj)
        temp_path = 'media/downloads/downloaded.pdf'
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': file_obj.name}
        
        media = MediaFileUpload(temp_path,
                                mimetype=file_obj.content_type)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


def convert_pdf_gdocs(file_path,name):
    """Upload file with conversion
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = get_creds('drive.json','credentials.json','drive')

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.document'
        }
        media = MediaFileUpload(file_path, mimetype='application/pdf',
                                resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File with ID: "{file.get("id")}" has been uploaded.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')

def get_file(file_id):
    creds = get_creds('drive.json','credentials.json','drive')
    file = None
    try:
        service = build('drive', 'v3', credentials=creds)
        # Call the Drive v3 API
        file = service.files().get(fileId=file_id).execute()
        
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')
    return file

def download_file(file_id, local_fd):
  """Download a Drive file's content to the local filesystem.

  Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    local_fd: io.Base or file object, the stream that the Drive file's
        contents will be written to.
  """
  creds = get_creds('drive.json','credentials.json','drive')
  service = build('drive', 'v3', credentials=creds)
  request = service.files().get_media(fileId=file_id)
  media_request = MediaIoBaseDownload(local_fd, request)

  while True:
    try:
      download_progress, done = media_request.next_chunk()
    except HttpError as error:
      print (f"An error occurred: {error}")
      return
    if download_progress:
      print(f"Download Progress: {int(download_progress.progress()) * 100}")
    if done:
      print ('Download Complete')
      return


@shared_task
def split_pdf(file_id,steps):
    material = get_object_or_404(Material,file=file_id)
    file_path = 'media/downloads/downloaded.pdf'
    file = open(file_path, 'wb')
    download_file(file_id,file)
    pdf = PdfReader(file_path)
    print(len(pdf.pages))
    ranges = [range(i,i+steps) for i in range(0,len(pdf.pages),steps)]
    for i,range_ in enumerate(ranges):
        pdf_writer = PdfWriter()
        for page in range_:
            text = pdf.pages[page].extract_text()
            print(text)
            pdf_writer.add_page(pdf.pages[page])

        output_filename = 'media/downloads/{}_page_{}.pdf'.format('download', i+1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
            out.close()

        assignment = Assignment()
        assignment.course_code = material.course_code
        assignment.file = convert_pdf_gdocs(output_filename,f'test_{i}')
        text_to_send = derive_text(assignment.file)
        # prompt = enrich_format_message(message=text_to_send)
        # response = query_gpt(prompt)
        assignment.description = text_to_send
        assignment.marks = steps
        assignment.deadline = date.today() + timedelta(days=len(ranges))
        assignment.save()
        material.assignments.add(assignment)
        material.save()
        cleanup_folder('media/downloads/')
        print('Created: {}'.format(output_filename))
    return len(os.listdir('media/downloads/'))


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text


def derive_text(document_id):
    """Uses the Docs API to print out the text of a document."""
    creds = get_creds('docs.json','credentials.json','docs')
    docs_service = build('docs', 'v1', credentials=creds)
    # docs_service = discovery.build(
    #     'docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    doc = docs_service.documents().get(documentId=document_id).execute()
    doc_content = doc.get('body').get('content')
    return read_structural_elements(doc_content)

def cleanup_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))