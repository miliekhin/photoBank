import os
import subprocess
from django.conf import settings
from app.models import Photo
from django.http import Http404
import shutil
from PIL import Image


def copy_top_photos_to_temp_dir(photos: list, media_dir: str, temp_dir: str) -> None:
    """Копируем топ картинки во временную папку для создания видеослайдшоу"""
    for i, photo_file in enumerate(photos, start=1):
        photo_file_new = f'top{i:02d}.jpg'
        if os.path.splitext(photo_file)[1].lower() == '.png':
            im = Image.open(os.path.join(media_dir, photo_file))
            im.convert('RGB').save(os.path.join(temp_dir, photo_file_new))
        else:
            shutil.copyfile(os.path.join(media_dir, photo_file), os.path.join(temp_dir, photo_file_new))


def prepare_top_photos(photos: list, is_user: int) -> str:
    """Подготовка временной папки для копирования картинок"""
    temp_dir = os.path.join(
        settings.VIDEO_SLIDESHOW_PATH,
        settings.TEMP_DIR_TOP_PHOTOS_USER if is_user else settings.TEMP_DIR_TOP_PHOTOS_SITE
    )
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)
    copy_top_photos_to_temp_dir(photos, settings.MEDIA_PATH, temp_dir)
    return temp_dir


def get_pic_list(user_id: int) -> list:
    """Возвращает список имен файлов картинок"""
    if user_id:
        photos = Photo.objects.filter(owner_id=user_id, viewed__gt=0)
    else:
        photos = Photo.objects.filter(viewed__gt=0)

    if not len(photos):
        raise Http404("No viewed photos.")

    pl = photos.order_by('-viewed')[:10].values_list('file_name', flat=True)
    return pl


def check_ffmpeg_exists() -> str:
    """Проверяет наличие файла ffmpeg.exe в папке виртуального окружения"""
    ffmpeg_path = os.path.join(settings.BASE_DIR, 'venv', 'Scripts', 'ffmpeg.exe')
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError('ffmpeg module not found.')
    return ffmpeg_path


def get_slideshow_path(is_user: int) -> str:
    """Возвращает путь к папке слайдшоу"""
    slideshow_path = os.path.join(
        settings.VIDEO_SLIDESHOW_PATH,
        settings.TOP_PHOTOS_SLIDESHOW_FILE_NAME_USER if is_user else settings.TOP_PHOTOS_SLIDESHOW_FILE_NAME_SITE
    )
    os.makedirs(os.path.dirname(slideshow_path), exist_ok=True)
    return slideshow_path


def convert_photos_to_video(ffmpeg_path: str, slideshow_path: str, temp_dir: str) -> None:
    """Создание файла видеослайдшоу из картинок"""
    sp = subprocess.run(
        [ffmpeg_path, '-y', '-framerate', f'1/{settings.VIDEO_SLIDESHOW_FRAME_DURATION_SEC}',
         '-i', temp_dir + r'\top%02d.jpg',
         '-vf', 'scale=640:480:force_original_aspect_ratio=decrease,pad=640:480:(ow-iw)/2:(oh-ih)/2,setsar=1',
         '-pix_fmt', 'yuv420p', slideshow_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if sp.returncode != 0:
        raise Exception('Video Encoding Error: ' + str(sp.stderr))


def build_video_slideshow(user_id: int) -> None:
    """Подготовка и cоздание видеофайла слайдшоу в формате webm"""
    ffmpeg_path = check_ffmpeg_exists()
    slideshow_path = get_slideshow_path(user_id)
    temp_dir = prepare_top_photos(get_pic_list(user_id), user_id)
    convert_photos_to_video(ffmpeg_path, slideshow_path, temp_dir)
