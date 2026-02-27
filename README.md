# 🎙️ Transcrever Áudio para TXT

Aplicativo com interface gráfica para transcrever arquivos de áudio em texto, utilizando o modelo **Whisper da OpenAI** — funciona 100% offline, sem enviar dados para a internet.

## 📋 O que faz

- Abre uma interface gráfica simples e intuitiva
- Suporta os formatos: `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.mp4`, `.webm`
- Transcreve o áudio em português automaticamente
- Salva o resultado em um arquivo `.txt` na mesma pasta do áudio
- Permite copiar o texto ou salvar em outro local

## ⚙️ Requisitos

- Python 3.x instalado
- Bibliotecas necessárias:

```bash
pip install openai-whisper torch
```

> ⚠️ A instalação do `torch` pode demorar alguns minutos pois é um arquivo grande.

## 🚀 Como usar

1. Instale as dependências acima
2. Execute o script:
```bash
python transcrever_audio.py
```
3. Clique em **"Escolher Áudio"** e selecione o arquivo
4. Escolha o modelo de transcrição:
   - **base** → mais rápido
   - **small** → equilibrado
   - **medium** → mais preciso, porém mais lento
5. Clique em **"Transcrever Agora"**
6. O arquivo `.txt` será salvo automaticamente na mesma pasta do áudio

## 🗂️ Arquivos

| Arquivo | Descrição |
|---|---|
| `transcrever_audio.py` | Script principal com interface gráfica |

## 💡 Observações

- Na primeira execução, o modelo Whisper será baixado automaticamente
- Arquivos de áudio longos podem demorar mais para transcrever
- O modelo `medium` oferece melhor precisão para o português
