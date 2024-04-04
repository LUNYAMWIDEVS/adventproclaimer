from time import sleep
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from django.template import loader
import re

# @shared_task
def send_newsletter(subject,email_address, message):
    """Sends an email when the feedback form has been submitted."""

    medium_blog_post_text = parse_to_medium_blog_post(message)
    html_text = parse_to_html(medium_blog_post_text)
    # Create EmailMultiAlternatives object
    msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [email_address])
    rendered_template = loader.render_to_string("email_template.html",context={'html_text':html_text, 'title': 'Title'})
    # Attach HTML content
    msg.attach_alternative(rendered_template, "text/html")
    # Send email
    msg.send()

    # this method adds paragraph breaks to newlines to space sentences
def parse_to_medium_blog_post(raw_string):
    # Add paragraph breaks
    medium_blog_post_text = re.sub(r'(?<=\w)\.\s+', '.\n\n', raw_string.strip())
    medium_blog_post_text = re.sub(r'\n{2,}', '\n\n', medium_blog_post_text)
    return medium_blog_post_text

    
    # This method add paragraph tags to new lines 
def parse_to_html(raw_string):
    # Parse to medium blog post text
    medium_blog_post_text = parse_to_medium_blog_post(raw_string)

    # Add HTML tags
    html_text = f"<p>{medium_blog_post_text}</p>"
    html_text = html_text.replace('\n\n', '</p>\n\n<p>')
    
    return html_text