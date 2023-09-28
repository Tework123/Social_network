from django.core.management import BaseCommand

from album.models import Photo


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # удаляем все оставшиеся фото
        photos = Photo.objects.all()
        for photo in photos:
            photo.image.delete(save=True)
            photo.delete()
