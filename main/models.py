from django.db import models
from froala_editor.fields import FroalaField
import re
# Create your models here.


class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    role = models.CharField(
        default="Student", max_length=100, null=False, blank=True)
    course = models.ManyToManyField(
        'Course', related_name='students', blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True,
                              null=False, default='profile_pics/default_student.png')
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=False, blank=False, related_name='students')

    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_student.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name


class Faculty(models.Model):
    faculty_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=False, related_name='faculty')
    role = models.CharField(
        default="Faculty", max_length=100, null=False, blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True,
                              null=False, default='profile_pics/default_faculty.png')

    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_faculty.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Faculty'

    def __str__(self):
        return self.name


class Department(models.Model):
    department_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

    def student_count(self):
        return self.students.count()

    def faculty_count(self):
        return self.faculty.count()

    def course_count(self):
        return self.courses.count()


class Course(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=False, related_name='courses')
    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    studentKey = models.IntegerField(null=False, unique=True)
    facultyKey = models.IntegerField(null=False, unique=True)

    class Meta:
        unique_together = ('code', 'department', 'name')
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Announcement(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    description = FroalaField()

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-datetime']

    def __str__(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    
class Assignment(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    deadline = models.DateTimeField(null=True,blank=True)
    file = models.CharField(max_length=255,null=True, blank=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=True,blank=True)

    class Meta:
        verbose_name_plural = "Assignments"
        ordering = ['datetime']

    def __str__(self):
        return self.file

    def delete(self, *args, **kwargs):
        # self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def due_date(self):
        if self.deadline:
            return self.deadline.strftime("%d-%b-%y, %I:%M %p")
    def formated_description(self):
        if self.description is not None:
            stripped_text = re.sub(r'(?<=\w)\.\s+', '.\n\n', self.description.strip())
            formatted_text = re.sub(r'\n{2,}', '\n\n', stripped_text)
            return formatted_text
        else:
            return ''
    
    def html_description(self):
        # Parse to medium blog post text
        formatted_text = self.formated_description()

        # Add HTML tags
        html_text = f"<p>{formatted_text}</p>"
        html_text = html_text.replace('\n\n', '</p>\n\n<p>')
        
        return html_text
    
    def number_of_paragraphs(self):
        unescaped_text = self.html_description()
        text_without_tags = re.sub(r'<.*?>', '', unescaped_text)
        # Split the text into paragraphs
        paragraphs = text_without_tags.split('\n\n')
        length = len(paragraphs)
        
        return length
    
    # Assignment string lentth
    def string_length(self):
        text = self.whatsapp_formatted_description()
        remove_new_line_chars =text.replace('\n',"")
        return len(remove_new_line_chars)
    
    # how many paragraphs fit into 912 char length and send thosee ones
    
    # Break down the text into readable paragrphs
    def whatsapp_formatted_description(self):
        unescaped_text = self.html_description()
        text_without_tags = re.sub(r'<.*?>', '', unescaped_text)
        # Split the text into paragraphs
        if text_without_tags is not None:
            paragraphs = text_without_tags.split('\n\n')
        else:
            return ''
    
        formatted_text = ""

        for paragraph in paragraphs:
            # Skip empty paragraphs
            if not paragraph.strip():
                continue
            print (paragraph)
            print ('********')
            # Otherwise, add the paragraph content
            formatted_text += f"{paragraph.strip()}\n\n"

        return formatted_text
    
    # break the assignment into paragraph chunks that can be sent in whatsapp msg
    def break_desc_into_whatsapp_msg_chunks(self, max_chars=912):
        # Split the text into paragraphs
        text = self.whatsapp_formatted_description()
        paragraphs = text.split('\n\n')
        # Initialize variables
        message = ''
        messages = []
        short_msg = []
        current_length = 0
        # Iterate through each paragraph
        for index, paragraph in enumerate(paragraphs):
            if index < len(paragraphs) - 1:
                
                if len(short_msg) == 5:
                    short_msg = []
                    current_length = 0
                    # print("Stopping max length reached", current_length)
                    continue
                
                else: 
                    #  remove new line characters
                    message = paragraph.replace("\n","") 
                    # Check if adding the next paragraph would exceed the maximum character limit
                    if current_length + len(message) < max_chars:
                        # If so & the msg is not empty, append the current message to the list of short messages
                        if message:
                            short_msg.append(message)
                            # print("Short message", message)
                            current_length += len(message)
                            
            
                    
                    # check if the message length is close or greater than the maximum length & continue
                    if current_length + len(paragraphs[index +1]) < max_chars:
                        message = ''
                        continue
                    # otherwise start a new whatsapp message
                    else:
                        messages.append(short_msg)
                        short_msg = []
                        current_length = 0
                        # print("Stopping max length reached", current_length)
                        continue
        return messages
    
    
        



class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    summary = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to='submissions/', null=True,)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    marks = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

    def file_name(self):
        return self.file.name.split('/')[-1]

    def time_difference(self):
        difference = self.assignment.deadline - self.datetime
        days = difference.days
        hours = difference.seconds//3600
        minutes = (difference.seconds//60) % 60
        seconds = difference.seconds % 60

        if days == 0:
            if hours == 0:
                if minutes == 0:
                    return str(seconds) + " seconds"
                else:
                    return str(minutes) + " minutes " + str(seconds) + " seconds"
            else:
                return str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"
        else:
            return str(days) + " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"

    def submission_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def delete(self, *args, **kwargs):
        # self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.student.name + " - " + self.assignment.title

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name_plural = "Submissions"
        ordering = ['-datetime']


class Material(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    description = models.TextField(max_length=2000, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    file = models.CharField(max_length=255,null=True, blank=True)
    assignments = models.ManyToManyField(Assignment)
    pages = models.IntegerField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Materials"
        ordering = ['-datetime']

    def __str__(self):
        return self.file

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")