import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import fitz  # PyMuPDF


class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer – Continuous Scroll")

        # ====== PDF Data ======
        self.doc = None
        self.total_pages = 0
        self.zoom = 1.0

        # Cache ảnh từng trang
        self.page_cache = {}

        # ====== Canvas + Frame để chứa nhiều trang ======
        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill="both", expand=True, side="left")

        self.scroll = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.frame = tk.Frame(self.canvas, bg="gray")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.update_canvas_width)

        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.page_widgets = []   # Label chứa từng trang
        self.page_height_cache = []

        # ====== Toolbar (đặt bên dưới) ======
        toolbar = tk.Frame(root, bg="#ddd", height=40)
        toolbar.pack(side="bottom", fill="x")

        btn = lambda t, c: tk.Button(toolbar, text=t, width=10, command=c)

        btn("Open", self.open_pdf).pack(side="left", padx=5)
        btn("Zoom -", self.zoom_out).pack(side="left")
        btn("100%", self.zoom_reset).pack(side="left")
        btn("Zoom +", self.zoom_in).pack(side="left")
        btn("Fit Width", self.fit_width).pack(side="left")
        btn("Fit Page", self.fit_page).pack(side="left")

    # =======================================================
    def open_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file:
            return

        self.doc = fitz.open(file)
        self.total_pages = self.doc.page_count
        self.zoom = 1.0
        self.page_cache.clear()

        # Xóa widget cũ
        for w in self.page_widgets:
            w.destroy()
        self.page_widgets.clear()

        # Tạo placeholder cho từng trang
        for i in range(self.total_pages):
            lbl = tk.Label(self.frame, bg="white")
            lbl.pack(pady=10)
            self.page_widgets.append(lbl)

        self.lazy_load_visible_pages()

    # =======================================================
    # Canvas resize → fit width content
    def update_canvas_width(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.lazy_load_visible_pages()

    # =======================================================
    # Mouse wheel scroll
    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-event.delta/120), "units")
        self.lazy_load_visible_pages()

    # =======================================================
    # Lazy load trang đang nhìn thấy
    def lazy_load_visible_pages(self):
        if not self.doc:
            return

        top = self.canvas.canvasy(0)
        bottom = top + self.canvas.winfo_height()

        for i, lbl in enumerate(self.page_widgets):
            y = lbl.winfo_y()
            h = lbl.winfo_height()

            if y + h >= top - 300 and y <= bottom + 300:
                self.load_page(i + 1)

    # =======================================================
    # Render trang PDF
    def load_page(self, page_num):
        if page_num in self.page_cache:
            self.page_widgets[page_num-1].config(image=self.page_cache[page_num])
            return

        page = self.doc.load_page(page_num - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom, self.zoom))

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        tk_img = ImageTk.PhotoImage(img)

        self.page_cache[page_num] = tk_img
        self.page_widgets[page_num - 1].config(image=tk_img)

    # =======================================================
    # ZOOM
    def zoom_in(self):
        self.zoom *= 1.2
        self.redraw_all()

    def zoom_out(self):
        self.zoom /= 1.2
        self.redraw_all()

    def zoom_reset(self):
        self.zoom = 1.0
        self.redraw_all()

    # Zoom xong phải xoá và load lại
    def redraw_all(self):
        if not self.doc:
            return

        self.page_cache.clear()

        for lbl in self.page_widgets:
            lbl.config(image="")

        self.lazy_load_visible_pages()

    # =======================================================
    # FIT WIDTH
    def fit_width(self):
        if not self.doc:
            return

        # Lấy trang đầu để tính kích thước
        page = self.doc.load_page(0)
        rect = page.rect

        canvas_w = self.canvas.winfo_width()
        self.zoom = canvas_w / rect.width

        self.redraw_all()

    # =======================================================
    # FIT PAGE
    def fit_page(self):
        if not self.doc:
            return

        page = self.doc.load_page(0)
        rect = page.rect

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        zoom_w = canvas_w / rect.width
        zoom_h = canvas_h / rect.height

        self.zoom = min(zoom_w, zoom_h)

        self.redraw_all()


# =======================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewer(root)
    root.mainloop()
