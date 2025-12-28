# Sửa số trang PDF

**User:** shinichiok kudo (phuonghoangit2614@gmail.com)  
**Created:** 12/28/2025 14:33:09  
**Updated:** 12/28/2025 14:54:24  
**Exported:** 12/28/2025 15:24:57  
**Link:** [https://chatgpt.com/c/6950dd28-69b8-8320-a1fc-7547da6aaaf3](https://chatgpt.com/c/6950dd28-69b8-8320-a1fc-7547da6aaaf3)  

## Response:
Khi **PDF bị đánh số trang sai**, cách sửa sẽ **phụ thuộc vào nguyên nhân** (sai số hiển thị hay sai số thực). Mình tóm lại **các trường hợp thường gặp + cách xử lý cụ thể** để bạn làm nhanh nhé 👇

* * *

1️⃣ PDF **hiển thị số trang sai** (ví dụ: bìa là trang 1 nhưng thực tế muốn là trang 0 / i)
-------------------------------------------------------------------------------------------

👉 **Đây là lỗi phổ biến nhất**, file vẫn đúng nhưng **Page Labels** sai.

### 🔧 Cách sửa bằng **Adobe Acrobat Pro**

1.  Mở PDF → **Tools** → **Organize Pages**
2.  Nhấn **More (⋯)** → **Page Labels**
3.  Chọn **Page Range** (ví dụ từ trang 2)
4.  Chọn kiểu:
    *   i, ii, iii (La Mã)
    *   1, 2, 3 (số thường)
5.  Đặt **Start at** đúng số bạn muốn
6.  OK → Save

✅ Không ảnh hưởng nội dung, chỉ sửa số trang hiển thị

* * *

2️⃣ PDF bị **chèn số trang trực tiếp sai** (số nằm trong nội dung)
------------------------------------------------------------------

👉 Trường hợp này **số trang đã được in cứng vào trang**, không phải page label.

### 🔧 Cách sửa (chuẩn nhất)

**Xóa & đánh số lại**

1.  Dùng **Edit PDF** (Acrobat Pro)
2.  Xóa số trang cũ
3.  Vào **Header & Footer → Add**
4.  Đánh số trang lại từ số đúng

⛔ Không sửa được nếu PDF là ảnh scan (xem mục 4)

* * *

3️⃣ PDF mở trong Premiere / Word / trình đọc khác thấy số trang lệch
--------------------------------------------------------------------

👉 Đây là do **phần mềm đếm trang vật lý**, không theo page label.

### ✅ Giải pháp

*   Sửa lại **Page Labels** (mục 1)
*   Hoặc chấp nhận lệch khi import (Premiere thường bị)

* * *

4️⃣ PDF scan (toàn bộ là ảnh)
-----------------------------

👉 Không thể sửa trực tiếp số trang.

### 🔧 Cách xử lý

1.  Dùng **OCR** (Acrobat / ABBYY)
2.  Xóa số cũ
3.  Đánh số lại bằng Header & Footer

* * *

5️⃣ Muốn **đánh lại toàn bộ số trang tự động**
----------------------------------------------

### 🔧 Acrobat Pro

*   Tools → **Edit PDF**
*   Header & Footer → **Add**
*   Insert Page Number
*   Chọn vị trí, font, bắt đầu từ số bất kỳ

* * *

6️⃣ Không có Acrobat Pro (giải pháp miễn phí)
---------------------------------------------

### 🆓 Dùng **PDF-XChange Editor**

*   Page Labels (miễn phí)
*   Header & Footer (bản free có watermark nhẹ)

### 🆓 Online (nhanh nhưng hạn chế)

*   iLovePDF
*   SmallPDF  
    ⚠️ Không nên dùng nếu file quan trọng / bảo mật

* * *

🔍 Mình hỏi nhanh để hướng dẫn đúng nhất:
-----------------------------------------

1.  PDF của bạn:
    *   📄 File gốc Word/InDesign?
    *   🖼️ Hay PDF scan?
2.  Sai kiểu:
    *   Hiển thị trong thanh trang?
    *   Hay số in trên trang?
3.  Bạn đang dùng:
    *   Adobe Acrobat Pro
    *   Hay phần mềm khác?

Chỉ cần trả lời 1–2 ý, mình sẽ chỉ **đúng cách + đúng công cụ** cho bạn luôn 👍

## Response:
OK 👍 mình đưa **code Python hoàn chỉnh** để:

✅ **Che (xóa/đè) số trang cũ**  
✅ **Đánh số trang mới theo thứ tự**  
✅ Áp dụng cho **PDF thường (không phải scan)**  
👉 Cách này **không cần Acrobat**, chạy offline

* * *

🔧 Cách làm chuẩn & dễ nhất: **Python + PyMuPDF (fitz)**
========================================================

1️⃣ Cài thư viện
----------------

```bash
pip install pymupdf
```

* * *

2️⃣ Nguyên lý
-------------

*   Vẽ **hình chữ nhật màu trắng** để che số trang cũ
*   Ghi **số trang mới** đúng vị trí bạn muốn
*   Bắt đầu từ số bất kỳ (ví dụ từ 1)

* * *

3️⃣ Code hoàn chỉnh
-------------------

```python
import fitz  # PyMuPDF

# ================== CONFIG ==================
INPUT_PDF = "input.pdf"
OUTPUT_PDF = "output_renumbered.pdf"

START_PAGE_NUMBER = 1   # bắt đầu đánh số từ
FONT_SIZE = 12

# Vị trí số trang mới (tính theo điểm PDF)
NEW_NUMBER_Y_OFFSET = 30   # cách đáy trang (px)

# Vùng che số trang cũ (tùy file, chỉnh lại nếu cần)
OLD_NUMBER_RECT_HEIGHT = 40  # chiều cao vùng che
# ===========================================

doc = fitz.open(INPUT_PDF)

page_number = START_PAGE_NUMBER

for page in doc:
    width = page.rect.width
    height = page.rect.height

    # ===== 1. CHE SỐ TRANG CŨ =====
    cover_rect = fitz.Rect(
        0,
        height - OLD_NUMBER_RECT_HEIGHT,
        width,
        height
    )

    page.draw_rect(
        cover_rect,
        fill=(1, 1, 1),  # màu trắng
        overlay=True
    )

    # ===== 2. ĐÁNH SỐ TRANG MỚI =====
    text = str(page_number)
    text_width = fitz.get_text_length(text, fontsize=FONT_SIZE)

    x = (width - text_width) / 2
    y = height - NEW_NUMBER_Y_OFFSET

    page.insert_text(
        (x, y),
        text,
        fontsize=FONT_SIZE,
        color=(0, 0, 0)
    )

    page_number += 1

doc.save(OUTPUT_PDF)
doc.close()

print("✅ Hoàn tất! File đã lưu:", OUTPUT_PDF)
```

* * *

4️⃣ Điều chỉnh cho đúng file của bạn
------------------------------------

### 📍 Nếu số trang cũ nằm:

*   **Giữa đáy trang** → OK như code trên
*   **Góc phải** → thu hẹp vùng che:

```python
cover_rect = fitz.Rect(
    width - 150,
    height - 40,
    width,
    height
)
```

### 📍 Đổi vị trí số trang mới

*   **Góc phải dưới**

```python
x = width - 60
```

*   **Góc trái**

```python
x = 30
```

* * *

5️⃣ Nếu PDF là **scan (ảnh)** ❗
-------------------------------

Code trên **vẫn chạy được**, nhưng:

*   Chỉ che được bằng màu trắng
*   Không xóa chính xác số nếu nền không trắng

👉 Giải pháp chuẩn:

*   OCR trước (Acrobat / ABBYY)
*   Hoặc mình viết thêm code **tự động nhận vị trí số trang** cho bạn

* * *

🔥 Bạn cho mình biết thêm:
--------------------------

1️⃣ Số trang cũ nằm **giữa / trái / phải**?  
2️⃣ PDF là **scan hay text**?  
3️⃣ Muốn bắt đầu từ **số mấy**?

Mình sẽ chỉnh code **chuẩn 100% cho file của bạn** 👌

## Response:
OK 👍 **số trang ở góc dưới bên phải** thì mình chỉnh lại **code đúng vị trí đó** luôn cho bạn.

Dưới đây là **code Python hoàn chỉnh**:

✅ Che số trang cũ **góc dưới phải**  
✅ Đánh số trang mới **góc dưới phải**  
✅ Khoảng cách đẹp, dễ chỉnh  
✅ Không cần Acrobat

* * *

🔧 Python – Che số cũ & đánh số mới (góc dưới phải)
===================================================

1️⃣ Cài thư viện
----------------

```bash
pip install pymupdf
```

* * *

2️⃣ Code hoàn chỉnh
-------------------

```python
import fitz  # PyMuPDF

# =============== CONFIG =================
INPUT_PDF = "input.pdf"
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
```

* * *

3️⃣ Chỉnh cho khớp 100% file của bạn
------------------------------------

### 📌 Nếu số cũ **cao hơn/thấp hơn**

```python
COVER_HEIGHT = 50   # tăng nếu chưa che hết
BOTTOM_MARGIN = 35
```

### 📌 Nếu số cũ **sát mép phải hơn**

```python
COVER_WIDTH = 150
RIGHT_MARGIN = 30
```

* * *

4️⃣ Lưu ý quan trọng
--------------------

*   PDF **text thường** → kết quả đẹp
*   PDF **scan ảnh** → chỉ che được, không xóa thật
*   Nền không trắng → cần đổi màu `fill=(r,g,b)`

* * *

🔥 Nếu bạn muốn nâng cấp:
-------------------------

*   Bỏ qua trang bìa
*   Đánh số từ trang X
*   Font khác / in đậm
*   Tự động dò vị trí số cũ

👉 Cứ nói yêu cầu, mình chỉnh code cho đúng nhu cầu của bạn luôn 💪

## Response:
OK 👍 yêu cầu này rất chuẩn trong thực tế (bỏ bìa, mục lục…).

Dưới đây là **code Python đã chỉnh** để:

✅ **Bỏ N trang đầu không đánh số**  
✅ **Chỉ đánh số từ trang kế tiếp**  
✅ **Số trang ở góc dưới bên phải**  
✅ **Che số cũ + đánh số mới**

* * *

🔧 Python – Bỏ trang đầu & đánh số từ trang X
=============================================

1️⃣ Cài thư viện
----------------

```bash
pip install pymupdf
```

* * *

2️⃣ Code hoàn chỉnh
-------------------

```python
import fitz  # PyMuPDF

# ================= CONFIG =================
INPUT_PDF = "input.pdf"
OUTPUT_PDF = "output_page_numbered.pdf"

SKIP_FIRST_PAGES = 2      # ❗ bỏ bao nhiêu trang đầu
START_PAGE_NUMBER = 1    # số bắt đầu sau khi bỏ

FONT_SIZE = 12

# Vị trí số trang mới
RIGHT_MARGIN = 40
BOTTOM_MARGIN = 30

# Vùng che số trang cũ (góc dưới phải)
COVER_WIDTH = 120
COVER_HEIGHT = 40
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
```

* * *

3️⃣ Ví dụ sử dụng nhanh
-----------------------

| Trường hợp | Giá trị |
| --- | --- |
| Bỏ bìa | `SKIP_FIRST_PAGES = 1` |
| Bỏ bìa + mục lục | `SKIP_FIRST_PAGES = 2` |
| Trang 5 mới là trang 1 | `SKIP_FIRST_PAGES = 4` |

* * *

4️⃣ Nếu bạn muốn **không che số cũ ở các trang bỏ qua**
-------------------------------------------------------

👉 Code hiện tại **đã đúng**:

*   Trang bị bỏ → **không che, không đánh số**
*   Trang bắt đầu → che + đánh số

* * *

🔥 Nâng cấp thêm (nếu cần)
--------------------------

*   Trang đầu đánh **i, ii, iii**
*   Chỉ che nếu phát hiện có số cũ
*   Font khác / in đậm
*   Chỉ đánh số trang lẻ / chẵn

👉 Nói yêu cầu, mình chỉnh tiếp cho bạn luôn 👌

## Response:
Mình giải thích **từng dòng, đúng ngữ cảnh PDF** để bạn **nhìn là hiểu ngay**, không mơ hồ 👇

* * *

1️⃣ `fitz.Rect(...)` là gì?
---------------------------

```python
cover_rect = fitz.Rect(x0, y0, x1, y1)
```

👉 Đây là **hình chữ nhật** trong hệ tọa độ PDF:

```
(x0, y0) ┌────────────┐
         │            │
         │  RECT      │
         │            │
         └────────────┘ (x1, y1)
```

📌 **Hệ tọa độ PDF (PyMuPDF)**:

*   (0, 0) → **góc trên bên trái**
*   x tăng → sang phải
*   y tăng → xuống dưới

* * *

2️⃣ Phân tích từng tham số
--------------------------

```python
cover_rect = fitz.Rect(
    width - COVER_WIDTH,    # x0
    height - COVER_HEIGHT,  # y0
    width,                  # x1
    height                  # y1
)
```

### 🔹 `width`

*   Chiều rộng trang PDF

### 🔹 `height`

*   Chiều cao trang PDF

* * *

### 🔹 `width - COVER_WIDTH` → **x0**

👉 Điểm bắt đầu **từ bên trái** của vùng che

Ví dụ:

*   Trang rộng 595px
*   `COVER_WIDTH = 120`

→ `x0 = 595 - 120 = 475`

➡️ Vùng che rộng 120px, nằm sát **mép phải**

* * *

### 🔹 `height - COVER_HEIGHT` → **y0**

👉 Điểm bắt đầu **từ phía trên** của vùng che

Ví dụ:

*   Trang cao 842px
*   `COVER_HEIGHT = 40`

→ `y0 = 842 - 40 = 802`

➡️ Vùng che cao 40px, nằm sát **mép dưới**

* * *

### 🔹 `width, height` → **x1, y1**

👉 Góc **dưới bên phải** trang

* * *

📌 Kết quả trực quan
--------------------

```text
┌──────────────────────────────┐
│                              │
│                              │
│                              │
│                              │
│                    ██████████│ ← vùng che số cũ
│                    ██████████│
└──────────────────────────────┘
```

➡️ Hình chữ nhật **góc dưới bên phải**, đúng vị trí số trang cũ

* * *

3️⃣ `page.draw_rect(...)` làm gì?
---------------------------------

```python
page.draw_rect(
    cover_rect,
    fill=(1, 1, 1),
    overlay=True
)
```

### 🔹 `cover_rect`

👉 Vùng cần vẽ (hình chữ nhật vừa tạo)

* * *

### 🔹 `fill=(1, 1, 1)`

👉 **Màu tô** (RGB chuẩn PDF)

| Giá trị | Màu |
| --- | --- |
| (1,1,1) | Trắng |
| (0,0,0) | Đen |
| (1,0,0) | Đỏ |

➡️ Ta dùng **trắng** để **che số trang cũ**

* * *

### 🔹 `overlay=True` (RẤT QUAN TRỌNG)

👉 Vẽ **lên trên nội dung cũ**

| overlay | Kết quả |
| --- | --- |
| `True` | Che nội dung bên dưới ✅ |
| `False` | Vẽ phía dưới → **không che được** ❌ |

* * *

4️⃣ Tóm tắt ngắn gọn
--------------------

> Đoạn code này:
> 
> *   Tạo **một hình chữ nhật ở góc dưới bên phải**
> *   Tô **màu trắng**
> *   Vẽ **đè lên nội dung cũ**  
>     → Mục đích: **che số trang cũ**
>     

* * *

5️⃣ Mẹo chỉnh nhanh
-------------------

### 📌 Che rộng hơn

```python
COVER_WIDTH = 160
```

### 📌 Che cao hơn

```python
COVER_HEIGHT = 60
```

### 📌 Nền không trắng

```python
fill=(0.95, 0.95, 0.95)
```

* * *

Nếu bạn muốn, mình có thể:

*   Vẽ **viền debug** để thấy rõ vùng che
*   Tự động dò vị trí số trang cũ
*   Giải thích tiếp phần `insert_text`

👉 Cứ nói tiếp nhé 👌

## Response:
Câu này hỏi **rất đúng chỗ** 👍  
Mặc định bạn **chỉ tô nền trắng**, **không vẽ viền**, nên **không có viền trắng hay viền gì cả**.

Giải thích + cách làm chi tiết như sau 👇

* * *

1️⃣ Vì sao bạn **không thấy viền**?
-----------------------------------

Code hiện tại:

```python
page.draw_rect(
    cover_rect,
    fill=(1, 1, 1),
    overlay=True
)
```

📌 Ở đây:

*   `fill=(1,1,1)` → **tô nền trắng**
*   ❌ **Không truyền `color`** → **không vẽ viền**

➡️ Kết quả:  
**Chỉ có một mảng trắng**, không có đường viền bao quanh.

* * *

2️⃣ Nếu muốn **viền cũng màu trắng**
------------------------------------

```python
page.draw_rect(
    cover_rect,
    fill=(1, 1, 1),      # nền trắng
    color=(1, 1, 1),     # viền trắng
    width=1,             # độ dày viền
    overlay=True
)
```

⚠️ Lưu ý:

*   Viền trắng **trùng màu nền** → **mắt thường gần như không thấy**
*   Chỉ có tác dụng khi **debug** hoặc khi nền không hoàn toàn trắng

* * *

3️⃣ Nếu muốn **có viền để debug (rất nên dùng lúc test)**
---------------------------------------------------------

```python
page.draw_rect(
    cover_rect,
    fill=(1, 1, 1),
    color=(1, 0, 0),   # viền đỏ
    width=1,
    overlay=True
)
```

📌 Dùng cách này để:

*   Nhìn rõ vùng che
*   Canh lại `COVER_WIDTH`, `COVER_HEIGHT`

Sau khi xong → đổi lại **không viền** hoặc viền trắng.

* * *

4️⃣ Chỉ tô trắng, KHÔNG vẽ viền (cách chuẩn khi xuất file)
----------------------------------------------------------

```python
page.draw_rect(
    cover_rect,
    fill=(1, 1, 1),
    color=None,
    overlay=True
)
```

➡️ Đây là **cách nên dùng cuối cùng**.

* * *

5️⃣ Tóm tắt nhanh
-----------------

| Mục tiêu | Cách làm |
| --- | --- |
| Che số cũ | `fill=(1,1,1)` |
| Không có viền | không dùng `color` |
| Viền trắng | `color=(1,1,1)` |
| Debug dễ nhìn | `color=(1,0,0)` |

* * *

Nếu bạn muốn:

*   **Che nhưng vẫn giữ nền gốc (không trắng)**
*   **Làm mờ (blur) số cũ**
*   **Tự dò vị trí số trang cũ**

👉 nói tiếp, mình làm code nâng cao cho bạn luôn 🔧💪



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)