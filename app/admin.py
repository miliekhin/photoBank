from django.contrib import admin
from .models import Photo, UserTopNotifyMessage


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'viewed', 'created', 'file_name',)

    @staticmethod
    def owner(self, obj):
        return obj.username


class NotifyAdmin(admin.ModelAdmin):
    """Ограничиваем создание только одного сообщения"""
    def add_view(self, request, form_url='', extra_context=None):
        obj = UserTopNotifyMessage.objects.all().first()
        if obj:
            return self.change_view(request, object_id=str(obj.id) if obj else None)
        else:
            return super(type(self), self).add_view(request, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        return self.add_view(request)


admin.site.register(Photo, PhotoAdmin)
admin.site.register(UserTopNotifyMessage, NotifyAdmin)
