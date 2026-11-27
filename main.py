import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
from PIL import Image, ImageTk
import yt_dlp
import json
    

thumbnail_photo = None


def on_click():
    url = link_entry.get().strip()
    if not url:
        messagebox.showerror("Missing URL", "Enter a YouTube video URL.")
        return

    downloads = Path.home() / "Downloads"

    try:
        downloads.mkdir(parents=True, exist_ok=True)
        options = {
            "format": "bestaudio[ext=m4a]/bestaudio",
            "outtmpl": str(downloads / "%(title)s.%(ext)s"),
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    except OSError as error:
        messagebox.showerror("Unable to use Downloads folder", str(error))
    except yt_dlp.utils.DownloadError as error:
        messagebox.showerror("Download failed", str(error))
    else:
        messagebox.showinfo("Download complete", f"Audio saved in:\n{downloads}")


def show_thumbnail():
    global thumbnail_photo

    url = link_entry.get().strip()
    if not url:
        messagebox.showerror("Missing URL", "Enter a YouTube video URL.")
        return

    try:
        with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as error:
        messagebox.showerror("Unable to load video info", str(error))
        return

    def display_value(value):
        if value is None or value == "":
            return "Unknown"
        if isinstance(value, (list, tuple)):
            return ", ".join(str(item) for item in value) or "Unknown"
        return str(value)

    details = (
        ("Title", info.get("title")),
        ("Uploader", info.get("uploader") or info.get("channel")),
        ("Channel", info.get("channel")),
        ("Genre", info.get("genre") or info.get("categories")),
        ("Duration", info.get("duration_string") or info.get("duration")),
        ("Views", info.get("view_count")),
        ("Upload date", info.get("upload_date") or info.get("release_date")),
    )
    metadata = "\n".join(
        f"{name}: {display_value(value)}" for name, value in details
    )
    label2.configure(text=metadata, image="")

    thumbnail_url = info.get("thumbnail")
    if not thumbnail_url:
        return

    try:
        with urlopen(thumbnail_url, timeout=15) as response:
            image = Image.open(BytesIO(response.read()))
        image.thumbnail((480, 270), Image.Resampling.LANCZOS)
        thumbnail_photo = ImageTk.PhotoImage(image)
        label2.configure(image=thumbnail_photo)
    except (yt_dlp.utils.DownloadError, OSError) as error:
        messagebox.showerror("Unable to load thumbnail", str(error))






root = tk.Tk()
root.title("DNC YouTube Audio Download Test")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Download')
tabControl.add(tab2, text='Info')
tabControl.add(tab3, text='Disclaimer')
tabControl.pack(expand=1, fill="both")



mainframe = Frame(tab1)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.rowconfigure(0, weight=1)

link_label = ttk.Label(mainframe, text=": YouTube URL")
link_label.grid(column=5, row=0, padx=10, pady=10, sticky=E)
link_entry = ttk.Entry(mainframe, width=50)
link_entry.grid(column=1, row=0, padx=10, pady=10, sticky=(W, E))
download_button = ttk.Button(mainframe, text="Download audio", command=lambda: [on_click(), show_thumbnail()])
download_button.grid(column=0, row=0, padx=10, pady=10, ipadx=15, ipady=15, sticky=W)

label2 = ttk.Label(
    tab2,
    text="Enter a YouTube URL and click Download audio to view its details.",
    compound="top",
    justify="left",
    anchor="nw",
    wraplength=600,
)
label2.grid(column=0, row=1, padx=30, pady=10)
label4 = ttk.Label(tab3, text="Download audio only from videos you own or are authorized to save.")
label4.grid(column=0, row=0, padx=30, pady=30)

tkvar = StringVar(mainframe)
tkvar.set('Options') 



label4.grid(column=0, row=0, padx=30, pady=30)

label3 = ttk.Label(tab4, text="Place hold").grid(column=0, row=0, padx=30, pady=30)

root.mainloop()
