import tkinter as tk
from tkinter import messagebox
import random
import string
import re

# Função para gerar a senha
def generate_password(size=None):
    if size is None:
        size = length_scale.get()
    
    length_password = int(size)
    include_symbols = var_symbols.get()
    include_numbers = var_numbers.get()
    include_upcase = var_uppercase.get()
    include_downcase = var_downcase.get()

    total_chars = ''

    if include_upcase:
        total_chars += string.ascii_uppercase
    if include_downcase:
        total_chars += string.ascii_lowercase
    if include_numbers:
        total_chars += string.digits
    if include_symbols:
        total_chars += string.punctuation

    max_percentage = 0.3
    max_specials = int(length_password * max_percentage)

    password = []

    if include_upcase:
        password.extend(random.choices(string.ascii_uppercase, k=max(1, length_password // 4)))
    if include_downcase:
        password.extend(random.choices(string.ascii_lowercase, k=max(1, length_password // 4)))
    if include_numbers:
        password.extend(random.choices(string.digits, k=min(max_specials, length_password // 4)))
    if include_symbols:
        password.extend(random.choices(string.punctuation, k=min(max_specials, length_password // 4)))

    while len(password) < length_password:
        password.append(random.choice(total_chars))
    
    random.shuffle(password)
    
    senha = ''.join(password[:length_password])
    label_senha['text'] = senha
    evaluate_strength(senha)

# Função para avaliar a força da senha
def evaluate_strength(password):
    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password)) 
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    if length < 8:
        strength = "Fraca"
        color = "red"
    elif length < 12:
        if has_upper or has_lower or has_digit or has_special:
            strength = "Média"
            color = "orange"
        else:
            strength = "Fraca"
            color = "red"
    elif length < 16:
        if (has_upper and has_lower) or (has_digit and has_special):
            strength = "Forte"
            color = "yellow"
        else:
            strength = "Média"
            color = "orange"
    else:
        if has_upper and has_lower and has_digit and has_special:
            strength = "Muito Forte"
            color = "green"
        else:
            strength = "Forte"
            color = "yellow"

    label_strength['text'] = f"Força: {strength}"
    label_strength['fg'] = color

# Função para copiar a senha
def copy_password():
    password = label_senha['text']
    print(f"Senha gerada: {password}")
    if password:
        window.clipboard_clear()
        window.clipboard_append(password)
        window.update()
        messagebox.showinfo("Cópia", "Senha copiada para a área de transferência!")

# Função para garantir que pelo menos uma opção esteja marcada
def check_options():
    if not (var_symbols.get() or var_numbers.get() or var_uppercase.get() or var_downcase.get()):
        messagebox.showwarning("Atenção", "Você deve selecionar pelo menos uma opção.")
        if not var_uppercase.get():
            var_uppercase.set(True)
        elif not var_downcase.get():
            var_downcase.set(True)
        elif not var_numbers.get():
            var_numbers.set(True)
        elif not var_symbols.get():
            var_symbols.set(True)
    
    generate_password()

# Função para gerar uma nova senha quando o botão for clicado
def refresh_password():
    generate_password()

# Configuração da janela principal
window = tk.Tk()
window.title("Gerador de Senhas")
window.geometry("1280x720")
window.configure(bg="#f1f1f1")  # Cor de fundo da janela

# Título estilizado
titulo = tk.Label(window, text="Gerador de Senhas", font=("Helvetica", 30, "bold"), fg="#2c3e50", bg="#f1f1f1")
titulo.pack(pady=(30, 10))

# Label para exibir a senha gerada
label_senha = tk.Label(window, text="", font=("Courier", 24), bg="#e0e0e0", fg="#2c3e50", padx=10, pady=10, relief=tk.SUNKEN)
label_senha.pack(pady=20, padx=50, fill=tk.X)

# Label para exibir a força da senha
label_strength = tk.Label(window, text="Força: ", font=("Helvetica", 20), bg="#f1f1f1", fg="#2c3e50")
label_strength.pack(pady=10)

# Scale para escolher o tamanho da senha (8 a 32)
label_tamanho = tk.Label(window, text="Tamanho da senha:", font=("Helvetica", 18), fg="#2c3e50", bg="#f1f1f1")
label_tamanho.pack(pady=10)

length_scale = tk.Scale(window, from_=1, to=32, orient=tk.HORIZONTAL, font=("Helvetica", 16), bg="#f1f1f1", fg="#2c3e50", length=400, command=lambda value: generate_password())
length_scale.set(16)
length_scale.pack(pady=10)

# Criação de um frame para os checkbuttons
frame_options = tk.Frame(window, bg="#f1f1f1")
frame_options.pack(pady=20)

# Estilo para os Checkbuttons
checkbutton_style = {
    'font': ("Helvetica", 16),
    'bg': "#f1f1f1",
    'fg': "#2c3e50",
    'selectcolor': "#dfe6e9",
    'relief': tk.RAISED,
    'bd': 2
}

# Checkbutton para incluir letras maiúsculas
var_uppercase = tk.BooleanVar(value=True)
check_uppercase = tk.Checkbutton(frame_options, text="Maiúsculas", variable=var_uppercase, command=check_options, **checkbutton_style)
check_uppercase.grid(row=0, column=0, padx=20, pady=10)

# Checkbutton para incluir letras minúsculas
var_downcase = tk.BooleanVar(value=True)
check_downcase = tk.Checkbutton(frame_options, text="Minúsculas", variable=var_downcase, command=check_options, **checkbutton_style)
check_downcase.grid(row=0, column=1, padx=20, pady=10)

# Checkbutton para incluir caracteres especiais
var_symbols = tk.BooleanVar(value=True)
check_symbols = tk.Checkbutton(frame_options, text="Símbolos", variable=var_symbols, command=check_options, **checkbutton_style)
check_symbols.grid(row=0, column=2, padx=20, pady=10)

# Checkbutton para incluir números
var_numbers = tk.BooleanVar(value=True)
check_numbers = tk.Checkbutton(frame_options, text="Números", variable=var_numbers, command=check_options, **checkbutton_style)
check_numbers.grid(row=0, column=3, padx=20, pady=10)

# Botão para copiar a senha
btn_copy = tk.Button(window, text="Copiar Senha", command=copy_password, font=("Helvetica", 16), bg="#2ecc71", fg="white", relief=tk.RAISED)
btn_copy.pack(pady=20)

# Botão para gerar uma nova senha com um ícone de recarregar
btn_refresh = tk.Button(window, text="🔄 Gerar Senha", command=refresh_password, font=("Helvetica", 16), bg="#3498db", fg="white", relief=tk.RAISED)
btn_refresh.pack(pady=10)

# Gera a senha inicial
generate_password()

# Iniciar a interface
window.mainloop()
