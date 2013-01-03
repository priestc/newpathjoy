from django.contrib import admin
from models import (StepOne, StepTwo, StepThree, StepFour, StepFive, StepSix,
    StepSeven, StepEight, CompletedBooking)

class StepOneAdmin(admin.ModelAdmin):
    pass
    
class StepTwoAdmin(admin.ModelAdmin):
    pass

class StepThreeAdmin(admin.ModelAdmin):
    pass

class StepFourAdmin(admin.ModelAdmin):
    pass

class StepFiveAdmin(admin.ModelAdmin):
    pass

class StepSixAdmin(admin.ModelAdmin):
    pass

class StepSevenAdmin(admin.ModelAdmin):
    pass

class StepEightAdmin(admin.ModelAdmin):
    pass

class CompletedBookingAdmin(admin.ModelAdmin):
    readonly_fields = ('step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8')

admin.site.register(StepOne, StepOneAdmin)
admin.site.register(StepTwo, StepTwoAdmin)
admin.site.register(StepThree, StepThreeAdmin)
admin.site.register(StepFour, StepFourAdmin)
admin.site.register(StepFive, StepFiveAdmin)
admin.site.register(StepSix, StepSixAdmin)
admin.site.register(StepSeven, StepSevenAdmin)
admin.site.register(StepEight, StepEightAdmin)
admin.site.register(CompletedBooking, CompletedBookingAdmin)