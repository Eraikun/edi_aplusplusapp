
from django.contrib import admin
from .models import Employee, Team, WorkArrangement,TeamLeader, TeamMember

# Register your models here.
admin.site.register(Employee)
admin.site.register(Team)
admin.site.register(TeamLeader)
admin.site.register(TeamMember)
admin.site.register(WorkArrangement)