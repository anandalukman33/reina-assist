import tkinter as tk
from ui.window import MeetingAssistantGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MeetingAssistantGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()