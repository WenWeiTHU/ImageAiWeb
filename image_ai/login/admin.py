from django.contrib import admin
from .models import User, Record


class RecordInline(admin.TabularInline):
    model = Record
    extra = 3


class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'password']
    inlines = [RecordInline]
    list_display = ('username',)
    list_filter = ['username']
    search_fields = ['username']


# add admin register
admin.site.register(User, UserAdmin)
admin.site.register(Record)
