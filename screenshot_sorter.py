import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def sort_screenshots():
    default_folder = os.path.expanduser("~/Desktop")
    selected_folder = filedialog.askdirectory(
        initialdir=default_folder,
        title="Select a folder to organize screenshots"
    )
    if not selected_folder:
        return

    target_folder = os.path.join(selected_folder, "Organized_Screenshots")
    os.makedirs(target_folder, exist_ok=True)

    image_exts = (".png", ".jpg", ".jpeg")
    moved = 0

    for filename in os.listdir(selected_folder):
        filepath = os.path.join(selected_folder, filename)
        if (
            os.path.isfile(filepath)
            and filename.lower().endswith(image_exts)
            and ("screenshot" in filename.lower() or "スクリーンショット" in filename)
        ):
            shutil.move(filepath, os.path.join(target_folder, filename))
            moved += 1

    if moved == 0:
        messagebox.showinfo(
            "Info",
            "No screenshot files found in the selected folder.\n\nMade by @KoyaSolo\nOfficial: yoshiverse1.gumroad.com"
        )
    else:
        messagebox.showinfo(
            "Success",
            f"{moved} screenshot(s) moved to 'Organized_Screenshots'.\n\nMade by @KoyaSolo"
        )

def center_window(win, width=350, height=150):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")

# ウィンドウの初期化
root = tk.Tk()
root.withdraw()

root.title("📂 Screenshot Organizer")
center_window(root)

# 🔒 フッターに製作者名＋配布元
footer = tk.Label(
    root,
    text="Made by @KoyaSolo – Official at yoshiverse1.gumroad.com",
    font=("Helvetica", 8)
)
footer.pack(side="bottom", pady=4)

# 中央のボタン
button = tk.Button(root, text="Organize Screenshots", command=sort_screenshots, font=("Helvetica", 12))
button.place(relx=0.5, rely=0.5, anchor="center")

root.deiconify()
root.mainloop()
