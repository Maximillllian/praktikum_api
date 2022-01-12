import codecs
import os
import re
from bs4 import BeautifulSoup

LESSONS_PATH = r'C:\Users\Owner\Desktop\Files\Projects\VS_Code\praktikum\static\lessons'


def get_html(path):
    html = codecs.open(path, 'r', 'utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def replace_savepage_url_in_background_image(soup):
    elements = soup.find_all('div', attrs={
        'style': lambda value: value and ('background-image' in value) and ('savepage-url' in value)})
    for el in elements:
        style_str = el['style']
        background_image_pattern = 'background-image.+;'
        background_image_str = re.findall(background_image_pattern, style_str)[0]
        url = re.findall(r'savepage-url=(.+)\*/', background_image_str)[0]
        fixed_background_image_str = f'background-image: url({url})'
        el['style'] = re.sub(background_image_pattern, fixed_background_image_str, style_str)
    return soup


def remove_tag_by_id(soup, id_):
    tag = soup.find(attrs={'id': id_})
    try:
        tag.decompose()
    except:
        pass
    return soup


def remove_tag_by_class(soup, class_):
    tag = soup.find(attrs={'class': class_})
    try:
        tag.decompose()
    except:
        pass
    return soup


def rewrite_tags_with_savepage_src(soup, attr='data-savepage-src'):
    tags = soup.find_all(attrs={attr: True})
    for tag in tags:
        tag['src'] = tag[attr]
    return soup


def rewrite_style_tags(soup):
    font_styles = soup.find_all('style')
    for style in font_styles:
        try:
            if 'fonts' in style['data-savepage-href']:
                style.decompose()
        except:
            pass
    return soup


def remove_head_tag(soup):
    try:
        soup.head.decompose()
    except:
        pass
    return soup


def compress_html(path):
    soup = get_html(path)

    soup = rewrite_tags_with_savepage_src(soup)
    soup = rewrite_style_tags(soup)
    soup = remove_head_tag(soup)
    soup = replace_savepage_url_in_background_image(soup)

    # Delete unused content
    soup = remove_tag_by_id(soup, 'portals')

    # Delete chat-bot
    soup = remove_tag_by_class(soup, 'popup-help')
    return str(soup)


def main():
    # rewrite_html(TEST_LESSON, 'newnew.html')
    tree = os.walk(LESSONS_PATH)
    for address, dirs, files in tree:
        for file in files:
            txt_file = file.split('.')[0] + '.txt'
            path = fr'{address}\{file}'
            new_path = fr'{address}\{txt_file}'
            try:
                compress_html(path, new_path)
                if path.split('.')[-1] == 'html':
                    os.remove(path)
            except:
                pass


if __name__ == '__main__':
    TEST_LESSON = fr'{LESSONS_PATH}\courseTwo\theme3\lesson2.txt'
    # rewrite_html(TEST_LESSON, TEST_LESSON)
    main()
