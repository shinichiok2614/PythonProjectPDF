import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import Image, ImageTk


class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer – Zoom + Loading Status")

        self.zoom = 1.0
        self.pdf_pages = []
        self.tk_pages = []

        # ============================
        # Canvas + Scroll
        # ============================
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True, side="left")

        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # ============================
        # Toolbar
        # ============================
        control = tk.Frame(root)
        control.pack(fill="x")

        tk.Button(control, text="Open PDF", command=self.open_pdf).pack(side="left", padx=5)
        tk.Button(control, text="Zoom +", command=self.zoom_in).pack(side="left", padx=5)
        tk.Button(control, text="Zoom -", command=self.zoom_out).pack(side="left", padx=5)

        # ============================
        # Thanh trạng thái loading
        # ============================
        self.status = tk.Label(root, text="Ready", anchor="w", bg="#eee")
        self.status.pack(fill="x")

    # =========================================================
    # OPEN PDF (kèm trạng thái loading)
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

        # ======= Loading Status =======
        self.status.config(text="Đang đọc PDF...", bg="#fffae6")
        self.root.update_idletasks()

        # ======= Convert PDF (TRANG TỪNG TRANG) =======
        try:
            pages = convert_from_path(file_path, dpi=150, first_page=None, last_page=None)
        except Exception as e:
            self.status.config(text=f"Lỗi: {e}", bg="#ffdddd")
            return

        total = len(pages)
        self.pdf_pages = []

        # Convert từng trang + cập nhật trạng thái
        for i, pg in enumerate(pages, start=1):
            self.pdf_pages.append(pg)

            # Update trạng thái
            self.status.config(text=f"Đang tải PDF... (trang {i}/{total})", bg="#fffae6")
            self.root.update_idletasks()

        # Sau khi load xong
        self.status.config(text=f"Đã tải xong {total} trang", bg="#e6ffe6")

        self.display_pages()

    # =========================================================
    # DISPLAY ALL PAGES
    # =========================================================
    def display_pages(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.tk_pages = []

        for page in self.pdf_pages:
            # Resize theo zoom
            w, h = page.size
            new_w = int(w * self.zoom)
            new_h = int(h * self.zoom)
            resized = page.resize((new_w, new_h), Image.LANCZOS)

            img = ImageTk.PhotoImage(resized)
            self.tk_pages.append(img)

            lbl = tk.Label(self.frame, image=img)
            lbl.pack(pady=10)

        self.status.config(text=f"Zoom: {int(self.zoom * 100)}%", bg="#eee")

    # =========================================================
    # ZOOM
    # =========================================================
    def zoom_in(self):
        self.zoom += 0.1
        self.display_pages()

    def zoom_out(self):
        if self.zoom > 0.2:
            self.zoom -= 0.1
            self.display_pages()


# =========================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewer(root)
    root.mainloop()
