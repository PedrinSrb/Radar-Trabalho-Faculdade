
import subprocess
import sys

# Instala bibliotecas se faltar
pacotes = ["reportlab", "qrcode", "pillow"]
for pacote in pacotes:
    try:
        __import__(pacote)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

# Importações
import re
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import qrcode
from PIL import Image
import os

# Funções
def classificar_multa(diferenca):
    if 1 <= diferenca <= 20:
        return "Leve", 88.38, 0
    elif 21 <= diferenca <= 30:
        return "Média", 130.16, 4
    elif 31 <= diferenca <= 50:
        return "Grave", 195.23, 5
    elif diferenca > 50:
        return "Gravíssima", 880.41, 7
    else:
        return None, 0.0, 0

def input_placa():
    while True:
        placa = input("Digite a placa do veículo (Mercosul ex: ABC1D23 ou Antiga ex: ABC1234): ").strip().upper()
        if re.fullmatch(r"[A-Z]{3}[0-9]{4}", placa):
            return placa, "Antiga"
        elif re.fullmatch(r"[A-Z]{3}[0-9][A-Z][0-9]{2}", placa):
            return placa, "Mercosul"
        else:
            print("❌ Placa inválida! Formatos válidos: ABC1234 ou ABC1D23")

# 🔹 INPUTS do usuário
placa, formato_placa = input_placa()
velocidade = float(input("Digite a velocidade registrada (km/h): "))
limite = int(input("Digite o limete da via (km/h): "))

# Simula dados
motoristas = [
    ("João da Silva", "123.456.789-00"),
    ("Maria Oliveira", "987.654.321-11"),
    ("Carlos Souza", "456.123.789-22"),
    ("Ana Beatriz", "789.321.654-33")
]
nome_motorista, cpf_motorista = random.choice(motoristas)
diferenca = velocidade - limite
tipo, valor, pontos = classificar_multa(diferenca)
ruas = [
    "Av. Cardoso Moreira", "Rua Dez de Maio", "Rua Rui Barbosa",
    "Rua Francisco Sá", "Rua Thomaz Teixeira dos Santos"
]
nome_rua = random.choice(ruas)
data_infracao = datetime.now()
data_infracao_formatada = data_infracao.strftime("%d/%m/%Y %H:%M")
vencimento = (data_infracao + timedelta(days=30)).strftime("%d/%m/%Y")
numero_ait = f"AIT-{random.randint(2025000000, 2025999999)}"

# Exibir no terminal
print(f"\n📋 Infração registrada:")
print(f"Placa: {placa} (Formato: {formato_placa})")
print(f"Tipo: {tipo}")
print(f"Valor da multa: R$ {valor:.2f}")
print(f"Pontos na CNH: {pontos}")

# Gera QR Code
url_multa = f"https://detran.rj.gov.br/multas/{placa}"
qr_img = qrcode.make(url_multa)
qr_path = "qr_temp.png"
qr_img.save(qr_path)

# Criar PDF
pdf_path = f"Multa_{placa}_completa.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)

# Cabeçalho
c.setFont("Helvetica-Bold", 16)
c.drawString(120, 800, "PREFEITURA MUNICIPAL DE ITAPERUNA")
c.setFont("Helvetica-Bold", 14)
c.drawString(150, 780, "DETRAN - Departamento de Trânsito do RJ")

# Dados principais
c.setFont("Helvetica", 12)
c.drawString(50, 750, f"Auto de Infração de Trânsito – {numero_ait}")
c.line(50, 745, 550, 745)

# Informações do motorista
c.drawString(50, 720, f"Nome do condutor: {nome_motorista}")
c.drawString(50, 700, f"CPF: {cpf_motorista}")
c.drawString(50, 680, f"Placa: {placa} (Formato: {formato_placa})")
c.drawString(50, 660, f"Rua: {nome_rua}, Itaperuna - RJ")
c.drawString(50, 640, f"Data e hora da infração: {data_infracao_formatada}")

# Detalhes da infração
c.line(50, 630, 550, 630)
c.drawString(50, 610, f"Velocidade medida: {velocidade} km/h")
c.drawString(50, 590, f"Velocidade permitida: {limite} km/h")
c.drawString(50, 570, f"Infração: {tipo}")
c.drawString(50, 550, f"Valor da multa: R$ {valor:.2f}")
c.drawString(50, 530, f"Pontos na CNH: {pontos}")
c.drawString(50, 510, f"Data de vencimento para pagamento: {vencimento}")

# QR Code
c.drawImage(qr_path, 400, 600, width=40*mm, height=40*mm)

# Rodapé
c.setFont("Helvetica-Oblique", 10)
c.drawString(50, 100, "Escaneie o QR Code para consultar detalhes da infração.")
c.drawString(50, 85, "Este documento é gerado automaticamente pelo sistema de monitoramento eletrônico de trânsito.")


c.save()
os.remove(qr_path)

print(f"\n✅ PDF gerado com sucesso: {pdf_path}")
