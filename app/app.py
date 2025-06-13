
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar", methods=["POST"])
def gerar():
    nome = request.form["nome"]
    nascimento = request.form["nascimento"]
    sexo = request.form["sexo"]
    cns = request.form["cns"]

    base = Image.open("app/static/cartao_sus_base.png").convert("RGB")
    draw = ImageDraw.Draw(base)

    font = ImageFont.truetype("arial.ttf", 16)
    big_font = ImageFont.truetype("arial.ttf", 18)

    draw.text((160, 160), nome, font=font, fill="black")
    draw.text((160, 190), f"Data de Nasc.: {nascimento}    Sexo: {sexo}", font=font, fill="black")
    draw.text((160, 220), cns, font=big_font, fill="black")

    # Gerar código de barras do CNS
    code128 = barcode.get('code128', cns, writer=ImageWriter())
    barcode_path = "app/static/codigo.png"
    code128.save(barcode_path[:-4])

    codigo = Image.open(barcode_path).resize((300, 80))
    base.paste(codigo, (160, 250))

    output_path = "app/static/cartao_gerado.png"
    base.save(output_path)
    return send_file(output_path, mimetype="image/png")
