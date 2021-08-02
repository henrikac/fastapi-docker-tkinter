import json
import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import ttk
from urllib import parse, request


@dataclass
class ShortURL:
    id: int
    url: str
    path: str
    redirects: int


class UI(ABC):
    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def start(self):
        pass


class TkUI(UI):
    def setup(self, controller):
        self.root = tk.Tk()
        self.root.title('URL Shortener')
        
        self.top_frame = tk.Frame(self.root, padx=10, pady=10)

        self.input_field = tk.Entry(self.top_frame, font=('Arial', 16))

        self.add_btn = tk.Button(self.top_frame, font=('Arial', 16))
        self.add_btn["text"] = "Add"
        self.add_btn["command"] = controller.add_url

        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.add_btn.pack(side=tk.RIGHT)
        self.input_field.pack(side=tk.RIGHT)

        cols = ('Id', 'URL', 'Path', 'Redirects')
        self.table = ttk.Treeview(self.root, columns=cols, show='headings')
        for col in cols:
            self.table.heading(col, text=col)
        self.table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self._set_table(controller)

    def start(self):
        self.root.mainloop()

    def _set_table(self, controller):
        rows = controller.fetch_urls()
        for row in rows:
            self.table.insert('', tk.END, values=(row.id, row.url, row.path, row.redirects))

    def _clear_table(self):
        rows = table.get_children()
        for row in rows:
            self.table.delete(row)


class App:
    def __init__(self, ui: UI):
        self.ui = ui

    def run(self):
        self.ui.setup(self)
        self.ui.start()

    def fetch_urls(self):
        res = request.urlopen('http://localhost:8000/urls')
        json_str = res.read().decode('UTF-8')
        data = json.loads(json_str)
        return [ShortURL(**item) for item in data]

    def add_url(self):
        data = json.dumps({'url': self.ui.input_field.get()}).encode('UTF-8')
        req = request.Request('http://localhost:8000/', data=data)
        req.add_header('Content-Type', 'application/json')

        try:
            res = request.urlopen(req)
            res_data = json.loads(res.read().decode('UTF-8'))
            short_url = ShortURL(**res_data)
            self.ui.table.insert('', tk.END, values=(
                short_url.id,
                short_url.url,
                short_url.path,
                short_url.redirects
            ))
            self.ui.input_field.delete(0, tk.END)
        except:  # TODO: handle this
            pass

if __name__ == '__main__':
    ui = TkUI()
    app = App(ui)
    app.run()

