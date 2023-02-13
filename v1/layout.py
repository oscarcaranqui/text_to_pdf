from v1.filter import extract_information
from fpdf import FPDF
import qrcode
import time
import os

user_current_directory = os.getcwd()
path_qr = os.path.join(user_current_directory, "path_of_qr")
directory_save_path_logo = os.path.join(user_current_directory, "v1/LOGO_SIEMAV.jpg")
directory_save_path_document = os.path.join(user_current_directory, "path_of_document")

pool_max_motor = {"132": "22", "133": "22", "134": "21", "136": "23", "137": "20"}


class DOCUMENT:

    def new_page_pdf(self):
        self.pdf.add_page()

    def save_pdf(self, name_document):
        name_pdf = os.path.join(directory_save_path_document, name_document)
        self.pdf.output(name=name_pdf)

    def border(self, offset_x=0):
        self.pdf.rect(x=10 + offset_x, y=10, w=297-10-10, h=210-10-10)
        line_horizontal = 17
        for i in range(1, line_horizontal + 1):
            self.pdf.line(x1=10 + offset_x, y1=20 + 10*i, x2=297 - 10 + offset_x, y2=20 + 10*i)

        line_vertical = 30
        for i in range(1, line_vertical + 2):
            self.pdf.line(x1=22 + 8*i + offset_x, y1=40, x2=22 + 8*i + offset_x, y2=200)

    def name_motor(self, offset_x=0):
        self.pdf.set_font("Arial", style="", size=8)
        max_account = 30
        for index, i in enumerate(range(1,max_account + 1), start=1):
            self.pdf.set_xy(x=22 + 8* i + offset_x, y=30)
            self.pdf.set_fill_color(255, 160, 122)
            self.pdf.cell(w=8, h=10, txt="M" + str(index), border=1, align='C', fill=True)

    def sector(self, offset_x=0):
        self.pdf.set_font("Arial", style="", size=10)
        self.pdf.set_xy(x=10 + offset_x, y=10)
        self.pdf.cell(w=20, h=10, txt="TAURA4", align='L')

    def fill_locker(self, pool_received):
        self.pdf.set_font("Arial", style="", size=8)
        same_keys = pool_received.keys() & pool_max_motor.keys()
        sorted_same_keys = sorted(list(same_keys))
        for index, key in enumerate(sorted_same_keys):
            current_motor_pool = pool_received[key]

            self.pdf.set_xy(x=10, y=40 + index * 10 )
            self.pdf.set_fill_color( 100, 149, 237)
            self.pdf.cell(w=20, h=10, txt="Piscina " + str(key), border=1, align='C', fill=True)

            max_motor = list(range(1, int(pool_max_motor[key]) + 1))
            current_motor_pool = set(current_motor_pool)
            list_motor_no_add = [num for num in max_motor if num not in current_motor_pool]

            for number_motor in current_motor_pool:
                self.pdf.set_xy(x=22 + 8 * number_motor, y=40 + 10 * index)
                self.pdf.set_fill_color(60, 179, 113)
                self.pdf.cell(w=8, h=10, txt="OK", border=1, align='C', fill=True)

            for motor_no_add in list_motor_no_add:
                self.pdf.set_xy(x=22 + 8 * motor_no_add, y=40 + 10 * index)
                self.pdf.set_fill_color(240, 230, 140)
                self.pdf.cell(w=8, h=10, txt="No", border=1, align='C', fill=True)

    def create_document(self, save_name, current_dictionary):
        self.pdf = FPDF(orientation="L", format="A4", unit="mm")
        self.new_page_pdf()
        self.border(offset_x=0)
        self.name_motor(offset_x=0)
        self.sector(offset_x=0)
        self.fill_locker(pool_received=current_dictionary)
        self.save_pdf(name_document=save_name)

    def write_pdf(self, sentence: str):
        response = extract_information(sentence)
        print(response)
        self.create_document(save_name="PRUEBA.pdf", current_dictionary=response)
