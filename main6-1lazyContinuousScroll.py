import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import ImageTk, Image
import PyPDF2

class ContinuousPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Continuous Scroll – Smooth")

        self.pdf_path = None
        self.total_pages = 0
        self.page_heights = []
        self.page_cache = {}
        self.zoom = 1.0

        # --- Canvas ---
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True, side="left")

        self.scroll = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        # Frame chứa tất cả trang
        self.frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.update_canvas_width)

        # Wheel scroll
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        # Danh sách widget (label) cho từng trang
        self.page_widgets = []

        # --- Controls ---
        bar = tk.Frame(root)
        bar.pack(fill="x")

        tk.Button(bar, text="Open PDF", command=self.open_pdf).pack(side="left", padx=5)
        tk.Button(bar, text="Zoom +", command=self.zoom_in).pack(side="left", padx=5)
        tk.Button(bar, text="Zoom -", command=self.zoom_out).pack(side="left", padx=5)

    # =========================================================
    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        self.pdf_path = file_path
        self.page_cache.clear()
        self.zoom = 1.0

        # Get number of pages
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            self.total_pages = len(reader.pages)

        # Clear old widgets
        for w in self.page_widgets:
            w.destroy()
        self.page_widgets.clear()

        # Create empty placeholders for each page
        for i in range(self.total_pages):
            lbl = tk.Label(self.frame, bg="white")
            lbl.pack(pady=10)
            self.page_widgets.append(lbl)

        self.update_scroll_region()
        self.lazy_load_visible_pages()

    # =========================================================
    def update_canvas_width(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.lazy_load_visible_pages()

    def update_scroll_region(self, event=None):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.lazy_load_visible_pages()

    # =========================================================
    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.lazy_load_visible_pages()

    # =========================================================
    def lazy_load_visible_pages(self):
        """Chỉ load trang đang nằm trong vùng nhìn thấy (viewport)."""
        view_top = self.canvas.canvasy(0)
        view_bottom = view_top + self.canvas.winfo_height()

        y = 0
        for i, lbl in enumerate(self.page_widgets):
            lbl_top = lbl.winfo_y()
            lbl_bottom = lbl_top + lbl.winfo_height()

            # Nếu trang nằm trong hoặc gần viewport → load
            if lbl_bottom >= view_top - 300 and lbl_top <= view_bottom + 300:
                self.load_page(i + 1)

    # =========================================================
    def load_page(self, page_num):
        if page_num in self.page_cache:
            return

        pil_img = convert_from_path(
            self.pdf_path,
            dpi=150,
            first_page=page_num,
            last_page=page_num
        )[0]

        # Apply zoom
        w, h = pil_img.size
        pil_img = pil_img.resize((int(w * self.zoom), int(h * self.zoom)), Image.LANCZOS)

        tk_img = ImageTk.PhotoImage(pil_img)
        self.page_cache[page_num] = tk_img

        self.page_widgets[page_num - 1].config(image=tk_img)
        self.page_widgets[page_num - 1].image = tk_img

    # =========================================================
    def zoom_in(self):
        self.zoom += 0.1
        self.redraw_zoom()

    def zoom_out(self):
        if self.zoom > 0.2:
            self.zoom -= 0.1
            self.redraw_zoom()

    def redraw_zoom(self):
        """Zoom lại tất cả các trang đang hiển thị."""
        self.page_cache.clear()

        for lbl in self.page_widgets:
            lbl.config(image="")

        self.lazy_load_visible_pages()

# =========================================================
root = tk.Tk()
app = ContinuousPDF(root)
root.mainloop()
