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
    # Split path string to array
    path = root.replace(to_replace, '')
    path_array = re.split(r'\\', path)
    return path_array


def replace_ad(string, ad_string='[SW.BAND] '):
    return string.replace(ad_string, '')


def parse_sprint_module_and_theme_name(path_array): 
    print(path_array)
    sprint_name = replace_ad(path_array[1])
    module_name = replace_ad(path_array[2])

    if len(path_array) == 4:
        theme_name = module_name
    elif len(path_array) > 3:
        theme_name = replace_ad(path_array[3])
    else:
        theme_name = module_name
    
    return sprint_name, module_name, theme_name


async def post_data(type, data):
    url = 'https://cryptodeputat.pythonanywhere.com/api/create/' + type
    res = await requests.post(url, json=data)
    return res


async def get_obj_or_false(type, slug):
    url = f'https://cryptodeputat.pythonanywhere.com/api/{type}/{slug}'
    res = await requests.get(url)
    cprint(f'Объект есть? {res}', 'green')
    if res.status_code == 200:
        return res.json()
    return False


async def get_or_create_object(type, data):
    object = await get_obj_or_false(type, slugify(data['title']))
    if object:
        return object['slug']
    res = await post_data(type, data)
    print(f'Ответ после создание - {res}')
    slug = slugify(res.json()['title'])
    return slug


LESSONS_PATH = r'D:\Courses\Yandex.Designer_interfaces\[SW.BAND] [Яндекс.Практикум] Профессия Дизайнер интерфейсов (2020) [Часть 1 из 7]\[SW.BAND] [Яндекс.Практикум] Профессия Дизайнер интерфейсов (2020) [Часть 1 из 7]'
FIRST_SPRINT = r'D:\designer_interfaces\[SW.BAND] 1 спринт'
SPRINTS_DIR = r'D:\designer_interfaces'


tree = os.walk(SPRINTS_DIR, topdown=True, onerror=walk_error)
modules = []
themes = []
order = 0

async def main():
    for root, dirs, files in tree:
        for file in files:

            file_extension = file.split('.')[-1]
            if file_extension in ('html', 'txt'):

                # Getting sprint, module, theme, lesson name 
                path = path_array(root, SPRINTS_DIR)
                sprint_name, module_name, theme_name = parse_sprint_module_and_theme_name(path)
                lesson_name = '.'.join(file.split('.')[:-1])
                raw_html = compress_html(f'{root}\{file}')

                sprint_data = {"title": sprint_name}
                sprint_slug = await get_or_create_object('sprint', sprint_data)

                module_data = {"title": module_name, "sprint": sprint_slug}
                module_slug = await get_or_create_object('module', module_data)

                theme_data = {"title": theme_name, "module": module_slug}
                theme_slug = await get_or_create_object('theme', theme_data)

                if theme_slug not in themes:
                    order = 0
                    themes.append(theme_slug)
                    
                lesson_data = {"title": lesson_name, "theme": theme_slug, "text": raw_html, "order": order}
                lesson_slug = await get_or_create_object('lesson', lesson_data)

                # cprint(f'Создали курс с респонзем: {res},\n сам курс - {module}', 'cyan')
                # finded_sprint = models.Sprint.objects.get_or_create(title=sprint_name)[0]
                # finded_module = models.Module.objects.get_or_create(title=module_name, sprint=finded_sprint)[0]

                # theme = models.Theme.objects.get_or_create(title=theme_name, module=finded_module)
                # finded_theme = theme[0]

                # if finded_theme.title not in themes:
                #     order = 0
                #     themes.append(finded_theme.title)

                # finded_lesson = models.Lesson.objects.get_or_create(title=lesson_name, theme=finded_theme, text=raw_html, order=order)[0]
                order += 1
        

asyncio.run(main())
# main()