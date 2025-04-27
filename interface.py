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
    
    largura_janela = 300
    altura_janela = 150

    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)

    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    root.configure(bg="#000000")


    label = tk.Label(root, text="Escolha uma imagem para gerar música 🎵",
                     font=("Helvetica", 12, "bold"), wraplength=250, bg = "#000000", fg="white")
    label.pack(pady=20)

    botao = tk.Button(root, text="Selecionar Imagem", font=("Helvetica", 10, "bold"), bg="#1B1212", fg="white", 
                      activebackground="#000000", padx=10, pady=5, command=escolher_imagem)
    botao.pack(pady=10)

    def on_enter(e):
        botao['background'] = '#45a049'

    def on_leave(e):
        botao['background'] = '#1B1212'

    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
