from django.contrib import admin
from .models import Competitor
from .forms import CompetitorAdminForm
# Register your models here.

class CompetitorAdmin(admin.ModelAdmin):
    form = CompetitorAdminForm

admin.site.register(Competitor, CompetitorAdmin)
