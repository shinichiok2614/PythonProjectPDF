import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import ImageTk, Image
import PyPDF2

class PDFViewerLazy:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer – Lazy Load + Zoom")

        # PDF data
        self.pdf_path = None
        self.total_pages = 0
        self.current_page = 1
        self.zoom = 1.0
        self.page_cache = {}  # Cache để tránh convert lại PDF

        # --- UI ---
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Controls
        control = tk.Frame(root)
        control.pack(fill="x")

        tk.Button(control, text="Open PDF", command=self.open_pdf).pack(side="left", padx=5)
        tk.Button(control, text="Prev", command=self.prev_page).pack(side="left", padx=5)
        tk.Button(control, text="Next", command=self.next_page).pack(side="left", padx=5)
        tk.Button(control, text="Zoom +", command=self.zoom_in).pack(side="left", padx=5)
        tk.Button(control, text="Zoom -", command=self.zoom_out).pack(side="left", padx=5)

        self.page_label = tk.Label(control, text="Page: 0/0")
        self.page_label.pack(side="right", padx=10)

    # =========================================================
    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        self.pdf_path = file_path

        # Lấy số trang PDF bằng PyPDF2 (nhanh)
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            self.total_pages = len(reader.pages)

        self.current_page = 1
        self.page_cache.clear()

        self.load_page()

    # =========================================================
    def load_page(self):
        """Load trang PDF → ảnh (cache để tránh convert lại)."""

        # Cập nhật text trang
        self.page_label.config(text=f"Page: {self.current_page}/{self.total_pages}")

        # Nếu trang đã có trong cache → dùng lại
        if self.current_page in self.page_cache:
            pil_img = self.page_cache[self.current_page]
        else:
            # Convert đúng 1 trang (không lag)
            pil_img = convert_from_path(
                self.pdf_path,
                dpi=150,
                first_page=self.current_page,
                last_page=self.current_page
            )[0]

            # Lưu cache
            self.page_cache[self.current_page] = pil_img

        # Resize theo zoom
        w, h = pil_img.size
        resized = pil_img.resize((int(w * self.zoom), int(h * self.zoom)), Image.LANCZOS)

        # Hiển thị
        self.tk_img = ImageTk.PhotoImage(resized)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # =========================================================
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_page()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page()

    # =========================================================
    def zoom_in(self):
        self.zoom += 0.1
        self.load_page()

    def zoom_out(self):
        if self.zoom > 0.2:
            self.zoom -= 0.1
            self.load_page()

# =========================================================
root = tk.Tk()
app = PDFViewerLazy(root)
root.mainloop()
