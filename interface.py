import tkinter as tk
from tkinter import filedialog
import subprocess

def escolher_imagem():
    caminho = filedialog.askopenfilename(
        title="Escolha uma imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
    )
    if caminho:
        subprocess.run(["python3", "main.py", caminho])

def iniciar_interface():
    root = tk.Tk()
    root.title("Imagem para Música 🎼")
    root.geometry("300x150")

    label = tk.Label(root, text="Escolha uma imagem para gerar música 🎵", wraplength=250)
    label.pack(pady=20)

    botao = tk.Button(root, text="Selecionar Imagem", command=escolher_imagem)
    botao.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
