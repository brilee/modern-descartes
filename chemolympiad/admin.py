from chemolympiad.models import *
from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('topics',)

admin.site.register(Competition)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic)


