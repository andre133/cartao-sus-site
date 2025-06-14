from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Carrega a fonte (ajuste o caminho conforme necessário)
try:
    font = ImageFont.truetype("arial.ttf", 40)
    small_font = ImageFont.truetype("arial.ttf", 18)
except:
    # Fallback para fonte padrão
    font = ImageFont.load_default()
    small_font = ImageFont.load_default()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Recebe dados do formulário
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    sexo = request.form['sexo']
    cns = request.form['cns']

    # Carrega a imagem base
    base_image = Image.open('static/cartao_base.jpg')
    draw = ImageDraw.Draw(base_image)

    # Adiciona os dados à imagem
    draw.text((150, 100), nome, fill="black", font=font)  # Nome
    draw.text((150, 180), data_nascimento, fill="black", font=font)  # Data Nascimento
    draw.text((400, 180), sexo, fill="black", font=font)  # Sexo
    draw.text((150, 260), cns, fill="black", font=small_font)  # CNS

    # Gera código de barras
    barcode_buffer = BytesIO()
    code128 = barcode.get('code128', cns, writer=ImageWriter())
    code128.write(barcode_buffer)
    
    # Adiciona código de barras à imagem
    barcode_img = Image.open(barcode_buffer)
    barcode_img = barcode_img.resize((400, 100))
    base_image.paste(barcode_img, (150, 300))

    # Salva imagem modificada
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_cartao.jpg')
    base_image.save(img_path)

    # Gera PDF
    pdf_buffer = generate_pdf(img_path)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name='cartao_sus.pdf',
        mimetype='application/pdf'
    )

def generate_pdf(image_path):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Adiciona imagem ao PDF
    c.drawImage(image_path, 50, 300, width=500, height=300)
    c.save()
    
    buffer.seek(0)
    return buffer

if __name__ == '__main__':
    app.run(debug=True)
