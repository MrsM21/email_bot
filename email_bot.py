import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Função para criar mensagem personalizada
def criar_mensagem(nome, valor, vencimento):
    return f"""Olá {nome},

Este é um lembrete do seu pagamento de R$ {valor:.2f}, com vencimento em {vencimento}.

Por favor, entre em contato se tiver dúvidas.

Atenciosamente,
Sua Empresa
"""


# Função para enviar e-mail
def enviar_email(destinatario, assunto, mensagem):
    import os
from dotenv import load_dotenv
load_dotenv()

remetente = os.getenv("EMAIL_REMETENTE")
senha = os.getenv("SENHA_DO_APP")


    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(mensagem, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
        print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar para {destinatario}: {e}")


# Leitura da planilha e envio
df = pd.read_excel("clientes.xlsx")

for _, row in df.iterrows():
    nome = row["Nome"]
    email = row["Email"]
    valor = row["Valor"]
    vencimento = row["Vencimento"]

    corpo_email = criar_mensagem(nome, valor, vencimento)
    enviar_email(email, "Lembrete de Pagamento", corpo_email)
