import time
from PIL import Image
from pathlib import Path
from uuid import uuid4
import os
import json

from app import app

from pathlib import Path

import pyqrcode
import pandas as pd

from datetime import datetime
import pytz


from app.models import Table, User


# Save Image and return image path
def store_picture(file):

    '''
    :param file: souce file where the input file is located - String
    :return: return the save_path as a String obj
    '''

    file_name, file_extension = os.path.splitext(file.filename)

    file_name = str(uuid4())

    full_filename = file_name + file_extension

    save_abs_path = str(Path(app.root_path) / 'static' / 'img' / full_filename)

    print(save_abs_path)

    output_size = (700, 400)
    i = Image.open(file)
    i.thumbnail(output_size)
    i.save(save_abs_path)

    return save_abs_path


def json_reader(file):

    with open(file) as f:

        data = json.load(f)

    return data[0]


def generate_qrcode(table, seat, base_url, suffix_url):

    url = f"{base_url}/{suffix_url}/{table}/{seat}"

    file_name = table + "_" + seat

    image = pyqrcode.create(url)

    save_abs_path = str(Path(app.root_path) / 'static'/ 'qrcode' / f"{file_name}.png")

    image.png(save_abs_path, scale=5)

    return f"{file_name}.png"


def activity_logger(order_id, operation_type,
                    page_name, descr,
                    status, log_time,
                    **kwargs):

    df = pd.read_csv(str(Path(app.root_path) / 'logging.csv'))

    dff = pd.DataFrame({'Order ID':[order_id],
                       'Operation': [operation_type],
                       'Page': [page_name],
                       'Description': [descr],
                       'Status': [status],
                       'Time': [log_time]})

    df = df.append(dff)

    df.to_csv(str(Path(app.root_path) / 'logging.csv'), index=False)

    return df


def qrcode2excel(tables):

    import json

    # for table_name in tables:

    import xlsxwriter

    save_abs_path = str(Path(app.root_path) / 'Downloads' / 'qrcode.xlsx')

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(save_abs_path)

    for table_name in tables:

        worksheet = workbook.add_worksheet(table_name)

        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 30)

        worksheet.write("A1", u"桌号")

        worksheet.write("B1", u"二维码")

        table = Table.query.filter_by(name=table_name).first_or_404()

        seats2qrcode = [(i.split('.')[0], i) for i in json.loads(table.container).get('qrcodes')]

        row = 2

        for items in seats2qrcode:

            img_path = str(Path(app.root_path) / 'static' / 'qrcode' / items[1])

            # Insert an image.
            worksheet.write(f'A{row}', items[0])
            worksheet.insert_image(f'B{row}',
                                    img_path)

            row += 12

    workbook.close()

    return save_abs_path


def html2pdf():

    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader('./templates'))

    template = env.get_template("info_receipt.html")

    template_vars = {"table_name": "A1",
                     "seat_number": "10"}

    html = template.render(template_vars)

    html_file = open("rest.html", "w")

    html_file.write(html)
    html_file.close()


def call2print(table_name):

    # Jinja Templating in word doc
    from docxtpl import DocxTemplate

    temp_file = str(Path(app.root_path) / 'static' / 'docx' / 'info.docx')

    abs_save_path = str(Path(app.root_path) / 'static' / 'out' / f'info_{table_name}.docx')

    doc = DocxTemplate(temp_file)
    context = dict(table_name=table_name,
                   now=str(datetime.now(tz=pytz.timezone("Europe/Berlin"))))
    doc.render(context)
    doc.save(abs_save_path)

    # Docx to PDF Conversion
    out_save_path = str(Path(app.root_path) / 'static' / 'out' / f'info_{table_name}.pdf')

    # import win32com.client as win32
    # # PDF Format Code
    # wdFormatPDF = 17
    #
    # if not Path(abs_save_path).is_file():
    #
    #     word = win32.Dispatch('Word.Application')
    #     doc = word.Documents.Open(abs_save_path)
    #     doc.SaveAs(out_save_path, FileFormat=wdFormatPDF)
    #     doc.Close()
    #     word.Quit()

    time.sleep(0.32)

    # Print the PDF info from the thermal printer
    printer_path = str(Path(app.root_path) / 'utils' / 'printer' / 'PDFtoPrinter')

    printer_name = "Star TSP100 Cutter (TSP143) eco"

    import subprocess

    subprocess.Popen(f'{printer_path} {out_save_path} "{printer_name}"', shell=True)







