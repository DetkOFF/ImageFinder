import os, sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import win32clipboard
from io import BytesIO

def resource_path(rel_path: str) -> str:
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, rel_path)

INDEX_FILE = resource_path("/../inv_index.pkl")

if not os.path.exists(INDEX_FILE):
    print("/../inv_index.pkl not found")
    print("Please use ../tagger/index_generator.py to create it")
    sys.exit(1)


import finder_lite as finder

def copy_image_to_clipboard(path: str):
    img = Image.open(path).convert("RGB")
    output = BytesIO()
    img.save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

class ImgSearchApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # self.iconbitmap("icon.ico")
        self.title("ImgFinder")
        self.geometry("700x400")

        top = tk.Frame(self)
        top.pack(fill="x", padx=10, pady=5)
        self.entry = tk.Entry(top)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<<Paste>>", self.on_paste)
        self.entry.bind("<Return>", lambda e: self.on_search())

        btn = tk.Button(top, text="search", command=self.on_search)
        btn.pack(side="left", padx=5)

        # # Canvas + Scrollbar # #
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(container)
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll( 1, "units"))

        self.thumbs = []

    def on_search(self):
        query = self.entry.get().strip()
        if not query:
            return

        # # Search for the query in the inverted index using finder_lite # #
        found = finder.search_by_word(query, finder.inv_index, operator="AND")
        
        # # Search for the query in the inverted index using finder # #
        # found = finder.search(query, finder.inv_index, operator="OR")
        
        self.show_results(found)

    def on_paste(self, event):
        try:
            clipboard_text = self.clipboard_get()
            self.entry.insert("insert", clipboard_text)
        except tk.TclError:
            pass
        return "break"
    
    def _on_mousewheel(self, event):
        direction = -1 if event.delta > 0 else 1
        scroll_amount = abs(event.delta) // 120  if event.delta else 1
        self.canvas.yview_scroll(direction * scroll_amount, "units")

    def show_results(self, files):
        for w in self.inner.winfo_children():
            w.destroy()
        self.thumbs.clear()

        cols = 4
        thumb_size = (150, 150)
        for idx, fn in enumerate(files):
            row, col = divmod(idx, cols)
            img_path = resource_path(os.path.join("database", fn))
            if not os.path.exists(img_path):
                continue

            img = Image.open(img_path)
            img.thumbnail(thumb_size)
            photo = ImageTk.PhotoImage(img)
            self.thumbs.append(photo)

            lbl = tk.Label(self.inner, image=photo, cursor="hand2")
            lbl.grid(row=row, column=col, padx=5, pady=5)
            lbl.bind("<Button-1>", lambda e, p=img_path: copy_image_to_clipboard(p))

        self.canvas.yview_moveto(0)

if __name__ == "__main__":
    app = ImgSearchApp()
    app.mainloop()