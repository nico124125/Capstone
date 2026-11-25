import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import yt_dlp
import json
    

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

link_label = ttk.Label(mainframe, text="YouTube URL:")
link_label.grid(column=0, row=0, padx=10, pady=10, sticky=W)
link_entry = ttk.Entry(mainframe, width=50)
link_entry.grid(column=1, row=0, padx=10, pady=10, sticky=(W, E))
download_button = ttk.Button(mainframe, text="Download audio", command=on_click)
download_button.grid(column=1, row=2, padx=10, pady=10, sticky=E)

label2 = ttk.Label(
    tab2,
    text="The metadata yo"
)
label4 = ttk.Label(tab3, text="Download audio only from videos you own or are authorized to save.")
label4.grid(column=0, row=0, padx=30, pady=30)

tkvar = StringVar(mainframe)
tkvar.set('Options') 



label2.grid(column=0, row=0, padx=30, pady=30)

label4.grid(column=0, row=0, padx=30, pady=30)

label3 = ttk.Label(tab4, text="Place hold").grid(column=0, row=0, padx=30, pady=30)

root.mainloop()
