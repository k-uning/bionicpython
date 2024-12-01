"""
A GUI for the bionicpython package. It uses the process_word function to process the input word and display the output.
The output is displayed in a texto box, which font, size, spacing, etc. can be customized.

Author: Kevin Uning
For personal use only, no distribution allowed without permission from the author (especially due to
Bionic Reading (R)'s patent on this technique).
"""

import tkinter as tk
from tkinter import messagebox
import math

from dataclasses import dataclass

@dataclass
class TextOptions():
    """
    Stores the parameters and options chosen for the text to be displayed.
    This includes: font, size, spacing, and bionic ratio.
    """
    font: str = "Aptos Display"
    size: int = 12
    spacing: int = 1
    bionic_ratio: float = 0.5
    list_fonts = ["Aptos Display", "OpenDyslexic"]
    
class TextOptions_GUI(tk.Frame):
    """
    A GUI to set the text options for the output text.
    """
    def __init__(self, master, getter_TextOptions:callable):
        super().__init__(master)
        self.master = master
        
        self.getter_text_options = lambda: getter_TextOptions()
        
        # Automatic widget creation subframe
        self._frm_params = tk.Frame(self)
        self._frm_params.grid(row=0, column=0,sticky='nsew')
        
        # Automatic widget creation parameters
        self._text_options_exclusions = ["font", "list_fonts"]
        self._listwid_label = []
        self._listwid_entry = []
        
        # Automatic widget creation
        self._auto_create_widgets()
        
    def _auto_create_widgets(self):
        """
        Automatically creates the widgets for the text options.
        """
        list_attr = [attr for attr in dir(self.getter_text_options()) if not attr.startswith("__") and not attr in self._text_options_exclusions]
        for attr in list_attr:
            label = tk.Label(self._frm_params, text=attr)
            entry = tk.Entry(self._frm_params)
            entry.bind("<Return>", lambda event, attr=attr, entry=entry, label=label: self._update_textOptionParams(attr,entry,label))
            entry.insert(0, getattr(self.getter_text_options(),attr))
            
            self._listwid_label.append(label)
            self._listwid_entry.append(entry)
            
        for i,tup in enumerate(zip(self._listwid_label,self._listwid_entry)):
            label, entry = tup
            label.grid(row=i, column=0, sticky='w')
            entry.grid(row=i, column=1, sticky='w')
            
            # Force a call to update the text options
            self._update_textOptionParams(list_attr[i],entry,label)
            
    def _update_textOptionParams(self,attr:str,entry:tk.Entry,label:tk.Label):
        """
        Automatically updates the text options parameters based on the entry widget.
        
        Args:
            attr (str): The attribute to be updated.
            entry (tk.Entry): The entry widget to be used for the update.
            label (tk.Label): The label widget to be updated.
        """
        try:
            val = entry.get()
            attr_type = type(getattr(self.getter_text_options(),attr))
            if attr_type == int:
                val = int(float(val))
            elif attr_type == float:
                val = float(val)
            else:
                messagebox.showerror("Error", "Invalid type for attribute.")
            setattr(self.getter_text_options(),attr,val)
            
            # Update the label
            label.config(text="{}: {}".format(attr,val))
            
        except Exception as e:
            messagebox.showerror("Error", "_update_textOptionParams: \n {}".format(e))
        
class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.input_text = tk.Text(self, height=10, width=50)
        self.process_button = tk.Button(self, text="Process", command=self.process_text)
        self.output_label = tk.Label(self, text="Output:")
        self.output_text = tk.Text(self, height=10, width=50)
        
        self.input_text.pack()
        self.process_button.pack()
        self.output_label.pack()
        self.output_text.pack()
        
        # Bind ctrl+enter to the process button
        self.process_button.bind("<Control-Return>", lambda event: self.process_text())
        
    # > Styling for the output text <
        # Set the default text options
        self.textOptions = TextOptions()
        
        # Set the frame for the text options
        self.frm_textOptions = TextOptions_GUI(self, getter_TextOptions=lambda: self.textOptions)
        self.frm_textOptions.pack()

    def process_text(self):
        """
        Processes the input text and displays the output in the output text box.
        """
        # Update the tags
        self.tag_bold = self.output_text.tag_configure("bionic_bold", font=(self.textOptions.font, self.textOptions.size, "bold"))
        self.tag_normal = self.output_text.tag_configure("bionic_normal", font=(self.textOptions.font, self.textOptions.size, "normal"))
        
        # Clear the output text
        self.output_text.delete(1.0, tk.END)
        
        # Get the input text
        input_text = self.input_text.get(1.0, tk.END)
        
        # Process the input text
        list_paragraphs = input_text.split("\n")
        for paragraph in list_paragraphs:
            list_words = paragraph.split()
            for word in list_words:
                wordpart_bold, wordpart_normal = self._process_word(word)
                self.output_text.insert(tk.END, wordpart_bold, "bionic_bold")
                self.output_text.insert(tk.END, wordpart_normal, "bionic_normal")
                self.output_text.insert(tk.END, " ")
                
            self.output_text.insert(tk.END, "\n\n")

    def _process_word(self,word:str) -> tuple:
        """
        Splits the input word into two parts, the first part is bold and the second part is normal.

        Args:
            word (str): The word to be processed.

        Returns:
            tuple: A tuple containing the two parts of the word.
        """
        ratio = self.textOptions.bionic_ratio
        idx_bold = math.ceil(len(word) * ratio)
        output_wordparts = [word[:idx_bold], word[idx_bold:]]
        return output_wordparts

if __name__ == '__main__':
    app = tk.Tk()
    app.title("Bionic Python")
    
    gui = GUI(master=app)
    gui.pack()
    app.mainloop()