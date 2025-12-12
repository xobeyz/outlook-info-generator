import random
import string
from datetime import datetime, timedelta

LOG_FILE = "outlook_accounts.txt"

# Allowed for Outlook email local-part (safe subset): letters, digits, dot.
# Rules we enforce:
# - 1–8 chars before "@outlook.com"
# - first char is a letter
# - no starting/ending dot
# - no consecutive dots
EMAIL_LETTERS = string.ascii_lowercase
EMAIL_BODY_CHARS = string.ascii_lowercase + string.digits + "."

# Password: 8–10 chars; include at least one upper, lower, digit, and symbol.
PWD_MIN = 8
PWD_MAX = 10
PWD_SYMBOLS = "!@#$%^&*?_-"  # safe set

FIRST_NAMES = [
    "Andrew","Ava","Maya","Liam","Noah","Sophia","Ethan","Isabella","Lucas","Mina",
    "Aiden","Zara","Kai","Amir","Yara","Diego","Elena","Mateo","Sofia","Jamal",
    "Aria","Noor","Hana","Owen","Ivy","Jalen","Rosa","Niko","Leila","Theo"
]
LAST_NAMES = [
    "Wild","Nguyen","Patel","Singh","Garcia","Johnson","Kim","Hernandez","Ali","Cohen",
    "Ibrahim","Khan","Chen","Morales","Brown","Davis","Wilson","Lopez","Martinez","Park",
    "Baker","Hassan","Novak","Costa","Lombardi","Sato","Ahmed","Silva","Foster","Romero"
]

def rand_email_local():
    # choose length 3–8 (shorter tends to be more available)
    length = random.randint(3, 8)
    s = [random.choice(EMAIL_LETTERS)]  # first must be a letter
    while len(s) < length:
        ch = random.choice(EMAIL_BODY_CHARS)
        # avoid consecutive dots
        if ch == "." and s[-1] == ".":
            continue
        s.append(ch)
    # avoid ending with dot
    if s[-1] == ".":
        s[-1] = random.choice(string.ascii_lowercase + string.digits)
    return "".join(s)

def rand_password():
    length = random.randint(PWD_MIN, PWD_MAX)
    # ensure category coverage
    picks = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(PWD_SYMBOLS),
    ]
    remaining = length - len(picks)
    pool = string.ascii_letters + string.digits + PWD_SYMBOLS
    picks += [random.choice(pool) for _ in range(remaining)]
    random.shuffle(picks)
    return "".join(picks)

def rand_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)

def rand_birthday():
    # 01/01/2000 to 12/31/2006 inclusive
    start = datetime(2000, 1, 1)
    end = datetime(2006, 12, 31)
    delta_days = (end - start).days
    d = start + timedelta(days=random.randint(0, delta_days))
    return d.strftime("%m/%d/%Y")

def generate_record():
    local = rand_email_local()
    email = f"{local}@outlook.com"
    password = rand_password()
    first, last = rand_name()
    dob = rand_birthday()
    return email, password, f"{first} {last}", dob

def log_record(email, password, name, dob):
    block = (
        "----------------------------\n"
        f"{email}\n{password}\n{name}\n{dob}\n"
        "----------------------------\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(block)

def main():
    print("Outlook Info Generator (manual use only) — press R to regenerate, Q to quit.\n")
    while True:
        email, password, name, dob = generate_record()
        print("Generated:")
        print(email)
        print(password)
        print(name)
        print(dob)
        log_record(email, password, name, dob)
        choice = input("\n[R]egenerate or [Q]uit? ").strip().lower()
        if choice == "q":
            print(f"\nSaved to {LOG_FILE}. Bye!")
            break
        # anything else regenerates

if __name__ == "__main__":
    main()
