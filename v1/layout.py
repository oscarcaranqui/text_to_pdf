from v1.filter import extract_information
from pdf2image import convert_from_path
from fpdf import FPDF
import datetime
import os

user_current_directory = os.getcwd()
directory_save_path_logo_siemav = os.path.join(user_current_directory, "v1/LOGO_SIEMAV.jpg")
directory_save_path_logo_santa_priscila = os.path.join(user_current_directory, "v1/SP.jpg")
directory_path_document = os.path.join(user_current_directory, "path_of_document")
directory_path_of_images = os.path.join(user_current_directory, "path_of_images")

#Este diccionario permite agregar la piscina correspondiente unicamente a una camaronera,
pool_max_motor = {"32": "20",
                  "33": "17",
                  "35": "14",
                  "38": "14",
                  "40": "26",

                  "132": "22",
                  "133": "22",
                  "134": "21",
                  "135": "23",
                  "136": "23",
                  "137": "17"}

class DOCUMENT:

    def new_page_pdf(self):
        self.pdf.add_page()

    def save_pdf(self, name_directory):
        # name_pdf = os.path.join(directory_save_path_document, name_document)
        self.pdf.output(name=name_directory)

    def titule(self):
        self.pdf.set_font("Arial", style="", size=12)
        self.pdf.set_xy(x=110, y=10)
        self.pdf.cell(w=40, h=10, txt="REPORTE DE PISCINAS VINCULADAS", border=0, align='C', fill=False)

    def border(self, offset_x=0):
        self.pdf.rect(x=10 + offset_x, y=10, w=297-10-10, h=210-10-10)

        line_horizontal = 15
        for i in range(1, line_horizontal + 1):
            self.pdf.line(x1=10 + offset_x, y1=20 + 10*i, x2=297 - 10 + offset_x, y2=20 + 10*i)

        line_vertical = 30
        for i in range(1, line_vertical + 2):
            self.pdf.line(x1=22 + 8*i + offset_x, y1=40, x2=22 + 8*i + offset_x, y2=170)

    def name_motor(self, offset_x=0):
        self.pdf.set_font("Arial", style="", size=8)
        max_account = 30
        for index, i in enumerate(range(1,max_account + 1), start=1):
            self.pdf.set_xy(x=22 + 8* i + offset_x, y=30)
            self.pdf.set_fill_color(255, 160, 122)
            self.pdf.cell(w=8, h=10, txt="M" + str(index), border=1, align='C', fill=True)

    def sector(self, offset_x=0, name_sector=str()):
        self.pdf.set_font("Arial", style="", size=10)
        self.pdf.set_xy(x=10 + offset_x, y=10)
        self.pdf.cell(w=20, h=10, txt=name_sector.upper(), align='L')

    def ip(self, offset_x=0, ip=str()):
        self.pdf.set_font("Arial", style="", size=10)
        self.pdf.set_xy(x=10 + offset_x, y=20)
        self.pdf.cell(w=20, h=10, txt=ip, align='L')

    def logos(self, offset_x=0):
        siemav = directory_save_path_logo_siemav
        self.pdf.image(siemav, x=267.5 + offset_x, y=10.5, w=17, h=17)
        santa_priscila = directory_save_path_logo_santa_priscila
        self.pdf.image(santa_priscila, x=245 + offset_x, y=10.5, w=19, h=19)

    def info_color(self, offset_x=0):
        self.pdf.set_xy(x=10 + offset_x, y=180)
        self.pdf.set_fill_color(240, 230, 140)
        self.pdf.cell(w=8, h=-10, txt="NO", border=1, align='C', fill=True)
        self.pdf.set_xy(x=20 + offset_x, y=179)
        self.pdf.cell(w=20, h=10, txt="Este cuadro significa que se encuentra vinculado", align='L')

        self.pdf.set_xy(x=10 + offset_x, y=180)
        self.pdf.set_fill_color(60, 179, 113)
        self.pdf.cell(w=8, h=9, txt="OK", border=1, align='C', fill=True)
        self.pdf.set_xy(x=20 + offset_x, y=170)
        self.pdf.cell(w=20, h=10, txt="Este cuadro significa que NO se encuentra vinculado", align='L')

    def fill_locker(self, pool_received):
        self.pdf.set_font("Arial", style="", size=8)
        same_keys = pool_received.keys() & pool_max_motor.keys()
        sorted_same_keys = sorted(list(same_keys))
        for index, key in enumerate(sorted_same_keys):
            current_motor_pool = pool_received[key]

            self.pdf.set_xy(x=10, y=40 + index * 10 )
            self.pdf.set_fill_color(100, 149, 237)
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
                self.pdf.cell(w=8, h=10, txt="NO", border=1, align='C', fill=True)

    def create_document(self, name_directory, current_dictionary, name_sector, ip):
        self.pdf = FPDF(orientation="L", format="A4", unit="mm")
        self.new_page_pdf()
        self.titule()
        self.border(offset_x=0)
        self.name_motor(offset_x=0)
        self.sector(offset_x=0, name_sector=name_sector)
        self.ip(offset_x=0, ip=ip)
        self.fill_locker(pool_received=current_dictionary)
        self.logos(offset_x=0)
        self.info_color(offset_x=0)
        self.save_pdf(name_directory=name_directory)

    def create_name_directory(self):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%d_%m_%Y__%H_%M_%S")
        name_file = formatted_date + ".pdf"
        directory_save_path_document_without_ext = formatted_date
        directory_save_path_document_pdf = os.path.join(directory_path_document, name_file)
        return [directory_save_path_document_pdf, directory_save_path_document_without_ext]

    def write_pdf(self, sentence: str):
        response = extract_information(sentence)
        if response[0]:
            data = response[1]
            self.create_document(name_directory=self.create_name_directory()[0],
                                 current_dictionary=data,
                                 ip=response[2],
                                 name_sector=response[3]
                                 )

            pages = convert_from_path(self.create_name_directory()[0],
                                      poppler_path=r'C:\Users\oscarcaranqui\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin')
            directory_save_image = os.path.join(directory_path_of_images, self.create_name_directory()[1])
            pages[0].save(directory_save_image + '.jpg', 'JPEG')
            return directory_save_image
        else:
            return sentence

