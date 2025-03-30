import streamlit as st
import pandas as pd
import pyqrcode
import smtplib
import pyperclip
from email.mime.text import MIMEText
from io import BytesIO
import base64
from gerador_pix import Payload, gerarPayload, gerarCrc16

# Configurações iniciais
CSV_URL = "presentes.csv"  # Substitua pelo URL real
#nome = "PEDRO WILLIAM RIBEIRO DINIZ"
chavepix = "08036122650"
#valor = '1.00'
#cidade = "BELO HORIZONTE"
#txtId = "DESCRIÇÃO"
#fileNameQrcode = "teste.png"
OWNER_EMAIL = "pedrowilliamrd@gmail.com"


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



def generate_pix_code(valor_total):
    """
    Função simplificada para gerar uma string de código PIX e um QR Code.
    Em produção, utilize uma implementação que siga o padrão do Pix.
    """
    # Formatação simples: combine chave e valor (apenas para exemplificar)
    #pix_data = f"00020126580014br.gov.bcb.pix0136{PIX_KEY}5204000053039865802BR5913{NOME}6014{CIDADE}62070503***63041234"
    #qr = pyqrcode.create(pix_data)
    #return pix_data, qr
    pass


def send_email(subject, message):
    """
    Função para enviar e-mail com os detalhes da compra.
    Utilize variáveis de ambiente ou o Secret Manager do Streamlit para armazenar credenciais.
    """
    sender_email = "pedrowilliamrd@gmail.com"
    sender_password = st.secrets["app_password"]
    
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = OWNER_EMAIL
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")
        return False
    

def main():
    # Add banner class to the main container
    st.markdown('<div class="banner">', unsafe_allow_html=True)
    
    # Load custom CSS
    local_css("style.css")

    # Title with custom styling
    st.markdown('<h1><span class="estilo1">Chá</span><span class="estilo2">DO JOCA</span><span class="estilo3"> e despedida da Rua Pompeia</span></h1>', unsafe_allow_html=True)
    st.markdown('<p>05 de abril</p>', unsafe_allow_html=True)
    st.markdown('<p>12h</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.5em;">Rua Pompeia, n 10 - Prado</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.5em;">Tocar 100 no interfone</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.5em;">Lista de Presentes</p>', unsafe_allow_html=True)

    # Carregar dados do CSV hospedado no GitHub
    try:
        df = pd.read_csv(CSV_URL, sep=";")
    except Exception as e:
        st.error("Erro ao carregar a lista de produtos. Verifique o URL do CSV.")
        return

    # Exibir a tabela de produtos
    st.markdown('<h2>Produtos Disponíveis</h2>', unsafe_allow_html=True)

    # Seleção do produto
    produtos = df["Presente"].tolist()
    produto_selecionado = st.selectbox("Escolha o presente:", produtos)

    # Obter detalhes do produto selecionado
    produto_info = df[df["Presente"] == produto_selecionado].iloc[0]
    quantidade_disponivel = int(produto_info["Quantidade"])
    valor_unitario = float(produto_info["Valor"])

    st.write(f"**Quantidade disponível:** {quantidade_disponivel}")
    st.write(f"**Valor Unitário:** R$ {valor_unitario:.2f}")

    # Entrada para a quantidade desejada
    quantidade = st.number_input("Informe a quantidade desejada:", min_value=1, 
                                   max_value=quantidade_disponivel, value=1, step=1)
    
    # Calcular o valor total da compra
    valor_total = valor_unitario * quantidade
    st.write(f"**Valor Total:** R$ {valor_total:.2f}")

    # Gerar código PIX e QR Code
    # pix_code, qr = generate_pix_code(valor_total)

    # Gerar QR code para pagamento PIX
    #payload = Payload(nome = "PEDRO WILLIAM RIBEIRO DINIZ", chavepix = "07174603637", valor = valor_total, cidade = "SAO PAULO", txtId = "DESCRIÇÃO", fileNameQrcode = "teste.png")

    st.markdown('<h2>Chave PIX para Pagamento</h2>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.5em;">Clique no ícone no canto direito do campo abaixo para copiar a chave!</p>', unsafe_allow_html=True)
    st.code(chavepix, language="text")


    # Formulário para enviar dados da compra e mensagem
    st.markdown('<h2>Deixe um recadinho!</h2>', unsafe_allow_html=True)
    st.markdown('<p>Ao final, clique no botão "Confirme o envio do seu presente!". É muito importante para que nós consigamos fazer o controle.</p>', unsafe_allow_html=True)
    st.markdown('<p>Os papais e o baby Joca agradecem muito seu presente 🤍👶🤍 </p>', unsafe_allow_html=True)
    
    nome_presenteante = st.text_input("Digite seu nome:")
    mensagem = st.text_area("Digite sua mensagem (opcional):", max_chars=200)
    enviar = st.button("Confirme o envio do seu presente!")
    
    if enviar:
        subject = "Nova Compra Realizada"
        # Junta o nome e a mensagem
        email_message = (
            f"Produto: {produto_selecionado}\n"
            f"Quantidade: {quantidade}\n"
            f"Valor Total: R$ {valor_total:.2f}\n\n"
            f"Presenteante: {nome_presenteante}\n"
            f"Mensagem: {mensagem}"
        )
        if send_email(subject, email_message):
            st.success("Seu presente para o Joca foi confirmado! 👶🎁")
        else:
            st.error("Ocorreu um problema ao enviar o e-mail.")
    
    # Close the banner div
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()