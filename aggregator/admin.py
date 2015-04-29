from django.contrib import admin

from .models import Commit, ResultSet

admin.site.register(Commit)
admin.site.register(ResultSet)

admin.AdminSite.site_header = "Jenkins Aggregator Administration"