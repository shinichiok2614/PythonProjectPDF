import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import ImageTk, Image

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer")

        # Canvas + Scroll
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.pdf_imgs = []  # giữ ảnh để không bị garbage collected

        # Nút mở file
        btn = tk.Button(root, text="Open PDF", command=self.open_pdf)
        btn.pack()

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def open_pdf(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not file_path:
            return

        # Xóa ảnh cũ
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.pdf_imgs.clear()

        # Convert PDF → list ảnh
        pages = convert_from_path(file_path, dpi=150)

        # Hiển thị từng ảnh lên Tkinter
        for i, page in enumerate(pages):
            img = ImageTk.PhotoImage(page)
            self.pdf_imgs.append(img)

            lbl = tk.Label(self.frame, image=img)
            lbl.pack(pady=10)

root = tk.Tk()
app = PDFViewer(root)
root.mainloop()
