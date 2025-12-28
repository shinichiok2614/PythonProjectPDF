# Ghép nối file PDF

**User:** shinichiok kudo (phuonghoangit2614@gmail.com)  
**Created:** 12/28/2025 14:14:15  
**Updated:** 12/28/2025 15:05:04  
**Exported:** 12/28/2025 15:25:23  
**Link:** [https://chatgpt.com/c/6950d8b4-d114-8320-bd17-1c03c7bc4cc4](https://chatgpt.com/c/6950d8b4-d114-8320-bd17-1c03c7bc4cc4)  

## Response:
Bạn muốn **ghép (nối) nhiều file PDF thành 1 file PDF** đúng không? Có vài cách phổ biến, tuỳ bạn muốn **nhanh – có giao diện – hay tự động bằng code**:

* * *

✅ Cách 1: Ghép PDF nhanh (không cần code)
-----------------------------------------

### Dùng phần mềm

*   **PDFsam Basic** (miễn phí)
*   **Adobe Acrobat** (trả phí)
*   **Foxit PDF**

👉 Chỉ cần chọn các file PDF → sắp xếp thứ tự → Merge.

* * *

✅ Cách 2: Ghép PDF bằng web (tiện nhưng lưu ý bảo mật)
------------------------------------------------------

*   iLovePDF
*   SmallPDF

👉 Không nên dùng nếu PDF chứa dữ liệu nhạy cảm.

* * *

✅ Cách 3: Ghép PDF bằng Python (tự động, rất phù hợp với bạn)
-------------------------------------------------------------

### Cài thư viện

```bash
pip install pypdf
```

### Code ghép nhiều file PDF

```python
from pypdf import PdfMerger
import os

pdf_files = [
    "file1.pdf",
    "file2.pdf",
    "file3.pdf"
]

merger = PdfMerger()

for pdf in pdf_files:
    merger.append(pdf)

output_file = "output_merge.pdf"
merger.write(output_file)
merger.close()

print("Đã ghép xong:", output_file)
```

📌 Có thể:

*   Ghép **theo thứ tự chọn**
*   Ghép **cả thư mục**
*   Tạo **giao diện chọn file (Tkinter)**

* * *

✅ Cách 4: Ghép toàn bộ PDF trong 1 thư mục (tự động)
----------------------------------------------------

```python
from pypdf import PdfMerger
import os

folder = "pdfs"
output = "merge_all.pdf"

merger = PdfMerger()

for file in sorted(os.listdir(folder)):
    if file.lower().endswith(".pdf"):
        merger.append(os.path.join(folder, file))

merger.write(output)
merger.close()
```

* * *

👉 Bạn muốn:

1.  Ghép PDF **có giao diện chọn file (Tkinter)**
2.  Ghép PDF **theo thứ tự kéo thả**
3.  Ghép PDF **kèm đổi tên / đánh số trang**

Nói mình biết để mình viết đúng loại bạn cần 👍

## Response:
Lỗi này **rất hay gặp** 👍  
Nguyên nhân là do **phiên bản `pypdf` bạn đang cài không còn `PdfMerger` nữa** (hoặc IDE đang dùng bản cũ / khác tên).

Hiện tại có **2 trường hợp chính**:

* * *

✅ CÁCH 1 (KHUYẾN NGHỊ): Dùng `PdfWriter` (chuẩn mới của pypdf)
--------------------------------------------------------------

Từ các phiên bản `pypdf` mới, **`PdfMerger` đã bị loại bỏ / deprecated**, thay bằng `PdfWriter`.

### ✅ Code ghép PDF (CHUẨN – KHÔNG LỖI)

```python
from pypdf import PdfReader, PdfWriter

pdf_files = [
    "file1.pdf",
    "file2.pdf",
    "file3.pdf"
]

writer = PdfWriter()

for pdf in pdf_files:
    reader = PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)

output_file = "merge_output.pdf"
with open(output_file, "wb") as f:
    writer.write(f)

print("Đã ghép xong:", output_file)
```

👉 **Code này chạy được trên mọi bản pypdf mới**

* * *

✅ CÁCH 2: Bạn đang dùng bản `pypdf` rất cũ (hoặc IDE báo sai)
-------------------------------------------------------------

### Kiểm tra phiên bản

```bash
pip show pypdf
```

Nếu bạn thấy:

*   version ≥ **3.x / 4.x / 5.x** → **KHÔNG có PdfMerger**
*   version ≤ **2.x** → mới có PdfMerger

* * *

❌ KHÔNG KHUYẾN NGHỊ nhưng vẫn có thể dùng
-----------------------------------------

Cài bản cũ:

```bash
pip install pypdf==2.12.1
```

Rồi code:

```python
from pypdf import PdfMerger
```

⚠️ Nhưng:

*   Dễ xung đột
*   Không còn được duy trì tốt
*   IDE (PyCharm) thường cảnh báo đỏ

* * *

✅ Nếu bạn muốn code GIAO DIỆN (Tkinter)
---------------------------------------

Mình có thể viết cho bạn:

*   Chọn nhiều file PDF
*   Sắp xếp thứ tự
*   Nút Merge
*   Lưu file kết quả

Chỉ cần nói:  
👉 **“Viết bản ghép PDF có giao diện”**  
hoặc  
👉 **“Ghép toàn bộ PDF trong thư mục hiện tại”**

Mình viết đúng kiểu bạn hay dùng luôn 👍



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)