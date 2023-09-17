from .celery import app as celery_app

__all__ = ("celery_app",)

# понять как импортировать селери из другого app
# переписать на классах
# доделать по статьям, написать для email и еще что нибудь
