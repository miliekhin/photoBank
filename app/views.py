from django.http import Http404
from app.videoslideshow import build_video_slideshow
from django.conf import settings
from django.shortcuts import redirect


def slider_user(request, user_id):
    """
    Создание слайдшоу из топ 10 картинок юзера.
    В случае любой ошибки на этапе создания слайдшоу будет возращаться 404
    """
    try:
        build_video_slideshow(user_id)
    except Exception as e:
        raise Http404(str(e))
    slideshow_file = settings.TOP_PHOTOS_SLIDESHOW_FILE_NAME_SITE
    if user_id:
        slideshow_file = settings.TOP_PHOTOS_SLIDESHOW_FILE_NAME_USER

    return redirect(f'/media/video_slideshow/{slideshow_file}')


def slider_site(request):
    """
    Передаём нулевого юзера в другую вьюшку, чтобы создалось слайдшоу из топ 10 картинок всего сайта.
    """
    return slider_user(request, 0)
