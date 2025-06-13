from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)

@app.route('/gerar-cartao', methods=['POST'])
def gerar_cartao():
    data = request.json
    nome = data.get("nome", "")
    nascimento = data.get("nascimento", "")
    sexo = data.get("sexo", "")
    cns = data.get("cns", "")

    # Criação da imagem base
    img = Image.new("RGB", (800, 400), "white")
    draw = ImageDraw.Draw(img)

    # Carregando fontes
    fonte_regular = ImageFont.truetype("Roboto-Regular.ttf", size=28)
    fonte_bold = ImageFont.truetype("Roboto-Bold.ttf", size=32)
    fonte_cns = ImageFont.truetype("Roboto-Bold.ttf", size=48)

    # Escrevendo nome
    draw.text((50, 50), nome, font=fonte_bold, fill="black")

    # Nascimento e Sexo na mesma linha
    draw.text((50, 100), f"Data de Nasc.: {nascimento}   Sexo: {sexo}", font=fonte_regular, fill="black")

    # CNS com fonte maior
    draw.text((50, 160), cns, font=fonte_cns, fill="black")

    # Gerando código de barras
    codigo = barcode.get("code128", cns, writer=ImageWriter())
    buffer = io.BytesIO()
    codigo.write(buffer, {"module_height": 10.0, "font_size": 12})
    buffer.seek(0)
    codigo_img = Image.open(buffer)

    # Colando código de barras na imagem
    img.paste(codigo_img, (50, 240))

    # Retornar como arquivo
    final_buffer = io.BytesIO()
    img.save(final_buffer, format="PNG")
    final_buffer.seek(0)

    return send_file(final_buffer, mimetype="image/png", as_attachment=True, download_name="cartao_cns.png")

if __name__ == "__main__":
    app.run(debug=True)
