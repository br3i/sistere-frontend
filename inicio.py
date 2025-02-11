import streamlit as st

# Configurar el título y subtítulo para hacer la página más atractiva
st.title("¡Bienvenido a la Aplicación!")
st.subheader("Elige una opción para empezar")

# Añadir enlaces con botones estilizados
col1, col2 = st.columns(2)

with col1:
    if st.button("🤖 Asistente", key="asistente", use_container_width=True):
        st.switch_page("pages/assistant.py")

with col2:
    if st.button("📁 Administración", key="dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")


# O si quieres agregar algún mensaje adicional o información útil
st.text(
    "Si tienes alguna duda o necesitas ayuda, no dudes en consultar el asistente o el área de administración."
)
