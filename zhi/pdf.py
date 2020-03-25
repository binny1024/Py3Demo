import sys
from imp import reload

import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader

if sys.getdefaultencoding() != 'utf-8':  # python2环境不是utf-8编码，需要设定默认编码
    reload(sys)
    sys.setdefaultencoding('utf-8')


def add_watermark(input_str, output_pdf, watermark_pdf):
    user_name = "123456"  # 页脚文本
    options = {
        'margin-top': '0.75in',  # 页面上边距
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'minimum-font-size': '30',  # 页面字体大小
        'footer-right': user_name,  # 右页脚设定文本
        'footer-font-size': '20',
        'encoding': "UTF-8"  # 设定生成pdf文件为utf-8编码，避免生成pdf中文乱码
    }
    res = pdfkit.from_string(input_str, './out.pdf', options=options)
    if not res:
        return 0
    watermark = PdfFileReader(watermark_pdf)  # 本地水印文件
    watermark_page = watermark.getPage(0)
    pdf = PdfFileReader('/Users/Desktop/out.pdf')  # 本地生成不带水印的pdf文件
    pdf_writer = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        pdf_page = pdf.getPage(page)
        pdf_page.mergePage(watermark_page)
        pdf_writer.addPage(pdf_page)
    pdf_writer.write(open(output_pdf, 'wb'))  # 本地生成带水印的pdf文件


if __name__ == '__main__':
    add_watermark("""
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;今天，老师宣布了期中考试前十名。我紧张极了。因为我做为中队委；做为老师眼中的好学生；做为妈妈的乖女儿，如果没有进前十，那脸就丢尽了！
    老师的话语刚刚响起，我的心就开始狂跳个不停。同学们都坐得笔直，唯独我的手在抖、脚在不安地踢着地面。一个、两个……许多同学都被念到了，还是没有我。环顾四周，被念到的同学红光满面，没有被点到的，也只能坐着干着急。而我，心已经跳到了嗓子眼：我该怎么办啊？！真希望我的名字不要在名单中“离家出走”。天气虽然很冷，我的脑门上却渗出了一层密密的汗珠
    """, "rwps.pdf", "water.pdf")
