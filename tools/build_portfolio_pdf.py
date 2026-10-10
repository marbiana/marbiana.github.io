from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "Marina_Orlova_Data_Portfolio.pdf"

INK = HexColor("#17211D")
PAPER = HexColor("#F3F0E8")
ACID = HexColor("#D8FF50")
CORAL = HexColor("#FF725E")
LAVENDER = HexColor("#DFD8FF")
MUTED = HexColor("#5E6862")
WHITE = HexColor("#FFFFFF")

SITE_URL = "https://marbiana.github.io/"
GITHUB_URL = "https://github.com/marbiana"
HH_URL = "https://hh.ru/resume/faeb7065ff1050e8f40039ed1f4b384d314846"


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))


def paragraph(c, text, x, y_top, width, style, height=100 * mm):
    p = Paragraph(text, style)
    _, used = p.wrap(width, height)
    p.drawOn(c, x, y_top - used)
    return used


def rounded_box(c, x, y, w, h, fill, radius=5 * mm, stroke=None):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.7)
    else:
        c.setStrokeColor(fill)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def pill(c, text, x, y, width, fill, color=INK):
    c.setFillColor(fill)
    c.setStrokeColor(fill)
    c.roundRect(x, y, width, 6 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont("Arial-Bold", 6.8)
    c.drawCentredString(x + width / 2, y + 2.05 * mm, text)


def link(c, label, url, x, y, color=INK):
    c.setFillColor(color)
    c.setFont("Arial-Bold", 8)
    c.drawString(x, y, label)
    width = pdfmetrics.stringWidth(label, "Arial-Bold", 8)
    c.setLineWidth(0.5)
    c.line(x, y - 1.5, x + width, y - 1.5)
    c.linkURL(url, (x, y - 3, x + width, y + 10), relative=0)


def make_styles():
    return {
        "hero": ParagraphStyle(
            "hero", fontName="Arial-Bold", fontSize=28, leading=27,
            textColor=INK, spaceAfter=0, alignment=TA_LEFT,
        ),
        "intro": ParagraphStyle(
            "intro", fontName="Arial", fontSize=9.6, leading=13,
            textColor=INK,
        ),
        "case_title_light": ParagraphStyle(
            "case_title_light", fontName="Arial-Bold", fontSize=15.5,
            leading=16.5, textColor=WHITE,
        ),
        "case_title_dark": ParagraphStyle(
            "case_title_dark", fontName="Arial-Bold", fontSize=15.5,
            leading=16.5, textColor=INK,
        ),
        "body_light": ParagraphStyle(
            "body_light", fontName="Arial", fontSize=8.1, leading=10.7,
            textColor=HexColor("#E7ECE8"), bulletIndent=0,
        ),
        "body_dark": ParagraphStyle(
            "body_dark", fontName="Arial", fontSize=8.1, leading=10.7,
            textColor=INK, bulletIndent=0,
        ),
        "small": ParagraphStyle(
            "small", fontName="Arial", fontSize=7.7, leading=10.3,
            textColor=MUTED,
        ),
        "skill": ParagraphStyle(
            "skill", fontName="Arial", fontSize=8.2, leading=11.2,
            textColor=INK,
        ),
    }


def build_pdf():
    register_fonts()
    styles = make_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    width, height = A4
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("Марина Орлова - портфолио аналитика данных")
    c.setAuthor("Марина Орлова")
    c.setSubject("Портфолио: аналитика данных, e-commerce, Python, SQL и ETL")

    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    margin = 16 * mm
    content_w = width - 2 * margin

    # Header
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 7.5)
    c.drawString(margin, height - 14 * mm, "ПОРТФОЛИО / DATA ANALYTICS")
    c.setFillColor(CORAL)
    c.circle(width - margin - 2 * mm, height - 12.5 * mm, 2 * mm, fill=1, stroke=0)

    paragraph(
        c,
        "Марина Орлова<br/><font color='#FF725E'>аналитик данных</font>",
        margin,
        height - 25 * mm,
        112 * mm,
        styles["hero"],
    )
    paragraph(
        c,
        "Более четырёх лет в e-commerce. Соединяю бизнес-контекст с Python, SQL и ETL: "
        "проверяю расчёты, автоматизирую отчётность и превращаю данные в понятные решения.",
        margin,
        height - 51 * mm,
        116 * mm,
        styles["intro"],
    )

    # QR and primary link
    qr_code = qr.QrCodeWidget(SITE_URL)
    bounds = qr_code.getBounds()
    qr_size = 23 * mm
    drawing = Drawing(qr_size, qr_size, transform=[qr_size / (bounds[2] - bounds[0]), 0, 0, qr_size / (bounds[3] - bounds[1]), 0, 0])
    drawing.add(qr_code)
    renderPDF.draw(drawing, c, width - margin - qr_size, height - 51 * mm)
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 7.5)
    c.drawRightString(width - margin, height - 55 * mm, "marbiana.github.io")
    c.linkURL(SITE_URL, (width - margin - 31 * mm, height - 57 * mm, width - margin, height - 51 * mm), relative=0)

    # Signal strip
    strip_y = height - 78 * mm
    c.setStrokeColor(INK)
    c.setLineWidth(0.6)
    c.line(margin, strip_y + 12 * mm, width - margin, strip_y + 12 * mm)
    c.line(margin, strip_y, width - margin, strip_y)
    signals = [
        ("ФОКУС", "Marketplace analytics"),
        ("ИНСТРУМЕНТЫ", "Python + SQL"),
        ("ПОДХОД", "От метрики до решения"),
    ]
    col_w = content_w / 3
    for idx, (label, value) in enumerate(signals):
        x = margin + idx * col_w
        if idx:
            c.setStrokeColor(HexColor("#B5B6AE"))
            c.line(x, strip_y, x, strip_y + 12 * mm)
        c.setFillColor(MUTED)
        c.setFont("Arial-Bold", 5.7)
        c.drawString(x + (3 * mm if idx else 0), strip_y + 7.5 * mm, label)
        c.setFillColor(INK)
        c.setFont("Arial-Bold", 7.7)
        c.drawString(x + (3 * mm if idx else 0), strip_y + 3.2 * mm, value)

    c.setFillColor(INK)
    c.setFont("Arial-Bold", 6.7)
    c.drawString(margin, strip_y - 10 * mm, "01 / ИЗБРАННЫЕ КЕЙСЫ")

    # Case cards
    gap = 6 * mm
    card_w = (content_w - gap) / 2
    card_h = 76 * mm
    card_y = strip_y - 92 * mm

    rounded_box(c, margin, card_y, card_w, card_h, INK)
    rounded_box(c, margin + card_w + gap, card_y, card_w, card_h, LAVENDER, stroke=INK)

    pad = 8 * mm
    x1 = margin + pad
    x2 = margin + card_w + gap + pad
    top = card_y + card_h - pad

    c.setFillColor(ACID)
    c.setFont("Arial-Bold", 6.2)
    c.drawString(x1, top, "SUPPLY PLANNING")
    paragraph(c, "Планирование поставок на склады Wildberries", x1, top - 6 * mm, card_w - 2 * pad, styles["case_title_light"])
    paragraph(
        c,
        "История заказов + остатки + товары в пути + доступный запас продавца.<br/><br/>"
        "<b>•</b> запас в днях и целевая потребность<br/>"
        "<b>•</b> распределение по приоритетам складов<br/>"
        "<b>•</b> округление до палет и автоматические тесты",
        x1,
        top - 28 * mm,
        card_w - 2 * pad,
        styles["body_light"],
    )
    pill(c, "PYTHON", x1, card_y + 9 * mm, 18 * mm, ACID)
    pill(c, "PANDAS", x1 + 20 * mm, card_y + 9 * mm, 18 * mm, ACID)
    link(c, "Репозиторий", "https://github.com/marbiana/wb-supply-planner", x1, card_y + 4.5 * mm, WHITE)

    c.setFillColor(INK)
    c.setFont("Arial-Bold", 6.2)
    c.drawString(x2, top, "FINANCE ANALYTICS")
    paragraph(c, "Сверка финансового отчёта Wildberries", x2, top - 6 * mm, card_w - 2 * pad, styles["case_title_dark"])
    paragraph(
        c,
        "Продажи и возвраты + комиссия + логистика + хранение + удержания.<br/><br/>"
        "<b>•</b> расчёты в целых копейках<br/>"
        "<b>•</b> витрины по товарам и операциям<br/>"
        "<b>•</b> поиск расхождений и исключений",
        x2,
        top - 28 * mm,
        card_w - 2 * pad,
        styles["body_dark"],
    )
    pill(c, "PYTHON", x2, card_y + 9 * mm, 18 * mm, WHITE)
    pill(c, "SQL", x2 + 20 * mm, card_y + 9 * mm, 12 * mm, WHITE)
    link(c, "Репозиторий", "https://github.com/marbiana/wb-finance-analytics", x2, card_y + 4.5 * mm, INK)

    # Skills and experience
    lower_top = card_y - 12 * mm
    left_w = 62 * mm
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 6.7)
    c.drawString(margin, lower_top, "02 / ПРОФИЛЬ")
    paragraph(c, "Бизнес-контекст<br/>плюс техническая база", margin, lower_top - 7 * mm, left_w, ParagraphStyle(
        "lower_heading", fontName="Arial-Bold", fontSize=18, leading=18.5, textColor=INK
    ))
    paragraph(
        c,
        "Работаю с P&amp;L, юнит-экономикой, маржинальностью, оборачиваемостью, ABC/XYZ и планированием поставок.",
        margin,
        lower_top - 31 * mm,
        left_w,
        styles["small"],
    )

    skills_x = margin + left_w + 12 * mm
    skills_w = content_w - left_w - 12 * mm
    skill_rows = [
        ("АНАЛИТИКА", "P&amp;L, unit economics, ABC/XYZ, запасы, прогнозирование"),
        ("ДАННЫЕ", "Python, SQL, PostgreSQL, Pandas, API, ETL, валидация"),
        ("ИНЖЕНЕРИЯ", "Airflow, Docker, PySpark, Kafka, витрины данных"),
    ]
    row_y = lower_top
    for label, value in skill_rows:
        c.setStrokeColor(HexColor("#B5B6AE"))
        c.line(skills_x, row_y + 2 * mm, skills_x + skills_w, row_y + 2 * mm)
        c.setFillColor(INK)
        c.setFont("Arial-Bold", 6.2)
        c.drawString(skills_x, row_y - 4 * mm, label)
        paragraph(c, value, skills_x + 28 * mm, row_y, skills_w - 28 * mm, styles["skill"], 15 * mm)
        row_y -= 15 * mm

    # Contact bar
    contact_h = 31 * mm
    contact_y = 18 * mm
    rounded_box(c, margin, contact_y, content_w, contact_h, CORAL)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", 18)
    c.drawString(margin + 8 * mm, contact_y + 18 * mm, "Открыта к задачам в данных")
    c.setFont("Arial", 7.7)
    c.drawString(margin + 8 * mm, contact_y + 11 * mm, "Аналитика данных / BI-аналитика / e-commerce / ETL")
    link(c, "Сайт", SITE_URL, margin + 8 * mm, contact_y + 5.5 * mm, WHITE)
    link(c, "GitHub", GITHUB_URL, margin + 27 * mm, contact_y + 5.5 * mm, WHITE)
    link(c, "Резюме hh.ru", HH_URL, margin + 52 * mm, contact_y + 5.5 * mm, WHITE)
    c.setFillColor(WHITE)
    c.setFont("Arial", 6.5)
    c.drawRightString(width - margin - 8 * mm, contact_y + 5.5 * mm, "Публичные проекты используют синтетические данные")

    c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
