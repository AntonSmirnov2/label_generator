from datetime import datetime
import os
import random
import pyqrcode
from PIL import Image, ImageDraw, ImageFont


def generate_qr(name, content: str, error='Q', scale=7, bg=(255, 255, 255, 0), qz=1):
    qr = pyqrcode.create(content, error=error)
    qr.png(name, scale=scale, background=bg, quiet_zone=qz)
    add_text_to_qr(name, name.split('.')[0])


def add_text_to_qr(qr_code: str, content):
    qr = Image.open(qr_code).convert("RGBA")
    size = (qr.size[0], qr.size[1] + qr.size[1] // 4)
    y_num = qr.size[1] + 3
    base = Image.new('RGBA', size, (0, 0, 0, 0))
    txt = Image.new('RGBA', size, (255, 255, 255, 0))
    fnt = ImageFont.truetype(font='C:\Python_Projects\label_generator\HelveticaLight.ttf', size=45)
    d = ImageDraw.Draw(txt)
    d.text((0, y_num), content, font=fnt, fill=(0, 0, 0, 255))
    base.paste(qr, mask=qr)
    out = Image.alpha_composite(base, txt)
    out.save(qr_code)


def get_label_template(templates_folder: str):
    labels = os.listdir(templates_folder)
    template_name = random.choice(labels)
    return template_name


def generate_label(templates_folder: str, label: str, qr_code: str):
    path = f'{templates_folder}\\{label}'
    base = Image.open(path).convert('RGBA')
    size = base.size
    qr_base = Image.new('RGBA', size, (0, 0, 0, 0))
    qr = Image.open(qr_code).convert('RGBA')
    qr_base.paste(qr, (110, 770))
    out = Image.alpha_composite(base, qr_base)
    out.save(qr_code)


def check_input(start_num, end_num):
    if start_num.isalpha() or end_num.isalpha():
        print('Вводить можно только числа. Перезпустите скрипт.')
        return False
    start_num = int(start_num)
    end_num = int(end_num)
    diff = end_num - start_num
    if diff <= 0:
        print('Введите сначала меньшее число, затем большее. Перезапустите скрипт.')
        return False
    return True


def main():
    print('Генератор этикеток LAPOT.SHOP запущен.\n')
    user = input('Приступаем?(y/n):')
    if user not in ('y', 'Y'):
        print('Выход.')
        exit(0)

    ct = datetime.now()
    start_num = input('Создать этикетки начиная С:')
    end_num = input('По:')
    if not check_input(start_num, end_num):
        print('Выход.')
        exit(0)
    start_num = int(start_num)
    end_num = int(end_num)
    directory = f'Result - {ct.day}-{ct.month}-{ct.year} {ct.hour}.{ct.minute}.{ct.second}'
    os.mkdir(directory)
    directory = r'C:\Python_Projects\label_generator' + '\\' + directory
    os.chdir(directory)
    for ind in range(start_num, end_num + 1):
        ind = str(ind)
        if len(ind) < 4:
            ind = '0' * (4 - len(ind)) + ind
        print(f'Создаю...{ind}')
        name = ind + '.png'
        content = ind + ' instagram.com/lapot.shop/'
        templates_folder = r'C:\Python_Projects\label_generator\back label base'

        generate_qr(name, content)
        template = get_label_template(templates_folder)
        generate_label(templates_folder, template, name)
    print(f'Выполнено! Результат работы скрипта в папке {directory}')
    pass


if __name__ == '__main__':
    main()
    # NAME = '1234.png'
    # CONTENT = '1234 instagram.com/lapot.shop/'
    # TEMPLATES_FOLDER = r'C:\Python_Projects\label_generator\back label base'
    #
    # generate_qr(NAME, CONTENT)
    # template = get_label_template(TEMPLATES_FOLDER)
    # generate_label(TEMPLATES_FOLDER, template, NAME)
