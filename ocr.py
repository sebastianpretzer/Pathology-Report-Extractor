from wand.image import Image as WImage
from PIL import ImageEnhance, ImageFilter
from PIL import Image as Img
Img.MAX_IMAGE_PIXELS = 1000000000
import pytesseract
from PyPDF2 import PdfFileReader
import os
import glob
from time import gmtime, strftime


#filename = "./GDC/0a0ff4de-0473-4b56-99e8-5faa4b2b0cd0/TCGA-US-A776.A34AB133-F144-42E4-AC61-505B8DA9554F.pdf"


def run(pathname):
    total_folders = len(get_folders(pathname))
    for i, folder in enumerate(get_folders(pathname)):
        pdf_path_list = get_pdf_path(folder)
        if len(pdf_path_list) == 1:
            print(str(i) + '/' + str(total_folders) + ' - ' + strftime("%H:%M:%S", gmtime()) +
                  ' - ' + pdf_path_list[0])
            if not check_text_file(pdf_path_list[0]):
                save_text(pdf_path_list[0], get_pdf_text(pdf_path_list[0]))


def get_folders(pathname):
    return [x[0] for x in os.walk(pathname)]


def get_pdf_path(pathname):
    return glob.glob(pathname + '/*.pdf')


def countPages(filename):
    pdf = PdfFileReader(open(filename, 'rb'))
    return pdf.getNumPages()


def get_pdf_text(filename):
    index = countPages(filename)
    text = ''
    for i in range(0, index):
        text += ('---Page ' + str(i + 1) + '---\n') + \
            get_text(filename, i) + '\n\n--- ---\n\n'

    return text


def get_text(filename, index=0):
    image_file = open("sample.jpeg", "wb")
    with WImage(filename=filename + "[{}]".format(index), resolution=400) as img:
        image_jpeg = img.convert('jpeg')
        image_jpeg.save(filename=image_file.name)
    image_file.close()

    im = Img.open("sample.jpeg")
    im = im.filter(ImageFilter.MedianFilter())

    enhancer = ImageEnhance.Contrast(im)

    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save('sample.jpeg')

    text = pytesseract.image_to_string(Img.open('sample.jpeg'))

    return text


def check_text_file(filename):
    temp_text_file = filename.replace('.pdf', '.txt')
    return os.path.isfile(temp_text_file)


def save_text(filename, text):
    save_path = filename.replace('.pdf', '.txt')
    text_file = open(save_path, "w")
    text_file.write(text)
    text_file.close()


run('./GDC/')
