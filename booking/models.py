from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.core.exceptions import ValidationError

NUM_ROOMS = ((0,'0'), (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5+'))
SQ_FEET = (
    (1, "< 500"),
    (2, "500 - 1000"),
    (3, "1000 - 1500"),
    (4, "1500 - 2000"),
    (5, "2000 - 3000"),
    (6, "4000 - 4000"),
    (7, "4000+"),
)

class Step(models.Model):
    session = models.ForeignKey('sessions.Session', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        get_latest_by = 'created'

class StepOne(Step):
    bedrooms = models.IntegerField(choices=NUM_ROOMS, default=0)
    bathrooms = models.IntegerField(choices=NUM_ROOMS, default=0)

    def __unicode__(self):
        return "bed: %s bath: %s" % (self.bedrooms, self.bathrooms)


class StepTwo(Step):
    sq_feet = models.IntegerField(choices=SQ_FEET)

    def __unicode__(self):
        return "%s sq. feet" % self.get_sq_feet_display()

class StepThree(Step):
    laundry = models.BooleanField(default=False)
    inside_fridge = models.BooleanField(default=False)
    inside_oven = models.BooleanField(default=False)
    inside_cabinets = models.BooleanField(default=False)
    windows = models.BooleanField(default=False)
    walls = models.BooleanField(default=False)

    def __unicode__(self):
        disp = []
        fields = ['laundrey', 'inside_cabinets', 'insode_oven', 'inside_fridge', 'windows', 'walls']
        for field in fields:
            if getattr(self, field, False):
                disp.append(field)
        return ", ".join(disp)

def zipcode_validator(zipcode):
    z = str(zipcode)
    z = z.replace('-', '')
    if not (z.isdigit() and (len(z) == 5 or len(z) == 9)):
        raise ValidationError('Invalid Zipcode')


class StepFour(Step):
    street = models.TextField(blank=False)
    city = models.TextField(blank=False)
    state = USStateField()
    zipcode = models.CharField(max_length=10, validators=[zipcode_validator])

    def __unicode__(self):
        return "%s\n%s\n%s %s" % (self.street, self.city, self.state, self.zipcode)

class StepFive(Step):
    hours = models.IntegerField()
    num_cleaners = models.IntegerField("Number of cleaners", default=1, choices=((1, '1'), (2, '2')))

    def __unicode__(self):
        return "%s cleaners for %s hours" % (self.num_cleaners, self.hours)

class StepSix(Step):
    cleaning_datetime = models.DateTimeField()

    def __unicode__(self):
        return "at %s" % self.cleaning_datetime

def phone_validator(phone):
    p = str(phone)
    p = p.replace('-', '').replace(' ', '')
    if not p.isdigit():
        raise ValidationError('Invalid phone number')

class StepSeven(Step):
    fullname = models.TextField()
    email = models.EmailField()
    phone = models.TextField(validators=[phone_validator])
    referral = models.TextField(blank=True)

    def __unicode__(self):
        return "%s\n%s\n%s\n%s" % (self.fullname, self.email, self.phone, self.referral)

class StepEight(Step):
    stripe_token = models.TextField()

    def __unicode__(self):
        return "payment token: %s" % self.stripe_token

class CompletedBooking(models.Model):
    key = models.TextField()
    canceled = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    step1 = models.ForeignKey('StepOne')
    step2 = models.ForeignKey('StepTwo')
    step3 = models.ForeignKey('StepThree')
    step4 = models.ForeignKey('StepFour')
    step5 = models.ForeignKey('StepFive')
    step6 = models.ForeignKey('StepSix')
    step7 = models.ForeignKey('StepSeven')
    step8 = models.ForeignKey('StepEight')

    def __unicode__(self):
        return "%s (%s) - %s" % (self.step7.fullname, self.step7.phone, self.step6.cleaning_datetime)

