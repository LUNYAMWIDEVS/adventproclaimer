from django.test import TestCase

# Create your tests here.
for index,paragraph in enumerate(paragraphs):
    print(index)
    if index < len(paragraphs) - 1:
        if len(short_msg) == 5:
            short_msg = []
            current_length = 0
            print(short_msg)
            print(current_length)
            continue
        else:
            pass