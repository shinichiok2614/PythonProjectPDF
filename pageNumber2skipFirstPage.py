import fitz  # PyMuPDF

# ================= CONFIG =================
INPUT_PDF = "merge_output.pdf"
OUTPUT_PDF = "output_page_numbered.pdf"

SKIP_FIRST_PAGES = 3      # ❗ bỏ bao nhiêu trang đầu
START_PAGE_NUMBER = 1    # số bắt đầu sau khi bỏ

FONT_SIZE = 12

# Vị trí số trang mới
RIGHT_MARGIN = 70
BOTTOM_MARGIN = 60

# Vùng che số trang cũ (góc dưới phải)
COVER_WIDTH = 120
COVER_HEIGHT = 70
# =========================================

doc = fitz.open(INPUT_PDF)
page_number = START_PAGE_NUMBER

for i, page in enumerate(doc):
    # 👉 BỎ QUA CÁC TRANG ĐẦU
    if i < SKIP_FIRST_PAGES:
        continue

    width = page.rect.width
    height = page.rect.height

    # ===== 1. CHE SỐ TRANG CŨ =====
    cover_rect = fitz.Rect(
        width - COVER_WIDTH,
        height - COVER_HEIGHT,
        width,
        height
    )

    page.draw_rect(
        cover_rect,
        fill=(1, 1, 1),
        color=None,
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

print("✅ Hoàn tất! File:", OUTPUT_PDF)
