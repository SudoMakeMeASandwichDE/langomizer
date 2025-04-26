import langomizer as lm
import tkinter as tk
from tkinter import ttk

class LangomizerUi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("langomizer")
        self.geometry("300x300")

        self.text_label = tk.Label(self, text="Enter word:")
        self.text_label.pack()
        self.text_entry = tk.Entry(self)
        self.text_entry.pack()

        self.number_label = tk.Label(self, text="Enter seed:")
        self.number_label.pack()
        self.number_entry = tk.Entry(self)
        self.number_entry.pack()

        self.dropdown_label = tk.Label(self, text="Choose word type:")
        self.dropdown_label.pack()
        self.dropdown_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self, textvariable=self.dropdown_var)
        self.dropdown['values'] = ("noun", "verb", "adjective", "conjunction", "pronoun", "preposition")
        self.dropdown.current(0)
        self.dropdown.pack()

        self.submit_button = tk.Button(self, text="Edit letters", command=self.open_letter_edit)
        self.submit_button.pack()
        self.vowels = ['a', 'e', 'i', 'o', 'u']
        self.consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

        self.submit_button = tk.Button(self, text="Translate", command=self.handle_submit)
        self.submit_button.pack()

        self.output_label = tk.Label(self, text="")
        self.output_label.pack()

        self.new_window_button = tk.Button(self, text="Show basic grammar", command=self.open_new_window)
        self.new_window_button.pack()

        self.lang = None
        self.used_seed = None

    def handle_submit(self):
        text = self.text_entry.get()
        self.used_seed = self.number_entry.get()
        option = self.dropdown_var.get()
        if self.used_seed:
            try:
                self.used_seed = int(self.used_seed)
            except ValueError:
                self.output_label.config(text="Invalid seed")
        if self.used_seed:
            self.lang = lm.SimpleLanguage(seed=self.used_seed, consonants=self.consonants, vowels=self.vowels)
        else:
            self.output_label.config(text="Please enter seed")
            return
        if text:
            self.output_label.config(text=self.lang.translate(text, option))
        else:
            self.output_label.config(text="Please enter a word")
            return
    
    def open_letter_edit(self):
        vowels = ['a', 'e', 'i', 'o', 'u']
        consonants = [
            'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q',
            'r', 's', 't', 'v', 'w', 'x', 'y', 'z'
        ]

        window = tk.Toplevel()
        window.title("Select letters")

        vowel_label = tk.Label(window, text="vowels")
        vowel_label.pack()

        vowel_frame = tk.Frame(window)
        vowel_frame.pack()

        vowel_vars = []
        for idx, v in enumerate(vowels):
            var = tk.BooleanVar(value=True if v in self.vowels else False)
            cb = tk.Checkbutton(vowel_frame, text=v, variable=var)
            cb.grid(row=idx//5, column=idx%5, sticky='w', padx=5, pady=2)
            vowel_vars.append((v, var))

        consonant_label = tk.Label(window, text="consonants")
        consonant_label.pack()

        consonant_frame = tk.Frame(window)
        consonant_frame.pack()

        consonant_vars = []
        for idx, c in enumerate(consonants):
            var = tk.BooleanVar(value=True if c in self.consonants else False)
            cb = tk.Checkbutton(consonant_frame, text=c, variable=var)
            cb.grid(row=idx//5, column=idx%5, sticky='w', padx=5, pady=2)
            consonant_vars.append((c, var))

        def select_all():
            for _, var in vowel_vars + consonant_vars:
                var.set(True)

        def deselect_all():
            for _, var in vowel_vars + consonant_vars:
                var.set(False)

        def get_selected():
            selected_vowels = [v for v, var in vowel_vars if var.get()]
            selected_consonants = [c for c, var in consonant_vars if var.get()]
            if len(selected_vowels) > 0 and len(selected_consonants) > 0:
                self.vowels = selected_vowels
                self.consonants = selected_consonants
                window.destroy()
            else:
                error_window = tk.Toplevel(self)
                error_window.title("Error")
                text = "You need to select at least one vowel and one consonant."
                label = tk.Label(error_window, text=text, wraplength=500, justify="left")
                label.pack(padx=10, pady=10)
                close_button = tk.Button(error_window, text="Close", command=error_window.destroy)
                close_button.pack()

        button_frame = tk.Frame(window)
        button_frame.pack(pady=10)

        select_all_button = tk.Button(button_frame, text="Select all", command=select_all)
        select_all_button.grid(row=0, column=0, padx=5)

        deselect_all_button = tk.Button(button_frame, text="Deselect all", command=deselect_all)
        deselect_all_button.grid(row=0, column=1, padx=5)

        submit_button = tk.Button(window, text="Set", command=get_selected)
        submit_button.pack(pady=10)



    def open_new_window(self):
        try:
            self.used_seed = int(self.number_entry.get())
        except ValueError:
            self.output_label.config(text="Invalid seed")
            return
        window = tk.Toplevel(self)
        window.title("Basic grammar description")
        if not self.lang:
            self.lang = lm.SimpleLanguage(seed=self.used_seed, consonants=self.consonants, vowels=self.vowels)
        text = self.lang.describe_grammar_basics()
        label = tk.Label(window, text=text, wraplength=500, justify="left")
        label.pack(padx=10, pady=10)

        close_button = tk.Button(window, text="Close", command=window.destroy)
        close_button.pack()

if __name__ == "__main__":
    langomizer_ui = LangomizerUi()
    langomizer_ui.mainloop()

