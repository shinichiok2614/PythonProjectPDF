import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import Image, ImageTk


class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer – Zoom + Scroll")

        self.zoom = 1.0
        self.pdf_pages = []
        self.tk_pages = []

        # --- Canvas + Scroll ---
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True, side="left")

        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Frame chứa ảnh bên trong canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Bắt sự kiện thay đổi kích thước frame -> cập nhật scrollregion
        self.frame.bind("<Configure>", self.update_scrollregion)
        self.frame.bind("<MouseWheel>", self.on_mouse_wheel)
        # --- Mouse scroll ---
        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        # --- Toolbar ---
        control = tk.Frame(root)
        control.pack(fill="x", pady=4)

        tk.Button(control, text="Open PDF", command=self.open_pdf).pack(side="left", padx=5)
        tk.Button(control, text="Zoom +", command=self.zoom_in).pack(side="left", padx=5)
        tk.Button(control, text="Zoom -", command=self.zoom_out).pack(side="left", padx=5)

    # =========================================================
    def update_scrollregion(self, event=None):
        """Cập nhật vùng scroll của canvas mỗi khi frame thay đổi."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Tự động giãn frame theo chiều ngang canvas
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())

    # =========================================================
    def on_mouse_wheel(self, event):
        """Scroll được trong display_pages."""
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

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

        self.pdf_pages = pages
        self.display_pages()

    # =========================================================
    def display_pages(self):
        """Hiển thị ảnh (sau khi zoom)."""
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.tk_pages = []

        for page in self.pdf_pages:
            w, h = page.size
            new_w = int(w * self.zoom)
            new_h = int(h * self.zoom)

            resized = page.resize((new_w, new_h), Image.LANCZOS)
            img = ImageTk.PhotoImage(resized)

            self.tk_pages.append(img)

            lbl = tk.Label(self.frame, image=img)
            lbl.pack(pady=10)

        # cần update scrollregion sau khi load xong
        self.root.after(10, self.update_scrollregion)

    # =========================================================
    def zoom_in(self):
        self.zoom += 0.1
        self.display_pages()

    def zoom_out(self):
        if self.zoom > 0.2:
            self.zoom -= 0.1
            self.display_pages()


# =========================================================
root = tk.Tk()
app = PDFViewer(root)
root.mainloop()
