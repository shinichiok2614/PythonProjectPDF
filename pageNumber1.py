# pip install pymupdf

import fitz  # PyMuPDF

# =============== CONFIG =================
INPUT_PDF = "nkls1820.pdf"
OUTPUT_PDF = "output_page_numbered.pdf"

START_PAGE_NUMBER = 1
FONT_SIZE = 12

# Khoảng cách số trang tới mép trang (điểm PDF)
RIGHT_MARGIN = 40
BOTTOM_MARGIN = 30

# Vùng che số trang cũ
COVER_WIDTH = 120
COVER_HEIGHT = 40
# ========================================

doc = fitz.open(INPUT_PDF)
page_number = START_PAGE_NUMBER

for page in doc:
    width = page.rect.width
    height = page.rect.height

    # ===== 1. CHE SỐ TRANG CŨ (GÓC PHẢI DƯỚI) =====
    cover_rect = fitz.Rect(
        width - COVER_WIDTH,
        height - COVER_HEIGHT,
        width,
        height
    )

    page.draw_rect(
        cover_rect,
        fill=(1, 1, 1),  # trắng
        overlay=True
    )

    # ===== 2. ĐÁNH SỐ TRANG MỚI =====
    text = str(page_number)
    text_width = fitz.get_text_length(text, fontsize=FONT_SIZE)

    x = width - RIGHT_MARGIN - text_width
    y = height - BOTTOM_MARGIN

    page.insert_text(
        (x, y),
        text,
        fontsize=FONT_SIZE,
        color=(0, 0, 0)
    )

    page_number += 1

doc.save(OUTPUT_PDF)
doc.close()

print("✅ Xong! File đã lưu:", OUTPUT_PDF)
