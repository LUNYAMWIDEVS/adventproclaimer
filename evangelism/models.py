from django.db import models

# Create your models here.

class MedicalMissionaryDailyReport(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    missionary_name = models.CharField(max_length=255, null=True, blank=True)
    name_of_patient = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    name_of_patients = models.CharField(max_length=255, null=True, blank=True)
    number_of_patients = models.IntegerField(null=True, blank=True)
    health_history = models.TextField(null=True, blank=True)
    interventions = models.TextField(null=True, blank=True)
    challenges_missionary_side = models.TextField(null=True, blank=True)
    new_patient_number = models.IntegerField(null=True, blank=True)
    nurture_rp_name = models.CharField(max_length=255, null=True, blank=True)
    nurture_rp_phone_number = models.CharField(max_length=50, null=True, blank=True)
    patient_contact_phone_number = models.CharField(max_length=50, null=True, blank=True)
    signs_and_symptoms = models.TextField(null=True, blank=True)
    measure = models.TextField(null=True, blank=True)  # "What measure are you taking e.g. Hydrotherapy"
    needs_interest_side = models.TextField(null=True, blank=True)
    vital_signs_heart_rate = models.IntegerField(null=True, blank=True)
    vital_signs_respiratory_rate = models.IntegerField(null=True, blank=True)
    vital_signs_temperature = models.FloatField(null=True, blank=True)  # Assuming temperature can be a float
    check_on_the_following_areas = models.TextField(null=True, blank=True)
    description_on_parameters = models.TextField(null=True, blank=True)  # "Give a brief description on the above parameters"
    symptoms_that_are_better = models.TextField(null=True, blank=True)
    symptoms_that_have_worsened = models.TextField(null=True, blank=True)
    food = models.TextField(null=True, blank=True)
    herb = models.TextField(null=True, blank=True)
    drink = models.TextField(null=True, blank=True)
    hydotherapies_administered = models.TextField(null=True, blank=True)  # "Tick any of the hydotherapies if administered"
    vegetables = models.TextField(null=True, blank=True)
    fruits = models.TextField(null=True, blank=True)
    juices = models.TextField(null=True, blank=True)
    legumes = models.TextField(null=True, blank=True)
    wholegrains = models.TextField(null=True, blank=True)
    seeds = models.TextField(null=True, blank=True)
    nuts = models.TextField(null=True, blank=True)
    water_quantify = models.FloatField(null=True, blank=True)  # "Quantify in terms of liters"
    walk_distance_minutes = models.FloatField(null=True, blank=True)  # "either provide distance in km or in terms of minutes"
    physiotherapies = models.TextField(null=True, blank=True)
    massage = models.TextField(null=True, blank=True)
    fill_in_the_following_yes = models.BooleanField(default=False)  # Assuming this is a Yes/No field
    fill_in_the_following_no = models.BooleanField(default=False)   # Assuming this is a Yes/No field
    fill_in_the_following_row3 = models.BooleanField(default=False)  # Assuming this is a Yes/No field
    open_air_hours = models.FloatField(null=True, blank=True)  # "How long were they in the open air (quantify in hours)?"
    quality_perspective = models.TextField(null=True, blank=True)  # "Quality as per individual's perspective"
    number_of_hours = models.FloatField(null=True, blank=True)  # Assuming this can be a float
    health_counseling_shared = models.TextField(null=True, blank=True)  # "What health counselling have you shared with interest?"
    fill_in_the_following_yes1 = models.BooleanField(default=False)  # Assuming this is a Yes/No field
    fill_in_the_following_no1 = models.BooleanField(default=False)   # Assuming this is a Yes/No field
    hospital_referrals_summary = models.TextField(null=True, blank=True)  # "Are there any hospital referrals if yes"


    # Add more fields as needed
    def __str__(self) -> str:
        return self.missionary_name if self.missionary_name else "Medical Missionary Daily Report"

class BibleWorkerDailyReport(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    email_address = models.EmailField(null=True, blank=True)
    missionary_name = models.CharField(max_length=255,null=True, blank=True)
    homes_visited = models.IntegerField(null=True, blank=True)
    home_visited = models.CharField(max_length=255,null=True, blank=True)
    interest_phone_number = models.CharField(max_length=255,null=True, blank=True)
    study = models.CharField(max_length=255,null=True, blank=True)
    people_attended = models.IntegerField(null=True, blank=True)
    homes_rejected = models.IntegerField(null=True, blank=True)
    challenges = models.TextField(null=True, blank=True)
    prayer_requests = models.TextField(null=True, blank=True)
    appointments = models.IntegerField(null=True, blank=True)
    homes_under_appointments = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    nurturing_rp_name = models.CharField(max_length=255,null=True, blank=True)
    nurturing_rp_phone_number = models.CharField(max_length=255,null=True, blank=True)
    appointment_day = models.CharField(max_length=10,null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    needs = models.TextField(null=True, blank=True)
    to_be_nurtured = models.BooleanField(default=False)

    def __str__(self):
        return self.missionary_name if self.missionary_name else "Bible Worker Daily Report"

class AdventistMuslimRelationsDailyReport(models.Model):
    name = models.CharField(max_length=1024)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)


class Survey(models.Model):
    TYPES = (
        ('Bible Worker', 'Bible Worker'),
        ('Medical Missionary', 'Medical Missionary'),
        ('Adentist Muslim Relations', 'Adentist Muslim Relations'),
    )   
    DAYS = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    name = models.CharField(max_length=1024,null=True,blank=True)
    scheduled_day = models.CharField(choices=DAYS,default='Sunday',null=True,blank=True)
    scheduled_time = models.TimeField(null=True,blank=True)
    interest_type = models.CharField(max_length=100,choices=TYPES, default='Bible Worker',null=True,blank=True)
    bible_worker = models.ForeignKey(BibleWorkerDailyReport,on_delete=models.CASCADE,null=True,blank=True)
    medical_missionary = models.ForeignKey(MedicalMissionaryDailyReport,on_delete=models.CASCADE,null=True,blank=True)  
    adventist_muslim_relations = models.ForeignKey(AdventistMuslimRelationsDailyReport,on_delete=models.CASCADE,null=True,blank=True)   
    date_posted = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=50,null=True,blank=True)


    def __str__(self) -> str:
        return f"{self.name} - {self.scheduled_day} - {self.scheduled_time}"
