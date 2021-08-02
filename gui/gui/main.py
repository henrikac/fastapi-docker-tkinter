from __future__ import annotations
import json
import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import ttk
from typing import List
from urllib import parse, request


@dataclass
class ShortURL:
    """
    A representation of a ShortURL.

    Attributes
    ----------
    id : int
        The id of the ShortURL.
    url : str
        The url where the ShortURL will redirect to.
    path : str
        The path of the ShortURL.
    redirects : int
        The number of times the ShortURL has been used.
    """
    id: int
    url: str
    path: str
    redirects: int


class UI(ABC):
    """An abstract class that describes which methods a UI should have."""
    @abstractmethod
    def setup(self, controller: Controller) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def add_row(self, row: ShortURL) -> None:
        pass

    @abstractmethod
    def clear_input_field(self) -> None:
        pass


class Controller(ABC):
    """
    An abstract class that describes which methods a Controller should have.
    """
    @abstractmethod
    def __init__(self, ui: UI) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def fetch_urls(self) -> List[ShortURL]:
        pass

    @abstractmethod
    def add_url(self) -> None:
        pass


class TkUI(UI):
    def setup(self, controller: Controller) -> None:
        """Sets up the UI"""
        self.root = tk.Tk()
        self.root.title('URL Shortener')
        
        self.top_frame = tk.Frame(self.root, padx=10, pady=10)

        self.input_field = tk.Entry(self.top_frame, font=('Arial', 16))
        self.add_btn = tk.Button(self.top_frame, font=('Arial', 16))
        self.refresh_btn = tk.Button(self.top_frame, font=('Arial', 16))

        cols = ('Id', 'URL', 'Path', 'Redirects')
        self.table = ttk.Treeview(self.root, columns=cols, show='headings')
        for col in cols:
            self.table.heading(col, text=col)
        self._set_table(controller)

        self.add_btn["text"] = "Add"
        self.add_btn["command"] = controller.add_url

        self.refresh_btn["text"] = "Refresh"
        self.refresh_btn["command"] = lambda: self._set_table(controller)

        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.add_btn.pack(side=tk.RIGHT)
        self.input_field.pack(side=tk.RIGHT)
        self.refresh_btn.pack(side=tk.LEFT)
        self.table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def start(self) -> None:
        """Starts the mainloop"""
        self.root.mainloop()

    def add_row(self, row: ShortURL) -> None:
        """Appends a ShortURL to the table"""
        self.table.insert('', tk.END, values=(
            row.id,
            row.url,
            row.path,
            row.redirects
        ))

    def clear_input_field(self):
        """Clears the input field"""
        self.input_field.delete(0, tk.END)

    def _set_table(self, controller: Controller) -> None:
        """Populates the table with ShortURLs"""
        self._clear_table()
        rows: List[ShortURL] = controller.fetch_urls()
        for row in rows:
            self.add_row(row)

    def _clear_table(self) -> None:
        """Clears the table"""
        rows = self.table.get_children()
        for row in rows:
            self.table.delete(row)


class App(Controller):
    def __init__(self, ui: UI) -> None:
        """Initializes a new App"""
        self.ui = ui

    def run(self) -> None:
        """Sets up the UI and starts the mainloop"""
        self.ui.setup(self)
        self.ui.start()

    def fetch_urls(self) -> List[ShortURL]:
        res = request.urlopen('http://localhost:8000/urls')
        json_str = res.read().decode('UTF-8')
        data = json.loads(json_str)
        return [ShortURL(**item) for item in data]

    def add_url(self) -> None:
        data = json.dumps({'url': self.ui.input_field.get()}).encode('UTF-8')
        req = request.Request('http://localhost:8000/', data=data)
        req.add_header('Content-Type', 'application/json')

        try:
            res = request.urlopen(req)
            res_data = json.loads(res.read().decode('UTF-8'))
            short_url = ShortURL(**res_data)
            self.ui.add_row(short_url)
            self.ui.clear_input_field()
        except:  # TODO: handle this
            pass


if __name__ == '__main__':
    ui = TkUI()
    app = App(ui)
    app.run()

