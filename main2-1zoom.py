import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import Image, ImageTk

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer – Zoom")

        self.zoom = 1.0            # Zoom mặc định
        self.pdf_pages = []        # Lưu ảnh gốc (PIL)
        self.tk_pages = []         # Lưu ảnh để hiển thị lên Tkinter

        # --- Canvas + Scroll ---
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True, side="left")

        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # --- Nút chức năng ---
        control = tk.Frame(root)
        control.pack(fill="x")

        tk.Button(control, text="Open PDF", command=self.open_pdf).pack(side="left", padx=5)
        tk.Button(control, text="Zoom +", command=self.zoom_in).pack(side="left", padx=5)
        tk.Button(control, text="Zoom -", command=self.zoom_out).pack(side="left", padx=5)

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    # =========================================================
    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        # Reset
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.pdf_pages.clear()
        self.tk_pages.clear()

        # Convert PDF → images
        pages = convert_from_path(file_path, dpi=150)

        # Lưu ảnh gốc (PIL)
        self.pdf_pages = pages

        # Hiển thị lần đầu
        self.display_pages()

    # =========================================================
    def display_pages(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.tk_pages = []

        for page in self.pdf_pages:
            # Áp dụng zoom: resize ảnh
            w, h = page.size
            new_w = int(w * self.zoom)
            new_h = int(h * self.zoom)
            resized = page.resize((new_w, new_h), Image.LANCZOS)

            img = ImageTk.PhotoImage(resized)
            self.tk_pages.append(img)

            lbl = tk.Label(self.frame, image=img)
            lbl.pack(pady=10)

    # =========================================================
    def zoom_in(self):
        self.zoom += 0.1
        self.display_pages()

    def zoom_out(self):
        if self.zoom > 0.2:  # Không cho zoom âm
            self.zoom -= 0.1
            self.display_pages()

# =========================================================
root = tk.Tk()
app = PDFViewer(root)
root.mainloop()
