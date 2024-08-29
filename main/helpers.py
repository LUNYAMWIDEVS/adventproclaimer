from __future__ import print_function
from io import BytesIO
import os
import json
import requests
import random
import logging
import pytz
from datetime import datetime
from PyPDF2 import PdfReader,PdfWriter
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings
from django.shortcuts import get_object_or_404
from celery import shared_task
from .models import Assignment,Material,Student
from quiz.models import Question,Quiz
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from datetime import timedelta, date
from .prompt import enrich_format_message
from messenger.llm import query_gpt
from chunked_upload.models import ChunkedUpload
import shutil

SCOPES = {
    'drive': ['https://www.googleapis.com/auth/drive'],
    'docs':['https://www.googleapis.com/auth/documents']
}
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
PARENT_FOLDER_ID = '1_c7FLhKFJz_j-jquhOkSOSv5cIg2sv9k'

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

    with open("service_account_key.json", 'w') as outfile:
        json.dump(creds, outfile)
    
    if not os.path.exists('media/'):
        os.makedirs('media/')
    
    if not os.path.exists('media/downloads/'):
        os.makedirs('media/downloads/')




def get_creds(credentials_file,scopes):
    if not os.path.exists('media/'):
        os.makedirs('media/')
    
    if not os.path.exists('media/downloads/'):
        os.makedirs('media/downloads/')
    # The file token_drive.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # import pdb;pdb.set_trace()
    # generate_credentials_json()
    creds = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=SCOPES[scopes])
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
    
    return creds

def handle_uploaded_file(f):
    with open('media/downloads/downloaded.pdf', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class ChunkedBytesIO(BytesIO):
    def chunks(self, chunk_size=1 * 1024 * 1024):
        while True:
            chunk = self.read(chunk_size)
            if not chunk:
                break
            yield chunk

@shared_task
def upload_file_to_google_drive():
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = get_creds('service_account_key.json','drive')
    # if not creds.valid:
    #     creds.refresh(Request())
    file_obj = ChunkedUpload.objects.last()
    temp_path = file_obj.file.path
    

    
    # if hasattr(file_obj,'temporary_file_path'):
    #     temp_path = file_obj.file.path
    # else:
        
    #     handle_uploaded_file(file_obj)
    #     temp_path = 'media/downloads/downloaded.pdf'
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'parents':[PARENT_FOLDER_ID],'name': file_obj.filename}
        
        
        media = MediaFileUpload(temp_path, resumable=True, chunksize=1024*1024)
        request = service.files().create(body=file_metadata, media_body=media)

        response = None
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    print(f"Uploaded {int(status.progress() * 100)}%.")
            except HttpError as e:
                print(f"An error occurred: {e}")
                response = None  # Reset response to continue upload

        print(f"File uploaded: {response.get('id')}")

    except HttpError as error:
        print(F'An error occurred: {error}')
        
    # import pdb;pdb.set_trace()
    material = Material()
    material.file = response.get('id')
    material.save()


    cleanup_folder('media/chunked_uploads/')

    return response.get('id')


def convert_pdf_gdocs(file_path,name):
    """Upload file with conversion
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = get_creds('service_account_key.json','drive')

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'parents':[PARENT_FOLDER_ID],
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
    creds = get_creds('service_account_key.json','drive')
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
  creds = get_creds('service_account_key.json','drive')
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
    material = Material.objects.filter(file=file_id).last()
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
    creds = get_creds('service_account_key.json','docs')
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


@shared_task
def schedule_assignments(course_format,student_id,id,generate_quiz=True):
    material = Material.objects.filter(id=id).last()
    assignments =material.assignments.all()
    desired_timezone = pytz.timezone('Africa/Nairobi')
    utc_now = datetime.utcnow()
    current_time_in_utc = desired_timezone.localize(utc_now)
    student = Student.objects.get(student_id=student_id)

    morning_flag = True
    check_quiz = Quiz.objects.filter(course = material.course_code) # check if quiz already exists first
    for index,assignment in enumerate(assignments):
        if not check_quiz.exists():
            try:
                # TODO: order the assignments
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful expert in Bible and Spirit of Prophecy matters. Your aim is to ask questions,give title also based on the"
                        f"information: {assignment.description},"
                    },
                    {"role": "user", "content": f"return a json with 5 questions and 4 options and the answer in the format below and preserve the json keys in english and format to strictly remain as shown below"
                        "{'title':'title','questions':[{'question1':['option1','option2'],'answer':'answer'},{'question2':['option1','option2'],'answer':'answer'}]}"}
                ]
                # TODO: ensure the loop is not one assignment per day
                body = {
                    "model": "gpt-4-1106-preview",
                    "response_format":{"type":"json_object"},
                    "messages": messages,
                }
                header = {"Authorization": "Bearer " + os.getenv("OPENAI_API_KEY").strip()}

                response = requests.post("https://api.openai.com/v1/chat/completions", json=body, headers=header)
                logging.warn(str(["time elapsed", response.elapsed.total_seconds()]))
                # logging.warn('\nmodel API response', str(res.json()))

                
                
                # response = openai_client.chat.completions.create(
                #     model="gpt-3.5-turbo",
                #     messages=messages,
                # )
                # import pdb;pdb.set_trace()
                results = response.json()
                content = json.loads(results['choices'][0]['message']['content'])
                print(content)
                # generate a quiz
                quiz = Quiz()
                quiz.assignment = assignment
                quiz.course = assignment.course_code
                quiz.title = content.get('title')
                quiz.start = datetime.now(tz=desired_timezone)
                quiz.end = datetime.now(tz=desired_timezone)+timedelta(days=360)
                quiz.save()
                options = ['option1', 'option2', 'option3', 'option4']
                # check obtained respons has the appropriate keys
                if "questions" in content:
                    # Iterate over each question in the content

                    # if "question1" in content["questions"][0].keys():
                        # Iterate over each question in the content
                    for i,question_ in enumerate(content.get('questions'),start=1):
                        
                        answer_ = question_.pop('answer')
                        print(answer_)
                        # del question_['answer']
                        first_key, _ = next(iter(question_.items()))
                        
                        question_info = question_[first_key]
                        print(question_info)
                        options_ = []
                        if isinstance(question_info,str):
                            del question_[first_key]
                        else:
                            question_info_ = question_info.pop(0)
                            for k_ in question_info:
                                options_.append({options[k_]:question_info[k_]})
                            question_info = question_info_

                        print(question_info)

                        for k,info in enumerate(question_):
                            if info == 'options':
                                for i,j in enumerate(question_['options']):
                                    try:
                                        options_.append({options[i]:j})
                                    except Exception as err:
                                        print(err)
                                    
                                    
                        # Flatten the list of dictionaries into a single dictionary
                        flattened_dict_ = {k: v for d in options_ for k, v in d.items()}
                        print(flattened_dict_)

                        # Shuffle the items in the dictionary
                        items = list(flattened_dict_.items())
                        random.shuffle(items)
                        flattened_dict = dict(items)

                        # Map the answer to a letter
                        mapper = {0: "A", 1: "B", 2: "C", 3: "D"}
                        correct_answer = None
                        for k,option_key in enumerate(flattened_dict):
                            if flattened_dict[option_key] == answer_:
                                print(f"{k}===={flattened_dict[option_key]}==={mapper.get(k)}")
                                correct_answer = mapper.get(k)

                        # Save the question and options to the database
                        Question.objects.create(question=question_info,answer=correct_answer,quiz=quiz,marks=1,**flattened_dict)

                    # else:
                    #     print("The questions do not have their respective keys e.g. 'question1','question2'....")
                else:
                    print(f"The response did not return questions in the keys for assignment ====> {assignment.id}")
            except Exception as err:
                print(err)
        # we get todays date -  kenyan time
        # TODO: get relative date from frontend
        # for whatsapp send chunks after every hour till chunks are over based on 
        # the time the client wanted the text to be sent, also during the evening 
        # send the quiz
        # for email send morning and evening devotion and at evening 2 hours before evening 
        # devotion send quiz link
        # for phone calls send morning and evening devotion
        
        
        try:
            # import pdb;pdb.set_trace()
            # print(form['course_format'].value)
            # print(course_format)
            if course_format == 'P':
                # import pdb;pdb.set_trace()
                relative_date = datetime.now(tz=desired_timezone) + timedelta(days=index+1)
                schedule = None
                random_minutes = random.randint(1,2)
                random_hour = None
                time_period = None
                if morning_flag:
                    random_hour = random.randint(6,7)  # morning devotion
                    time_period = "Morning"
                else:
                    random_hour = random.randint(6, 7)  # evening devotion
                    time_period = "Evening"

                morning_flag = not morning_flag  # Toggle the flag
                schedule, _ = CrontabSchedule.objects.get_or_create(
                    minute=f'{random_minutes}',
                    hour=f'{random_hour}',
                    day_of_week=f'*',
                    day_of_month=f'{relative_date.day}',
                    month_of_year=f'{relative_date.month}',
                    timezone=desired_timezone
                )
                PeriodicTask.objects.update_or_create(
                    crontab=schedule,                  # we created this above.
                    name=f'Send Assignment {time_period} - {student.name} - {assignment.id}--{index}',          # simply describes this periodic task.
                    task='messenger.tasks.phone_call_manager.send_voice_over_call',  # name of task.
                    args=json.dumps([student.phone_number, assignment.description]),
                )
                
            if course_format == 'W':
                # handle whatsapp logic
                # TODO: implement relative date from the frontend
                relative_date = datetime.now(tz=desired_timezone) + timedelta(days=index+1) #TODO: implement option of beginning today or tomorrow from frontend too.
                chunks = assignment.break_desc_into_whatsapp_msg_chunks()
                time_period = None
                for i,chunk in enumerate(chunks,start=1):
                    schedule = None
                    schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute=f'{relative_date.minute}',
                        hour=f'{relative_date.hour+i}',
                        day_of_week=f'*',
                        day_of_month=f'{relative_date.day}',
                        month_of_year=f'{relative_date.month}',
                        timezone = desired_timezone
                    )
                    
                    PeriodicTask.objects.update_or_create(
                        crontab=schedule,                  # we created this above.
                        name=f'Send Morning Assignment - {student.name} - {assignment.id}--{index}',          # simply describes this periodic task.
                        task='messenger.tasks.whatsapp_manager.send_batch_whatsapp_text_with_template',  # name of task.
                        args=json.dumps([[student.phone_number], [student.name], str(i), chunk]),
                    )

                schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute=f'{relative_date.minute}',
                        hour=f'{relative_date.hour+12}', #TODO: add evening schedule from frontend
                        day_of_week=f'*',
                        day_of_month=f'{relative_date.day}',
                        month_of_year=f'{relative_date.month}',
                        timezone = desired_timezone
                    )
                PeriodicTask.objects.update_or_create(
                    crontab=schedule,                  # we created this above.
                    name=f'Send Evening Assignment - {student.name} - {assignment.id}',          # simply describes this periodic task.
                    task='messenger.tasks.whatsapp_manager.send_batch_whatsapp_text_with_template',  # name of task.
                    args=json.dumps([[student.phone_number], [student.name], str(i), f"do quiz @ https://adventproclaimer.com/quizSummary/{assignment.course_code.code}/{quiz.pk}/"]),
                )
            if course_format == 'E':
                relative_date = datetime.now(tz=desired_timezone) + timedelta(days=index+1)
                schedule = None
                random_minutes = random.randint(1,2)
                random_hour = None
                time_period = None
                if morning_flag:
                    random_hour = random.randint(6, 7)  # morning devotion
                    time_period = "Morning"
                else:
                    random_hour = random.randint(6, 7)  # evening devotion
                    time_period = "Evening"

                morning_flag = not morning_flag  # Toggle the flag
                schedule, _ = CrontabSchedule.objects.get_or_create(
                    minute=f'{random_minutes}',
                    hour=f'{random_hour}',
                    day_of_week=f'*',
                    day_of_month=f'{relative_date.day}',
                    month_of_year=f'{relative_date.month}',
                )
                PeriodicTask.objects.update_or_create(
                    crontab=schedule,                  # we created this above.
                    name=f'Send Assignment {time_period} - {student.name} - {assignment.id}--{index}',          # simply describes this periodic task.
                    task='messenger.tasks.email_manager.send_newsletter',  # name of task.
                    args=json.dumps([student.name, student.email,assignment.description]),
                )
                PeriodicTask.objects.update_or_create(
                    crontab=schedule,                  # we created this above.
                    name=f'Send Assignment {time_period} - {student.name} - {assignment.id}--{index}',          # simply describes this periodic task.
                    task='messenger.tasks.email_manager.send_newsletter',  # name of task.
                    args=json.dumps([[student.phone_number], [student.name], f"do quiz @ https://adventproclaimer.com/quizSummary/{assignment.course_code.code}/"]),
                )
            
        except Exception as err:
            print(err)
