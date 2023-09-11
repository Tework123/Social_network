from django.contrib import admin

from chat.models import Chat, Relationship, Message

admin.site.register(Chat)
admin.site.register(Relationship)
admin.site.register(Message)
