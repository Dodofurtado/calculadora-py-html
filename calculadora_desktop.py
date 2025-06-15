import tkinter as tk
from tkinter import ttk
import math

class CalculadoraModerna:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Calculadora Moderna")
        self.janela.configure(bg='#2c2f34')
        
        # Configuração do estilo
        style = ttk.Style()
        style.configure('Modern.TButton', padding=10, font=('Segoe UI', 12))
        style.configure('Display.TEntry', padding=10, font=('Segoe UI', 16))
        
        # Display
        self.display = ttk.Entry(self.janela, justify='right', style='Display.TEntry')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        
        # Botões
        botoes = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        row = 1
        col = 0
        for botao in botoes:
            cmd = lambda x=botao: self.click(x)
            btn = ttk.Button(self.janela, text=botao, command=cmd, style='Modern.TButton')
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Botão Limpar
        ttk.Button(self.janela, text='C', command=self.limpar, style='Modern.TButton').grid(row=row, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        
        # Configurar o redimensionamento
        for i in range(4):
            self.janela.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.janela.grid_rowconfigure(i, weight=1)
            
        # Definir tamanho mínimo da janela
        self.janela.minsize(300, 400)

    def click(self, key):
        if key == '=':
            try:
                resultado = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(resultado))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Erro")
        else:
            self.display.insert(tk.END, key)

    def limpar(self):
        self.display.delete(0, tk.END)

    def iniciar(self):
        self.janela.mainloop()

if __name__ == '__main__':
    calc = CalculadoraModerna()
    calc.iniciar()
