import tkinter as tk
from tkinter import ttk


class IPWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Rexair Software Updater")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        # Main frame that holds left and right sections
        main_frame = ttk.Frame(master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for buttons and labels
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Create 5 buttons and labels in a column
        for i in range(5):
            row_frame = ttk.Frame(left_frame)
            row_frame.pack(fill=tk.X, pady=5)

            button = ttk.Button(row_frame, text=f"Button {i + 1}")
            button.pack(side=tk.LEFT, padx=5)

            label = ttk.Label(row_frame, text=f"Label {i + 1}")
            label.pack(side=tk.LEFT, padx=5)

        # Right frame for IP address box
        right_frame = ttk.Frame(main_frame, relief=tk.RIDGE, borderwidth=2, padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ip_label = ttk.Label(right_frame, text="IP Address:")
        ip_label.pack(anchor=tk.W, pady=(0, 5))

        self.ip_entry = ttk.Entry(right_frame, width=25)
        self.ip_entry.pack(anchor=tk.W)
        self.ip_entry.insert(0, "xxx.xxx.xxx.xxx")  # Default IP


if __name__ == "__main__":
    root = tk.Tk()
    app = IPWindow(root)
    root.mainloop()