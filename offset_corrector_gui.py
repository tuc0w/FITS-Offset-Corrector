import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from pathlib import Path
from astropy.io import fits
import numpy as np
from datetime import datetime
import webbrowser


class FITSOffsetCorrectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FITS Offset Corrector v1.0 - by tuc0w")

        root.columnconfigure(1, weight=1)
        root.rowconfigure(6, weight=1)

        self.input_dir = tb.StringVar()
        self.output_dir = tb.StringVar()
        self.source_offset = tb.IntVar(value=0)
        self.target_offset = tb.IntVar(value=42)
        self.file_count = tb.IntVar(value=0)

        pad_opts = {"padx": 10, "pady": 5, "sticky": "ew"}

        tb.Label(root, text="Input folder:").grid(
            row=0, column=0, padx=10, pady=(15, 5), sticky="w"
        )
        tb.Entry(root, textvariable=self.input_dir).grid(row=0, column=1, **pad_opts)
        tb.Button(root, text="Choose", command=self.choose_input, bootstyle=SECONDARY).grid(
            row=0, column=2, padx=10, pady=(15, 5), sticky="ew"
        )

        tb.Label(root, text="Files found:").grid(row=1, column=0, **pad_opts)
        tb.Entry(root, textvariable=self.file_count, state="readonly").grid(row=1, column=1, **pad_opts)

        tb.Label(root, text="Output folder:").grid(row=2, column=0, **pad_opts)
        tb.Entry(root, textvariable=self.output_dir).grid(row=2, column=1, **pad_opts)
        tb.Button(root, text="Choose", command=self.choose_output, bootstyle=SECONDARY).grid(
            row=2, column=2, **pad_opts
        )

        tb.Label(root, text="Source Offset:").grid(row=3, column=0, **pad_opts)
        tb.Entry(root, textvariable=self.source_offset, state="readonly").grid(row=3, column=1, **pad_opts)

        tb.Label(root, text="Target Offset:").grid(row=4, column=0, **pad_opts)
        tb.Entry(root, textvariable=self.target_offset).grid(row=4, column=1, **pad_opts)

        btn_frame = tb.Frame(root)
        btn_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=15, sticky="e")

        tb.Button(btn_frame, text="❓", width=3, command=self.show_info, bootstyle=INFO).pack(side="left", padx=(0,5))
        tb.Button(btn_frame, text="Start", command=self.run, bootstyle=SUCCESS).pack(side="left")

        self.log_frame = tb.Frame(root)
        self.log_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.log = tb.Text(
            self.log_frame,
            wrap="word",
            background="#1e1e1e",
            foreground="#d4d4d4",
            insertbackground="white",
            highlightbackground="#333333",
            highlightcolor="#444444",
        )
        self.log.grid(row=0, column=0, sticky="nsew")

        scrollbar = tb.Scrollbar(
            self.log_frame, orient="vertical", command=self.log.yview, bootstyle="dark"
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=scrollbar.set)

        self.log_frame.rowconfigure(0, weight=1)
        self.log_frame.columnconfigure(0, weight=1)

        self.progress = tb.Progressbar(
            root, bootstyle=SUCCESS, mode="determinate"
        )
        self.progress.grid(row=7, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")

        self.center_window(self.root, width=700, height=550)


    def center_window(self, window, width=None, height=None):
        window.update_idletasks()
        if width is None:
            width = window.winfo_width()
        if height is None:
            height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")


    def choose_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_dir.set(path)
            fits_files = sorted(list(Path(path).glob("*.fits")) + list(Path(path).glob("*.fit")))
            self.file_count.set(len(fits_files))
            if fits_files:
                try:
                    with fits.open(fits_files[0]) as hdul:
                        hdr = hdul[0].header
                        if "OFFSET" in hdr:
                            self.source_offset.set(int(hdr["OFFSET"]))
                        else:
                            self.source_offset.set(0)
                except Exception as e:
                    messagebox.showwarning("Warnung", f"Konnte OFFSET nicht lesen:\n{e}")
                    self.source_offset.set(0)


    def choose_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)


    def show_info(self):
        info_win = tb.Toplevel(self.root)
        info_win.title("Info / Credits")
        info_win.resizable(False, False)

        info_win.configure(bg="#1e1e1e")

        tb.Label(info_win, text="FITS Offset Corrector",
                font=("Arial", 12, "bold"), background="#1e1e1e", foreground="#d4d4d4").pack(pady=(10,5))

        tb.Label(info_win, text="Version 1.0",
                background="#1e1e1e", foreground="#d4d4d4").pack(pady=(0,5))

        tb.Label(info_win, text="Andreas Behrend (tuc0w)",
                background="#1e1e1e", foreground="#d4d4d4").pack(pady=(10,5))

        blog = tb.Label(info_win, text="https://andreasbehrend.space",
                        foreground="#4da6ff", background="#1e1e1e", cursor="hand2")
        blog.pack(pady=(5,5))
        blog.bind("<Button-1>", lambda e: webbrowser.open_new("https://andreasbehrend.space"))

        github = tb.Label(info_win, text="https://github.com/tuc0w/FITS-Offset-Corrector",
                        foreground="#4da6ff", background="#1e1e1e", cursor="hand2")
        github.pack(pady=(5,5), padx=30)
        github.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/tuc0w/FITS-Offset-Corrector"))

        tb.Button(info_win, text="Close", bootstyle=SECONDARY, command=info_win.destroy).pack(pady=(20,10))

        self.center_window(info_win)


    def log_write(self, text):
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.root.update()


    def run(self):
        input_dir = Path(self.input_dir.get())
        output_dir = Path(self.output_dir.get())
        output_dir.mkdir(exist_ok=True)

        source_offset = self.source_offset.get()
        target_offset = self.target_offset.get()
        offset_diff = target_offset - source_offset

        fits_files = sorted(list(input_dir.glob("*.fits")) + list(input_dir.glob("*.fit")))
        if not fits_files:
            messagebox.showerror("Fehler", "Keine FITS-Dateien gefunden!")
            return

        medians_before, means_before, stds_before = [], [], []
        medians_after, means_after, stds_after = [], [], []

        self.log.delete(1.0, "end")
        self.log_write(f"Starte Verarbeitung von {len(fits_files)} Dateien...")
        self.log_write(f"Offset-Korrektur: {source_offset} → {target_offset} (Δ={offset_diff})\n")

        self.progress["maximum"] = len(fits_files)
        self.progress["value"] = 0

        for i, flat_path in enumerate(fits_files, start=1):
            with fits.open(flat_path) as hdul:
                data = hdul[0].data.astype(np.float32)
                header = hdul[0].header

                median_before = np.median(data)
                mean_before = np.mean(data)
                std_before = np.std(data)

                data_corrected = data + offset_diff

                median_after = np.median(data_corrected)
                mean_after = np.mean(data_corrected)
                std_after = np.std(data_corrected)

                medians_before.append(median_before)
                means_before.append(mean_before)
                stds_before.append(std_before)
                medians_after.append(median_after)
                means_after.append(mean_after)
                stds_after.append(std_after)

                header["OFFSET"] = target_offset
                header.add_history(
                    f"Offset adjusted by {offset_diff:+d} ADU "
                    f"(from {source_offset} to {target_offset}) "
                    f"on {datetime.utcnow().isoformat()} UTC"
                )

                out_path = output_dir / flat_path.name
                fits.writeto(out_path, data_corrected.astype(np.float32), header, overwrite=True)

                self.log_write(f"[{i}/{len(fits_files)}] {flat_path.name}:")
                self.log_write(f"   Median : {median_before:.1f} → {median_after:.1f}")
                self.log_write(f"   Mean   : {mean_before:.1f} → {mean_after:.1f}")
                self.log_write(f"   StdDev : {std_before:.1f} → {std_after:.1f}")
                self.log_write(f"   Gespeichert in: {out_path}\n")

            self.progress["value"] = i
            self.root.update_idletasks()

        self.log_write("===== Gesamtstatistik über alle Dateien =====")
        self.log_write(
            f"   Median : {np.mean(medians_before):.1f} → {np.mean(medians_after):.1f} "
            f"(Min {np.min(medians_before):.1f}/{np.min(medians_after):.1f}, "
            f"Max {np.max(medians_before):.1f}/{np.max(medians_after):.1f})"
        )
        self.log_write(
            f"   Mean   : {np.mean(means_before):.1f} → {np.mean(means_after):.1f} "
            f"(Min {np.min(means_before):.1f}/{np.min(means_after):.1f}, "
            f"Max {np.max(means_before):.1f}/{np.max(means_after):.1f})"
        )
        self.log_write(
            f"   StdDev : {np.mean(stds_before):.1f} → {np.mean(stds_after):.1f} "
            f"(Min {np.min(stds_before):.1f}/{np.min(stds_after):.1f}, "
            f"Max {np.max(stds_before):.1f}/{np.max(stds_after):.1f})"
        )
        self.log_write("===========================================")

        self.progress["value"] = 0
        messagebox.showinfo("Fertig", f"Verarbeitung abgeschlossen!\n{len(fits_files)} Dateien bearbeitet.")


if __name__ == "__main__":
    app = tb.Window(themename="darkly")
    FITSOffsetCorrectorGUI(app)
    app.mainloop()
