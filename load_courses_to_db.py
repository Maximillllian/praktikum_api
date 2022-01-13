import os
import re
import requests_async as requests
import asyncio
from django.core.checks.messages import Error
from slugify import slugify
from termcolor import colored, cprint
from compress_html import compress_html

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "praktikum_api.settings")

import django 
django.setup()

from api import models

def walk_error(error):
    print('\n' + '*' * 20)
    print(error.filename)
    print('\n' + '*' * 20 + '\n')


def print_tree_items(root, dirs, files):
    print('\n' + '*' * 20)
    print(f'root: {root}\n{dirs}\n{files}')
    print('\n' + '*' * 20 + '\n')


def path_array(root, to_replace):
    path = root.replace(FIRST_SPRINT, '')
    path_array = re.split(r'\\', path)
    return path_array


def parse_course_and_theme_name(path_array): 
    course_name = path_array[1]

    if len(path_array) == 3:
        theme_name = course_name
    elif len(path_array) > 2:
        theme_name = path_array[2]
    else:
        theme_name = course_name
    
    return course_name, theme_name


async def post_data(type, data):
    url = 'https://cryptodeputat.pythonanywhere.com/api/create/' + type
    res = await requests.post(url, json=data)
    return res


async def get_obj_or_false(type, slug):
    url = f'https://cryptodeputat.pythonanywhere.com/api/{type}/{slug}'
    res = await requests.get(url)
    cprint(res, 'green')
    if res.status_code == 200:
        return res.json()
    return False


async def get_or_create_object(type, data):
    object = await get_obj_or_false(type, slugify(data['title']))
    if object:
        return object['slug']
    res = await post_data(type, data)
    slug = slugify(res.json()['title'])
    return slug


# async def get_or_create_theme(theme_name, course_slug):
#     theme = await get_obj_or_false('theme', slugify(theme_name))
#     if theme:
#         return theme['slug']
#     data = {"title": theme_name, "course": course_slug}
#     res = await post_data('course', data)
#     slug = slugify(res.json()['title'])
#     return slug


LESSONS_PATH = r'D:\Courses\Yandex.Designer_interfaces\[SW.BAND] [Яндекс.Практикум] Профессия Дизайнер интерфейсов (2020) [Часть 1 из 7]\[SW.BAND] [Яндекс.Практикум] Профессия Дизайнер интерфейсов (2020) [Часть 1 из 7]'
FIRST_SPRINT = r'D:\designer_interfaces\[SW.BAND] 1 спринт'


tree = os.walk(FIRST_SPRINT, topdown=True, onerror=walk_error)
scan_dirs = os.scandir(LESSONS_PATH)
courses = []
themes = []
order = 0

async def main():
    for root, dirs, files in tree:
    
        for file in files:
            file_extension = file.split('.')[-1]
            if file_extension in ('html', 'txt'):
                path = path_array(root, LESSONS_PATH)
                course_name, theme_name = parse_course_and_theme_name(path)
                lesson_name = '.'.join(file.split('.')[:-1])

                course_data = {"title": course_name}
                course_slug = await get_or_create_object('course', course_data)

                theme_data = {"title": theme_name, "course": course_slug}
                theme_slug = await get_or_create_object('theme', theme_data)

                if theme_slug not in themes:
                    order = 0
                    themes.append(theme_slug)
                    
                raw_html = compress_html(f'{root}\{file}')
                lesson_data = {"title": lesson_name, "theme": theme_slug, "text": raw_html, "order": order}
                lesson_slug = await get_or_create_object('lesson', lesson_data)

                order += 1
                # cprint(f'Создали курс с респонзем: {res},\n сам курс - {course}', 'cyan')
                # finded_course = models.Course.objects.get_or_create(title=course_name)[0]

                # theme = models.Theme.objects.get_or_create(title=theme_name, course=finded_course)
                # finded_theme = theme[0]

                # finded_lesson = models.Lesson.objects.get_or_create(title=lesson_name, theme=finded_theme, text=raw_html, order=order)[0]

        

asyncio.run(main())