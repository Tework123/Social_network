from django.contrib import admin

from album.models import Album, Photo, PhotoComment

admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(PhotoComment)

