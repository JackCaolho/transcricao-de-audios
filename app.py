import os
import speech_recognition as sr
from pydub import AudioSegment

pasta_entrada = "Amostra de Dados"
pasta_saida = "Amostras extraidas"
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)


recognizer = sr.Recognizer()

# Percorrer todos os arquivos
for filename in os.listdir(pasta_entrada):
    if filename.endswith(".wav"):
        caminho_arquivo = os.path.join(pasta_entrada, filename)
        
        # Converter o arquivo para o formato certo
        audio = AudioSegment.from_wav(caminho_arquivo)
        caminho_temporario = "temp.flac"
        audio.export(caminho_temporario, format="flac")

        # Recognizer entra em ação
        with sr.AudioFile(caminho_temporario) as source:
            audio_data = recognizer.record(source)
            try:
                texto = recognizer.recognize_google(audio_data, language="pt-BR")
            except sr.UnknownValueError:
                texto = "Não foi possível transcrever o áudio"
            except sr.RequestError:
                texto = "Erro na solicitação de reconhecimento de fala"

        # Salvando as transcriçoes
        nome_arquivo_txt = os.path.splitext(filename)[0] + ".txt"
        caminho_saida = os.path.join(pasta_saida, nome_arquivo_txt)
        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(texto)

        # drop arquivos temporários
        os.remove(caminho_temporario)

print("Transcrição concluída.")

