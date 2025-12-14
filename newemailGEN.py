import random
import string
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import os

# ---------------- CONFIG ----------------
PROVIDERS = {
    "Outlook": "@outlook.com",
    "Gmail": "@gmail.com",
    "Hotmail": "@hotmail.com",
    "iCloud": "@icloud.com",
    "Yahoo": "@yahoo.com",
}

LOG_FILE = "generated_accounts.txt"

EMAIL_LETTERS = string.ascii_lowercase
EMAIL_BODY_CHARS = string.ascii_lowercase + string.digits + "."
PWD_SYMBOLS = "!@#$%^&*?_ -"

LOCAL_MIN = 5
LOCAL_MAX = 12

FIRST_NAMES = [
    "Andrew","Ava","Maya","Liam","Noah","Sophia","Ethan","Isabella","Lucas","Mina",
    "Elijah","Aiden","Zara","Kai","Amir","Yara","Diego","Elena","Mateo","Sofia",
    "Oliver","Charlotte","James","Amelia","Benjamin","Harper","Henry","Evelyn",
    "Daniel","Ella","Leo","Chloe","Julian","Layla","Sebastian","Nora","Theo",
    "Hannah","Aaron","Brooklyn","Caleb","Scarlett","Isaac","Penelope","Miles",
    "Aurora","Ezra","Savannah","Asher","Lucy","Roman","Stella","Finn","Violet"
]

LAST_NAMES = [
    "Wild","Nguyen","Patel","Singh","Garcia","Johnson","Kim","Hernandez","Ali",
    "Khan","Chen","Morales","Brown","Davis","Wilson","Lopez","Martinez","Park",
    "Anderson","Taylor","Thomas","Moore","Jackson","Martin","Lee","Perez","Thompson",
    "White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young",
    "Allen","King","Wright","Scott","Torres","Ng","Hill","Flores","Green","Adams"
]

# ---------------- DUPLICATE HANDLING ----------------
def load_existing_emails():
    existing = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "@" in line:
                    existing.add(line.split("|")[0].strip())
    return existing

SESSION_EMAILS = set()
EXISTING_EMAILS = load_existing_emails()

# ---------------- GENERATION ----------------
def rand_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)

def rand_birthday(min_year=1999, max_year=2006):
    start = datetime(min_year, 1, 1)
    end = datetime(max_year, 12, 31)
    d = start + timedelta(days=random.randint(0, (end - start).days))
    return d.strftime("%m/%d/%Y")

def enforce_min_length(local):
    while len(local) < LOCAL_MIN:
        local += random.choice(string.digits)
    return local[:LOCAL_MAX]

def random_email_local():
    length = random.randint(LOCAL_MIN, LOCAL_MAX)
    s = [random.choice(EMAIL_LETTERS)]
    while len(s) < length:
        ch = random.choice(EMAIL_BODY_CHARS)
        if ch == "." and s[-1] == ".":
            continue
        s.append(ch)
    if s[-1] == ".":
        s[-1] = random.choice(string.ascii_lowercase)
    return "".join(s)

def smart_email_local(first, last, provider):
    base = [
        f"{first}{last}",
        f"{first}.{last}",
        f"{first}{random.randint(10,999)}",
        f"{first[0]}{last}{random.randint(10,999)}",
    ]
    local = random.choice(base).lower()
    local = enforce_min_length(local)

    if provider == "Gmail" and random.choice([True, False]):
        idx = random.randint(1, len(local)-2)
        local = local[:idx] + "." + local[idx:]

    return local

def rand_password(smart=False):
    length = random.randint(12, 16) if smart else random.randint(8, 10)
    picks = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(PWD_SYMBOLS),
    ]
    pool = string.ascii_letters + string.digits + PWD_SYMBOLS
    picks += [random.choice(pool) for _ in range(length - 4)]
    random.shuffle(picks)
    return "".join(picks)

def unique_email(local, domain):
    email = f"{local}{domain}"
    attempts = 0
    while email in EXISTING_EMAILS or email in SESSION_EMAILS:
        attempts += 1
        if attempts > 25:
            local += str(random.randint(0,9))
        else:
            local = enforce_min_length(local + random.choice(string.digits))
        email = f"{local}{domain}"
    SESSION_EMAILS.add(email)
    return email

# ---------------- GUI ACTIONS ----------------
def generate(count=1):
    provider = provider_var.get()
    mode = mode_var.get()
    log = log_var.get()
    results = ""

    if provider not in PROVIDERS:
        messagebox.showerror("Error", "Pick an email provider.")
        return

    for _ in range(count):
        first, last = rand_name()

        if mode == "Smart":
            local = smart_email_local(first, last, provider)
            password = rand_password(True)
            dob = rand_birthday(1998, 2004)
        else:
            local = random_email_local()
            password = rand_password(False)
            dob = rand_birthday()

        local = enforce_min_length(local)
        email = unique_email(local, PROVIDERS[provider])

        block = f"{email} | {password} | {first} {last} | {dob}\n"
        results += block

    text_box.insert(tk.END, results)
    text_box.see(tk.END)

    if log:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(results)
            for line in results.splitlines():
                if "@" in line:
                    EXISTING_EMAILS.add(line.split("|")[0].strip())

def copy_output():
    pyperclip.copy(text_box.get("1.0", tk.END))
    messagebox.showinfo("Copied", "Output copied to clipboard")

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Obeys Email Generator")
root.geometry("680x720")
root.resizable(False, False)
root.configure(bg="#050807")

style = ttk.Style(root)
style.theme_use("default")
style.configure("TLabel", background="#050807", foreground="#9cff9c", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"))
style.configure("TButton", padding=8)
style.configure("TLabelframe", background="#0b1a12", foreground="#9cff9c")
style.configure("TLabelframe.Label", background="#050807", foreground="#4cff4c", font=("Segoe UI", 10, "bold"))

# Header
header = tk.Label(
    root,
    text="Obeys Email Generator",
    font=("Segoe UI", 24, "bold"),
    bg="#050807",
    fg="#4cff4c"
)
header.pack(pady=(15, 5))

sub = tk.Label(
    root,
    text="Fast • Clean • Duplicate-Safe",
    bg="#050807",
    fg="#5fae5f",
    font=("Segoe UI", 10)
)
sub.pack(pady=(0, 15))

# Main container
container = tk.Frame(root, bg="#0f0f14")
container.pack(fill="both", expand=True, padx=20)

# Provider frame
provider_frame = ttk.LabelFrame(container, text="1. Email Provider")
provider_frame.pack(fill="x", pady=8)
provider_var = tk.StringVar()
for p in PROVIDERS:
    ttk.Radiobutton(provider_frame, text=p, value=p, variable=provider_var).pack(side="left", padx=10, pady=6)

# Mode frame
mode_frame = ttk.LabelFrame(container, text="2. Generation Mode")
mode_frame.pack(fill="x", pady=8)
mode_var = tk.StringVar(value="Random")
ttk.Radiobutton(mode_frame, text="Random (Fast Burner)", value="Random", variable=mode_var).pack(side="left", padx=10, pady=6)
ttk.Radiobutton(mode_frame, text="Smart (Human-like)", value="Smart", variable=mode_var).pack(side="left", padx=10, pady=6)

# Bulk + logging row
options_frame = ttk.LabelFrame(container, text="3. Options")
options_frame.pack(fill="x", pady=8)

bulk_var = tk.IntVar(value=1)
ttk.Label(options_frame, text="Accounts:").pack(side="left", padx=(10, 4))
ttk.Entry(options_frame, width=6, textvariable=bulk_var).pack(side="left", padx=(0, 15))

log_var = tk.BooleanVar(value=True)
ttk.Checkbutton(options_frame, text="Enable logging (duplicate protection)", variable=log_var).pack(side="left", padx=10)

# Buttons
action_frame = tk.Frame(container, bg="#0f0f14")
action_frame.pack(pady=15)
ttk.Button(action_frame, text="Generate", command=lambda: generate(bulk_var.get())).pack(side="left", padx=8)
ttk.Button(action_frame, text="Copy Output", command=copy_output).pack(side="left", padx=8)

# Output
output_frame = ttk.LabelFrame(container, text="Generated Accounts")
output_frame.pack(fill="both", expand=True, pady=10)

text_box = tk.Text(
    output_frame,
    height=14,
    bg="#020403",
    fg="#9cff9c",
    insertbackground="#4cff4c",
    relief="flat",
    font=("Consolas", 10)
)
text_box.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
