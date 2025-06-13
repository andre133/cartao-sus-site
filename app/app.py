from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar", methods=["POST"])
def gerar():
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    nascimento = request.form["nascimento"]

    imagem = Image.new("RGB", (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(imagem)

    # Usar fonte que está na pasta "fonts"
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    font = ImageFont.truetype(font_path, 16)

    draw.text((10, 50), f"Nome: {nome}", font=font, fill=(0, 0, 0))
    draw.text((10, 80), f"CPF: {cpf}", font=font, fill=(0, 0, 0))
    draw.text((10, 110), f"Nascimento: {nascimento}", font=font, fill=(0, 0, 0))

    output = io.BytesIO()
    imagem.save(output, format="PNG")
    output.seek(0)

    return send_file(output, mimetype="image/png")
