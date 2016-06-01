from django.contrib import admin

# Register your models here.
from .models import WordSet, Word, Trial

admin.site.register(WordSet)
admin.site.register(Word)
admin.site.register(Trial)
