import tkinter as tk
import re

def insert_markdown_text(widget, text):
    pattern = r'(\*\*.+?\*\*)|(\_.+?\_)|(\*.+?\*)|(`.+?`)'
    
    parts = re.split(pattern, text)
    
    for part in parts:
        if not part: 
            continue
            
        if part.startswith('**') and part.endswith('**'):
            widget.insert(tk.END, part[2:-2], "bold")
            
        elif part.startswith('_') and part.endswith('_'):
            widget.insert(tk.END, part[1:-1], "italic")
            
        elif part.startswith('*') and part.endswith('*'):
            widget.insert(tk.END, part[1:-1], "italic")
            
        elif part.startswith('`') and part.endswith('`'):
            widget.insert(tk.END, part[1:-1], "code")
            
        else:
            widget.insert(tk.END, part)