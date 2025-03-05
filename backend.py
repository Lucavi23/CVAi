from flask import Flask, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
import textwrap

app = Flask(__name__)

styles = getSampleStyleSheet()
justify_style = ParagraphStyle(
    name="Justify",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,  # Espaciado entre líneas
    alignment=TA_JUSTIFY,  # Justificación del texto
)

def generar_cv(datos):
    file_path = "cv_generado.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', fontSize=20, textColor=colors.black, spaceAfter=14, fontName="Helvetica-Bold")
    subtitle_style = ParagraphStyle('Subtitle', fontSize=14, textColor=colors.grey, spaceAfter=10,
                                    fontName="Helvetica-Bold")
    normal_style = ParagraphStyle('Normal', fontSize=11, textColor=colors.black, spaceAfter=5, fontName="Helvetica")
    section_title_style = ParagraphStyle('SectionTitle', fontSize=12, textColor=colors.black, spaceAfter=8,
                                         fontName="Helvetica-Bold")

    # Datos personales
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, 780, datos["nombre"])

    c.setFont("Helvetica", 14)
    c.setFillColor(colors.grey)
    c.drawString(50, 760, datos["puesto"])

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(400, 780, datos["telefono"])
    c.drawString(400, 765, datos["ciudad"])
    c.drawString(400, 750, datos["correo"])

    # Línea separadora
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.line(50, 735, 550, 735)

    # Secciones
    y_position = 710

    def draw_section(title, content, is_list=False, max_width=110):
        nonlocal y_position
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawString(50, y_position, title)
        y_position -= 15

        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)

        if isinstance(content, list):
            if title == "HABILIDADES":
                # Imprimir todas las habilidades en una sola línea separadas por " | "
                habilidades_texto = " | ".join(content)
                lines = [habilidades_texto[i:i + max_width] for i in range(0, len(habilidades_texto), max_width)]
                for line in lines:
                    c.drawString(50, y_position, line)
                    y_position -= 12  # Espaciado entre líneas
            else:
                for item in content:
                    if isinstance(item, dict):  # Si es experiencia laboral o educación
                        # Imprimir el título en negrita
                        c.setFont("Helvetica-Bold", 10)
                        c.drawString(50, y_position, item.get('titulo', 'Sin título'))
                        y_position -= 12

                        # Imprimir la institución y la fecha en texto normal
                        c.setFont("Helvetica", 10)
                        c.drawString(50, y_position,
                                     f"{item.get('institucion', 'Sin institución')} ({item.get('fecha', 'Sin fecha')})")
                        y_position -= 15

                        # Envuelve la descripción en líneas más cortas
                        wrapped_text = textwrap.wrap(item.get("descripcion", ""), width=max_width)
                        for line in wrapped_text:
                            c.drawString(60, y_position, line)
                            y_position -= 12
                        y_position -= 10  # Espaciado entre bloques

                    else:  # Para listas de habilidades, idiomas, etc.
                        c.drawString(50, y_position, f"• {item}")
                        y_position -= 15
        else:
            wrapped_text = textwrap.wrap(str(content), width=max_width)
            for line in wrapped_text:
                c.drawString(50, y_position, line)
                y_position -= 12
            y_position -= 15  # Espaciado extra después de cada sección

    draw_section("PERFIL", datos["perfil"])
    draw_section("EXPERIENCIA PROFESIONAL", datos["experiencia"], is_list=True)
    draw_section("EDUCACIÓN", datos["educacion"], is_list=True)
    draw_section("HABILIDADES", datos["habilidades"].split(", "))
    draw_section("IDIOMAS", datos["idiomas"].split(", "))

    c.save()
    return file_path


@app.route("/generar_cv", methods=["POST"])
def generar_cv_endpoint():
    datos = request.json
    cv_file = generar_cv(datos)
    return send_file(cv_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)


