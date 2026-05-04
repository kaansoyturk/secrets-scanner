from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

# Renkler
RED = HexColor("#f85149")
GREEN = HexColor("#3fb950")
BLUE = HexColor("#58a6ff")
DARK = HexColor("#0d1117")
GRAY = HexColor("#8b949e")
LIGHT_GRAY = HexColor("#161b22")

# Türkçe font kaydı
font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("Arial", font_path))
    FONT = "Arial"
else:
    FONT = "Helvetica"

def generate_report(findings, scanned_files, output_path="scan_report.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontSize=24,
        textColor=BLUE,
        spaceAfter=10,
        fontName=FONT
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=GRAY,
        spaceAfter=20,
        fontName=FONT
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontSize=14,
        textColor=BLUE,
        spaceBefore=20,
        spaceAfter=10,
        fontName=FONT
    )

    normal_style = ParagraphStyle(
        "Normal2",
        parent=styles["Normal"],
        fontSize=10,
        textColor=black,
        spaceAfter=5,
        fontName=FONT
    )

    elements.append(Paragraph("Secrets Scanner", title_style))
    elements.append(Paragraph(
        f"Tarama Raporu — {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        subtitle_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    summary_data = [
        ["Taranan Dosya", "Bulunan Secret", "Tarih"],
        [
            str(scanned_files),
            str(len(findings)),
            datetime.now().strftime("%d.%m.%Y")
        ]
    ]

    summary_table = Table(summary_data, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), BLUE),
        ("FONTNAME", (0, 0), (-1, 0), FONT),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GRAY),
        ("TEXTCOLOR", (0, 1), (-1, -1), white),
        ("FONTNAME", (0, 1), (-1, -1), FONT),
        ("FONTSIZE", (0, 1), (-1, -1), 12),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWHEIGHT", (0, 0), (-1, -1), 0.8*cm),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 0.5*cm))

    if findings:
        elements.append(Paragraph("Bulunan Secretlar", section_style))

        table_data = [["Tur", "Dosya", "Satir", "Icerik"]]

        for f in findings:
            filepath = f["file"]
            if len(filepath) > 30:
                filepath = "..." + filepath[-27:]

            content = f["content"]
            if len(content) > 40:
                content = content[:37] + "..."

            table_data.append([
                f["type"],
                filepath,
                str(f["line"]),
                content
            ])

        findings_table = Table(
            table_data,
            colWidths=[4*cm, 4.5*cm, 1.5*cm, 6.5*cm]
        )
        findings_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), BLUE),
            ("FONTNAME", (0, 0), (-1, 0), FONT),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f6f8fa")]),
            ("TEXTCOLOR", (0, 1), (0, -1), RED),
            ("FONTNAME", (0, 1), (-1, -1), FONT),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ALIGN", (2, 0), (2, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWHEIGHT", (0, 0), (-1, -1), 0.7*cm),
            ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
        ]))

        elements.append(findings_table)

    elements.append(Paragraph("Oneriler", section_style))
    recommendations = [
        "• Bulunan secretlari hemen gecersiz kilin ve yenilerini olusturun.",
        "• Secretlari kod icine yazmak yerine .env dosyasi kullanin.",
        "• .env dosyasini .gitignore'a ekleyin.",
        "• python-dotenv kutuphanesiyle environment variable kullanin.",
        "• Git gecmisindeki secretlari temizlemek icin git-filter-repo kullanin.",
    ]
    for rec in recommendations:
        elements.append(Paragraph(rec, normal_style))

    elements.append(Spacer(1, 1*cm))
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=GRAY,
        alignment=1,
        fontName=FONT
    )
    elements.append(Paragraph(
        "Secrets Scanner — github.com/kaansoyturk/secrets-scanner",
        footer_style
    ))

    doc.build(elements)
    print(f"PDF rapor olusturuldu: {output_path}")
    return output_path