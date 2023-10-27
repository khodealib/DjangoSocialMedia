from django.contrib import admin

from account.models import Relation


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    pass
