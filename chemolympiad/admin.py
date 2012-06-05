from chemolympiad.models import *
from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('topics',)

class TopicAdmin(admin.ModelAdmin):
    filter_horizontal = ('subfield',)

admin.site.register(Competition)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Subfield)

