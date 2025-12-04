import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer (Fast & Smooth)")

        self.doc = None
        self.total_pages = 0
        self.current_page = 1
        self.zoom = 1.0

        self.page_cache = {}      # Cache 3 pages
        self.cache_limit = 3

        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        # scrollbar
        self.v_scroll = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        self.v_scroll.pack(side="right", fill="y")

        # key bindings
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)      # Windows / Mac
        self.canvas.bind("<Button-4>", self.on_mouse_wheel_linux)  # Linux
        self.canvas.bind("<Button-5>", self.on_mouse_wheel_linux)

        # menu
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open PDF", command=self.open_pdf)
        filemenu.add_separator()
        filemenu.add_command(label="Fit Width", command=self.fit_width)
        filemenu.add_command(label="Fit Page", command=self.fit_page)
        menubar.add_cascade(label="File", menu=filemenu)

        self.root.config(menu=menubar)

    # ======================================================================
    # OPEN PDF
    # ======================================================================
    def open_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file:
            return

        self.doc = fitz.open(file)
        self.total_pages = self.doc.page_count
        self.current_page = 1
        self.page_cache.clear()

        self.load_page()
        self.preload_pages()

    # ======================================================================
    # PAGE RENDERING + CACHING
    # ======================================================================
    def render_page(self, page_number, zoom):
        """Render nhanh + cache trang."""
        if page_number in self.page_cache:
            return self.page_cache[page_number]

        page = self.doc.load_page(page_number - 1)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # lưu cache
        self.page_cache[page_number] = img
        if len(self.page_cache) > self.cache_limit:
            first_key = list(self.page_cache.keys())[0]
            del self.page_cache[first_key]

        return img

    def load_page(self):
        """Load trang không giật."""
        img = self.render_page(self.current_page, self.zoom)

        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def preload_pages(self):
        """Preload trang kế + trang trước để scroll cực mượt."""
        if self.current_page + 1 <= self.total_pages:
            self.render_page(self.current_page + 1, self.zoom)

        if self.current_page - 1 >= 1:
            self.render_page(self.current_page - 1, self.zoom)

    # ======================================================================
    # SCROLL (WHEEL)
    # ======================================================================
    def on_mouse_wheel(self, event):
        direction = -1 if event.delta > 0 else 1

        self.canvas.yview_scroll(direction, "units")
        top, bottom = self.canvas.yview()

        # Scroll xuống -> qua trang tiếp theo
        if bottom >= 1.0 and direction > 0:
            if self.current_page < self.total_pages:
                self.current_page += 1
                self.load_page()
                self.canvas.yview_moveto(0)
                self.preload_pages()

        # Scroll lên -> quay lại trang trước
        if top <= 0.0 and direction < 0:
            if self.current_page > 1:
                self.current_page -= 1
                self.load_page()
                self.canvas.yview_moveto(1.0)
                self.preload_pages()

    def on_mouse_wheel_linux(self, event):
        direction = -1 if event.num == 4 else 1
        self.on_mouse_wheel(type("e", (object,), {"delta": -direction}))

    # ======================================================================
    # ZOOM + FIT
    # ======================================================================
    def fit_width(self):
        if not self.doc:
            return
        page = self.doc.load_page(self.current_page - 1)
        rect = page.rect

        canvas_w = self.canvas.winfo_width()
        self.zoom = canvas_w / rect.width

        self.page_cache.clear()
        self.load_page()
        self.preload_pages()

    def fit_page(self):
        if not self.doc:
            return

        page = self.doc.load_page(self.current_page - 1)
        rect = page.rect

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        zoom_w = canvas_w / rect.width
        zoom_h = canvas_h / rect.height

        self.zoom = min(zoom_w, zoom_h)

        self.page_cache.clear()
        self.load_page()
        self.preload_pages()


# ======================================================================
# MAIN
# ======================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewer(root)
    root.mainloop()
