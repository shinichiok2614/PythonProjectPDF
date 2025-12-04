import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer")

        # PDF data
        self.doc = None
        self.total_pages = 0
        self.current_page = 1
        self.zoom = 1.0

        # Cache 3 pages
        self.page_cache = {}
        self.cache_limit = 3

        # ===========================================================
        # CANVAS hiển thị PDF
        # ===========================================================
        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        # Scrollbar dọc
        self.v_scroll = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.v_scroll.set)
        self.v_scroll.pack(side="right", fill="y")

        # Mouse wheel
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel_linux)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel_linux)

        # ===========================================================
        # TOOLBAR — nằm ở đáy cửa sổ
        # ===========================================================
        toolbar = tk.Frame(root, bg="#ddd", height=40)
        toolbar.pack(side="bottom", fill="x")

        btn = lambda t, c: tk.Button(toolbar, text=t, width=10, command=c)

        btn("Open", self.open_pdf).pack(side="left", padx=2, pady=5)
        btn("Prev", self.prev_page).pack(side="left")
        btn("Next", self.next_page).pack(side="left")

        btn("Zoom -", self.zoom_out).pack(side="left")
        btn("100%", self.zoom_reset).pack(side="left")
        btn("Zoom +", self.zoom_in).pack(side="left")

        btn("Fit Width", self.fit_width).pack(side="left", padx=10)
        btn("Fit Page", self.fit_page).pack(side="left")

        # Ô nhập số trang
        tk.Label(toolbar, text="Page:").pack(side="left", padx=5)
        self.page_entry = tk.Entry(toolbar, width=5)
        self.page_entry.pack(side="left")
        self.page_entry.bind("<Return>", self.jump_to_page)

    # ======================================================================
    # OPEN PDF
    # ======================================================================
    def open_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file:
            return

        self.doc = fitz.open(file)
        self.total_pages = self.doc.page_count
        self.current_page = 1
        self.page_cache.clear()

        self.load_page()
        self.preload_pages()

    # ======================================================================
    # RENDER + CACHE
    # ======================================================================
    def render_page(self, page_number, zoom):
        if page_number in self.page_cache:
            return self.page_cache[page_number]

        page = self.doc.load_page(page_number - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # update cache
        self.page_cache[page_number] = img
        if len(self.page_cache) > self.cache_limit:
            first = list(self.page_cache.keys())[0]
            del self.page_cache[first]

        return img

    def load_page(self):
        img = self.render_page(self.current_page, self.zoom)

        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def preload_pages(self):
        if self.current_page + 1 <= self.total_pages:
            self.render_page(self.current_page + 1, self.zoom)
        if self.current_page - 1 >= 1:
            self.render_page(self.current_page - 1, self.zoom)

    # ======================================================================
    # MOUSE SCROLL
    # ======================================================================
    def on_mouse_wheel(self, event):
        direction = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(direction, "units")

        top, bottom = self.canvas.yview()

        # Next page
        if bottom >= 1.0 and direction > 0:
            self.next_page()

        # Previous page
        if top <= 0.0 and direction < 0:
            self.prev_page()

    def on_mouse_wheel_linux(self, event):
        direction = -1 if event.num == 4 else 1
        self.on_mouse_wheel(type("e", (object,), {"delta": -direction}))

    # ======================================================================
    # PAGE CONTROL
    # ======================================================================
    def next_page(self):
        if not self.doc or self.current_page >= self.total_pages:
            return
        self.current_page += 1
        self.load_page()
        self.canvas.yview_moveto(0)
        self.preload_pages()

    def prev_page(self):
        if not self.doc or self.current_page <= 1:
            return
        self.current_page -= 1
        self.load_page()
        self.canvas.yview_moveto(1.0)
        self.preload_pages()

    def jump_to_page(self, event=None):
        if not self.doc:
            return
        try:
            p = int(self.page_entry.get())
            if 1 <= p <= self.total_pages:
                self.current_page = p
                self.load_page()
                self.preload_pages()
        except:
            pass

    # ======================================================================
    # ZOOM
    # ======================================================================
    def zoom_in(self):
        if not self.doc:
            return
        self.zoom *= 1.2
        self.page_cache.clear()
        self.load_page()
        self.preload_pages()

    def zoom_out(self):
        if not self.doc:
            return
        self.zoom /= 1.2
        self.page_cache.clear()
        self.load_page()
        self.preload_pages()

    def zoom_reset(self):
        if not self.doc:
            return
        self.zoom = 1.0
        self.page_cache.clear()
        self.load_page()
        self.preload_pages()

    # ======================================================================
    # FIT FUNCTIONS
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
