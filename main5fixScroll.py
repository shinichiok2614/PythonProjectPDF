import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import ImageTk, Image
import PyPDF2

class PDFViewerLazy:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer – Fit Width / Fit Page")

        self.pdf_path = None
        self.total_pages = 0
        self.current_page = 1

        self.zoom = 1.0
        self.page_cache = {}  # Cache ảnh gốc PIL

        # --- Canvas ---
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # --- Controls ---
        control = tk.Frame(root)
        control.pack(fill="x")

        tk.Button(control, text="Open PDF", command=self.open_pdf).pack(side="left", padx=5)
        tk.Button(control, text="Prev", command=self.prev_page).pack(side="left", padx=5)
        tk.Button(control, text="Next", command=self.next_page).pack(side="left", padx=5)

        tk.Button(control, text="Zoom +", command=self.zoom_in).pack(side="left", padx=5)
        tk.Button(control, text="Zoom -", command=self.zoom_out).pack(side="left", padx=5)

        tk.Button(control, text="Fit Width", command=self.fit_width).pack(side="left", padx=5)
        tk.Button(control, text="Fit Page", command=self.fit_page).pack(side="left", padx=5)

        self.page_label = tk.Label(control, text="Page: 0/0")
        self.page_label.pack(side="right", padx=10)

        self.current_pil_page = None  # giữ trang gốc để fit lại khi resize

        # Bind lăn chuột
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)         # Windows

    def on_mouse_wheel(self, event):
        """Scroll + tự chuyển trang khi tới đầu/cuối."""
        # Hướng scroll
        direction = -1 if event.delta > 0 else 1

        # Scroll canvas
        self.canvas.yview_scroll(direction, "units")

        # Lấy vị trí scroll hiện tại
        top, bottom = self.canvas.yview()

        # Nếu kéo xuống và gần chạm đáy → sang trang tiếp theo
        if bottom >= 1.0 and direction > 0:
            if self.current_page < self.total_pages:
                self.current_page += 1
                self.load_page()
                self.canvas.yview_moveto(0)  # bắt đầu trang mới từ top

        # Nếu kéo lên và gần chạm top → sang trang trước
        if top <= 0.0 and direction < 0:
            if self.current_page > 1:
                self.current_page -= 1
                self.load_page()
                self.canvas.yview_moveto(1.0)  # bắt đầu trang trước từ bottom



    # =========================================================
    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        self.pdf_path = file_path
        self.page_cache.clear()
        self.zoom = 1.0

        # Lấy tổng số trang
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            self.total_pages = len(reader.pages)

        self.current_page = 1
        self.load_page()

    # =========================================================
    def load_page(self):
        """Load đúng 1 trang PDF (cache tránh convert lại)."""

        self.page_label.config(text=f"Page: {self.current_page}/{self.total_pages}")

        # Nếu trang đã cached → dùng lại
        if self.current_page in self.page_cache:
            pil_img = self.page_cache[self.current_page]
        else:
            pil_img = convert_from_path(
                self.pdf_path,
                dpi=150,
                first_page=self.current_page,
                last_page=self.current_page
            )[0]

            self.page_cache[self.current_page] = pil_img

        self.current_pil_page = pil_img

        self.render_zoom()

    # =========================================================
    def render_zoom(self):
        """Resize ảnh theo zoom hiện tại & hiển thị."""
        if self.current_pil_page is None:
            return

        w, h = self.current_pil_page.size
        new_w = int(w * self.zoom)
        new_h = int(h * self.zoom)

        resized = self.current_pil_page.resize((new_w, new_h), Image.LANCZOS)

        self.tk_img = ImageTk.PhotoImage(resized)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # =========================================================
    def on_canvas_resize(self, event):
        """Auto Fit Width / Fit Page nếu người dùng resize cửa sổ."""
        if self.current_pil_page is None:
            return

        # Nếu đang ở chế độ Fit Width
        if hasattr(self, "mode") and self.mode == "width":
            self.fit_width()
        # Nếu đang ở chế độ Fit Page
        elif hasattr(self, "mode") and self.mode == "page":
            self.fit_page()

    # =========================================================
    def fit_width(self):
        if self.current_pil_page is None:
            return

        self.mode = "width"

        canvas_w = self.canvas.winfo_width()
        page_w, _ = self.current_pil_page.size

        self.zoom = canvas_w / page_w
        self.render_zoom()

    # =========================================================
    def fit_page(self):
        if self.current_pil_page is None:
            return

        self.mode = "page"

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        page_w, page_h = self.current_pil_page.size

        zoom_w = canvas_w / page_w
        zoom_h = canvas_h / page_h

        # chọn zoom nhỏ hơn để vừa khung
        self.zoom = min(zoom_w, zoom_h)

        self.render_zoom()

    # =========================================================
    def zoom_in(self):
        self.mode = "manual"
        self.zoom += 0.1
        self.render_zoom()

    def zoom_out(self):
        self.mode = "manual"
        if self.zoom > 0.2:
            self.zoom -= 0.1
            self.render_zoom()

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
root = tk.Tk()
app = PDFViewerLazy(root)
root.mainloop()
