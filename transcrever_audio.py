import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import os

# ──────────────────────────────────────────
#  VERIFICAÇÃO DE DEPENDÊNCIAS
# ──────────────────────────────────────────
def verificar_dependencias():
    faltando = []
    try:
        import whisper
    except ImportError:
        faltando.append("openai-whisper")
    try:
        import torch
    except ImportError:
        faltando.append("torch")
    return faltando

# ──────────────────────────────────────────
#  JANELA PRINCIPAL
# ──────────────────────────────────────────
class AppTranscricao:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ Transcritor de Áudio - Sandro")
        self.root.geometry("650x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        self.arquivo_selecionado = tk.StringVar(value="Nenhum arquivo selecionado")
        self.modelo_var = tk.StringVar(value="base")

        self._construir_interface()

    def _construir_interface(self):
        tk.Label(
            self.root, text="🎙️ Transcritor de Áudio",
            font=("Segoe UI", 16, "bold"), bg="#f0f4f8", fg="#2d3748"
        ).pack(pady=(20, 5))

        tk.Label(
            self.root, text="Powered by OpenAI Whisper",
            font=("Segoe UI", 9), bg="#f0f4f8", fg="#718096"
        ).pack()

        frame_arquivo = tk.Frame(self.root, bg="#f0f4f8")
        frame_arquivo.pack(pady=15, padx=30, fill="x")

        tk.Button(
            frame_arquivo, text="📂 Escolher Áudio",
            command=self.escolher_arquivo,
            font=("Segoe UI", 10, "bold"), bg="#4299e1", fg="white",
            relief="flat", padx=15, pady=8, cursor="hand2"
        ).pack(side="left")

        tk.Label(
            frame_arquivo, textvariable=self.arquivo_selecionado,
            font=("Segoe UI", 9), bg="#f0f4f8", fg="#4a5568",
            wraplength=400, anchor="w"
        ).pack(side="left", padx=10)

        frame_modelo = tk.Frame(self.root, bg="#f0f4f8")
        frame_modelo.pack(pady=5, padx=30, fill="x")

        tk.Label(
            frame_modelo, text="Modelo:",
            font=("Segoe UI", 10), bg="#f0f4f8", fg="#2d3748"
        ).pack(side="left")

        modelos = [("Rápido (base)", "base"), ("Equilibrado (small)", "small"), ("Preciso (medium)", "medium")]
        for texto, valor in modelos:
            tk.Radiobutton(
                frame_modelo, text=texto, variable=self.modelo_var, value=valor,
                font=("Segoe UI", 9), bg="#f0f4f8", fg="#2d3748",
                activebackground="#f0f4f8"
            ).pack(side="left", padx=8)

        tk.Label(
            self.root,
            text="💡 Dica: 'base' é mais rápido. 'medium' é mais preciso mas demora mais.",
            font=("Segoe UI", 8), bg="#f0f4f8", fg="#a0aec0"
        ).pack()

        self.btn_transcrever = tk.Button(
            self.root, text="▶️  Transcrever Agora",
            command=self.iniciar_transcricao,
            font=("Segoe UI", 11, "bold"), bg="#48bb78", fg="white",
            relief="flat", padx=20, pady=10, cursor="hand2"
        )
        self.btn_transcrever.pack(pady=15)

        self.status_var = tk.StringVar(value="Aguardando arquivo...")
        self.label_status = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Segoe UI", 9, "italic"), bg="#f0f4f8", fg="#718096",
            wraplength=600
        )
        self.label_status.pack()

        tk.Label(
            self.root, text="📄 Transcrição:",
            font=("Segoe UI", 10, "bold"), bg="#f0f4f8", fg="#2d3748"
        ).pack(anchor="w", padx=30, pady=(10, 2))

        self.texto_resultado = scrolledtext.ScrolledText(
            self.root, font=("Segoe UI", 10), wrap="word",
            width=72, height=8, relief="solid", bd=1
        )
        self.texto_resultado.pack(padx=30, pady=(0, 10))

        frame_botoes = tk.Frame(self.root, bg="#f0f4f8")
        frame_botoes.pack(pady=5)

        tk.Button(
            frame_botoes, text="💾 Salvar .txt",
            command=self.salvar_txt,
            font=("Segoe UI", 9), bg="#667eea", fg="white",
            relief="flat", padx=12, pady=6, cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes, text="📋 Copiar Texto",
            command=self.copiar_texto,
            font=("Segoe UI", 9), bg="#ed8936", fg="white",
            relief="flat", padx=12, pady=6, cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes, text="📁 Abrir Pasta",
            command=self.abrir_pasta,
            font=("Segoe UI", 9), bg="#38b2ac", fg="white",
            relief="flat", padx=12, pady=6, cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes, text="🗑️ Limpar",
            command=self.limpar,
            font=("Segoe UI", 9), bg="#fc8181", fg="white",
            relief="flat", padx=12, pady=6, cursor="hand2"
        ).pack(side="left", padx=5)

    def escolher_arquivo(self):
        tipos = [
            ("Áudios", "*.mp3 *.wav *.m4a *.ogg *.flac *.mp4 *.webm"),
            ("Todos", "*.*")
        ]
        caminho = filedialog.askopenfilename(title="Selecione o arquivo de áudio", filetypes=tipos)
        if caminho:
            self.caminho_arquivo = caminho
            nome = os.path.basename(caminho)
            self.arquivo_selecionado.set(f"✅ {nome}")
            self.status_var.set("Arquivo pronto. Clique em 'Transcrever'.")

    def iniciar_transcricao(self):
        if not hasattr(self, "caminho_arquivo") or not self.caminho_arquivo:
            messagebox.showwarning("Atenção", "Selecione um arquivo de áudio primeiro!")
            return

        self.btn_transcrever.config(state="disabled", text="⏳ Transcrevendo...")
        self.status_var.set("Carregando modelo Whisper... aguarde.")
        self.texto_resultado.delete("1.0", "end")

        thread = threading.Thread(target=self.transcrever, daemon=True)
        thread.start()

    def transcrever(self):
        try:
            import whisper

            modelo_nome = self.modelo_var.get()
            self.root.after(0, lambda: self.status_var.set(f"Carregando modelo '{modelo_nome}'... aguarde."))

            modelo = whisper.load_model(modelo_nome)

            self.root.after(0, lambda: self.status_var.set("Transcrevendo... isso pode levar alguns minutos."))

            resultado = modelo.transcribe(self.caminho_arquivo, language="pt")
            texto = resultado["text"].strip()

            self.root.after(0, lambda t=texto: self._exibir_resultado(t))

        except Exception as e:
            msg = str(e)
            self.root.after(0, lambda m=msg: self._erro(m))

    def _exibir_resultado(self, texto):
        self.texto_resultado.insert("1.0", texto)
        self.btn_transcrever.config(state="normal", text="▶️  Transcrever Agora")

        # Salva automaticamente na mesma pasta do áudio
        try:
            pasta = os.path.dirname(self.caminho_arquivo)
            nome_base = os.path.splitext(os.path.basename(self.caminho_arquivo))[0]
            self.caminho_txt_salvo = os.path.join(pasta, f"{nome_base}_transcricao.txt")
            with open(self.caminho_txt_salvo, "w", encoding="utf-8") as f:
                f.write(texto)
            self.status_var.set(f"✅ Salvo automaticamente: {self.caminho_txt_salvo}")
        except Exception:
            self.caminho_txt_salvo = None
            self.status_var.set("✅ Concluído! Use 'Salvar .txt' para exportar.")

    def _erro(self, msg):
        self.status_var.set("❌ Erro na transcrição.")
        self.btn_transcrever.config(state="normal", text="▶️  Transcrever Agora")
        messagebox.showerror("Erro", f"Ocorreu um erro:\n\n{msg}\n\nVerifique se o Whisper está instalado:\npip install openai-whisper")

    def salvar_txt(self):
        texto = self.texto_resultado.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Vazio", "Não há texto para salvar.")
            return

        nome_inicial = "transcricao"
        pasta_inicial = "/"
        if hasattr(self, "caminho_arquivo"):
            nome_inicial = os.path.splitext(os.path.basename(self.caminho_arquivo))[0] + "_transcricao"
            pasta_inicial = os.path.dirname(self.caminho_arquivo)

        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")],
            initialfile=nome_inicial,
            initialdir=pasta_inicial
        )
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(texto)
            messagebox.showinfo("Salvo!", f"Arquivo salvo em:\n{caminho}")

    def copiar_texto(self):
        texto = self.texto_resultado.get("1.0", "end").strip()
        if texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            messagebox.showinfo("Copiado!", "Texto copiado para a área de transferência!")

    def abrir_pasta(self):
        pasta = None
        if hasattr(self, "caminho_arquivo"):
            pasta = os.path.dirname(self.caminho_arquivo)
        if pasta and os.path.exists(pasta):
            os.startfile(pasta)
        else:
            messagebox.showinfo("Pasta", "Selecione um arquivo primeiro.")

    def limpar(self):
        self.texto_resultado.delete("1.0", "end")
        self.arquivo_selecionado.set("Nenhum arquivo selecionado")
        self.status_var.set("Aguardando arquivo...")
        if hasattr(self, "caminho_arquivo"):
            del self.caminho_arquivo
        if hasattr(self, "caminho_txt_salvo"):
            del self.caminho_txt_salvo

# ──────────────────────────────────────────
#  INICIAR
# ──────────────────────────────────────────
if __name__ == "__main__":
    faltando = verificar_dependencias()
    if faltando:
        root_temp = tk.Tk()
        root_temp.withdraw()
        libs = ", ".join(faltando)
        messagebox.showerror(
            "Dependências não encontradas",
            f"Instale as bibliotecas necessárias no terminal:\n\n"
            f"pip install openai-whisper\n\n"
            f"Faltando: {libs}"
        )
        root_temp.destroy()
    else:
        root = tk.Tk()
        app = AppTranscricao(root)
        root.mainloop()
