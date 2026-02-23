
# cipher_lab.py
import tkinter as tk
from tkinter import messagebox
from mono import Mono, check_keyword  # import from mono.py in the same folder

def main():
    root = tk.Tk()
    root.title("Keyword Cipher Lab")
    root.geometry("760x520")

    # -- Layout: a simple 2-column grid for clarity --
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(3, weight=1)   # input text row grows
    root.rowconfigure(5, weight=1)   # output text row grows

    # --- Row 0: Keyword ---
    tk.Label(root, text="KEYWORD (A–Z, no repeats):").grid(row=0, column=0, sticky="w", padx=10, pady=(12, 4))
    keyword_entry = tk.Entry(root)
    keyword_entry.grid(row=0, column=1, sticky="we", padx=10, pady=(12, 4))
    keyword_entry.focus_set()
    # Keep this in sync across calls
    def get_key() -> str:
        return keyword_entry.get().strip().upper()

    # --- Row 1: Validation status ---
    status = tk.StringVar(value="Enter a valid KEYWORD to enable Encode/Decode.")
    tk.Label(root, textvariable=status, fg="#555").grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

    # --- Row 2: Buttons ---
    btn_frame = tk.Frame(root)
    btn_frame.grid(row=2, column=0, columnspan=2, sticky="we", padx=10, pady=6)
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    encode_btn = tk.Button(btn_frame, text="Encode")
    encode_btn.grid(row=0, column=0, sticky="we", padx=(0, 6))
    decode_btn = tk.Button(btn_frame, text="Decode")
    decode_btn.grid(row=0, column=1, sticky="we", padx=(6, 0))

    # Initially disabled until keyword is valid
    encode_btn.config(state=tk.DISABLED)
    decode_btn.config(state=tk.DISABLED)

    # --- Row 3: Input ---
    tk.Label(root, text="INPUT (uppercase letters A–Z recommended):").grid(row=3, column=0, columnspan=2, sticky="w", padx=10)
    input_text = tk.Text(root, height=8, wrap="word")
    input_text.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 8))

    # --- Row 5: Output ---
    tk.Label(root, text="OUTPUT:").grid(row=5, column=0, columnspan=2, sticky="w", padx=10)
    output_text = tk.Text(root, height=8, wrap="word")
    output_text.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))

    # --- Behaviours --------------------------------------------------------

    def validate_key(event=None):
        key = get_key()
        if check_keyword(key):
            encode_btn.config(state=tk.NORMAL)
            decode_btn.config(state=tk.NORMAL)
            status.set("Keyword OK. You can Encode/Decode.")
        else:
            encode_btn.config(state=tk.DISABLED)
            decode_btn.config(state=tk.DISABLED)
            status.set("Invalid keyword. Use A–Z uppercase, no letters repeated.")

    def do_encode():
        key = get_key()
        if not check_keyword(key):
            messagebox.showwarning("Keyword", "Invalid keyword.\nUse A–Z uppercase with no repeated letters.")
            return
        mono = Mono(key)
        text = input_text.get("1.0", tk.END).upper()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, mono.encode(text))

    def do_decode():
        key = get_key()
        if not check_keyword(key):
            messagebox.showwarning("Keyword", "Invalid keyword.\nUse A–Z uppercase with no repeated letters.")
            return
        mono = Mono(key)
        text = output_text.get("1.0", tk.END).upper()
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, mono.decode(text))

    # Wire callbacks
    encode_btn.config(command=do_encode)
    decode_btn.config(command=do_decode)

    # Bindings: Return validates keyword; live validation optional on KeyRelease
    keyword_entry.bind("<Return>", validate_key)
    keyword_entry.bind("<KeyRelease>", validate_key)  # Optional live validation

    # --- Optional convenience: right-click clear actions -------------------
    def clear_input(event=None):
        input_text.delete("1.0", tk.END)
    def clear_output(event=None):
        output_text.delete("1.0", tk.END)
    root.bind("<Control-BackSpace>", lambda e: (clear_input(), clear_output()))

    root.mainloop()

if __name__ == "__main__":
    main()
