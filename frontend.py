import streamlit as st
import requests

st.title("Generador de CV en PDF con IA")

# Datos personales
nombre = st.text_input("Nombre Completo")
puesto = st.text_input("Puesto Ocupado/Buscado")
ciudad = st.text_input("Ciudad")
correo = st.text_input("Correo Electrónico")
telefono = st.text_input("Teléfono")

# Perfil
perfil = st.text_area("Perfil Profesional")

# Experiencia Laboral
st.subheader("Experiencia Laboral")
experiencia = []
num_exp = st.number_input("Número de experiencias laborales", min_value=0, step=1)
for i in range(num_exp):
    with st.expander(f"Experiencia {i+1}"):
        puesto_exp = st.text_input(f"Puesto", key=f"puesto_{i}")
        empresa = st.text_input(f"Empresa", key=f"empresa_{i}")
        fecha = st.text_input(f"Fecha", key=f"fecha_exp_{i}")
        descripcion = st.text_area(f"Descripción", key=f"descripcion_exp_{i}")
        experiencia.append({"puesto": puesto_exp, "empresa": empresa, "fecha": fecha, "descripcion": descripcion})

# Educación
st.subheader("Educación")
educacion = []
num_edu = st.number_input("Número de estudios", min_value=0, step=1)
for i in range(num_edu):
    with st.expander(f"Educación {i+1}"):
        titulo = st.text_input(f"Título", key=f"titulo_{i}")
        institucion = st.text_input(f"Institución", key=f"institucion_{i}")
        fecha = st.text_input(f"Fecha", key=f"fecha_edu_{i}")
        educacion.append({"titulo": titulo, "institucion": institucion, "fecha": fecha})

# Habilidades e Idiomas
habilidades = st.text_area("Habilidades (separadas por comas)")
idiomas = st.text_area("Idiomas (separados por comas)")

# Botón para generar CV
if st.button("Generar CV"):
    datos = {
        "nombre": nombre,
        "puesto": puesto,
        "ciudad": ciudad,
        "correo": correo,
        "telefono": telefono,
        "perfil": perfil,
        "experiencia": experiencia,
        "educacion": educacion,
        "habilidades": habilidades,
        "idiomas": idiomas
    }
    respuesta = requests.post("http://127.0.0.1:5000/generar_cv", json=datos)
    if respuesta.status_code == 200:
        st.success("CV generado con éxito. Descarga el archivo abajo.")
        with open("cv_generado.pdf", "rb") as pdf_file:
            st.download_button("Descargar CV en PDF", pdf_file, file_name="CV.pdf", mime="application/pdf")
    else:
        st.error("Hubo un error al generar el CV.")

