import streamlit as st
import pandas as pd
import random
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from modules.reports.utils.get_feedback_reports import (
    get_scores_distribution,
    get_feedback_types,
    get_docs_satisfaction,
    get_response_quality_metrics,
    get_low_score_words,
    get_high_score_contexts,
    get_feedback_summary,
)
from helpers.colors_reports import colors_allowed, get_opposite_bright_color


def fetch_feedback_data(n_feedbacks):
    return {
        "scores_distribution": get_scores_distribution(n_feedbacks),
        "feedback_types": get_feedback_types(n_feedbacks),
        "docs_satisfaction": get_docs_satisfaction(n_feedbacks),
        "response_quality": get_response_quality_metrics(n_feedbacks),
        "low_score_words": get_low_score_words(n_feedbacks),
        "high_score_contexts": get_high_score_contexts(n_feedbacks),
        "feedback_summary": get_feedback_summary(n_feedbacks),
    }


def display_scores_distribution(scores_data):
    if scores_data:
        st.subheader("Distribución de Scores por Modelo LLM")
        df = pd.DataFrame(scores_data)

        # Gráfico de barras agrupadas
        pivot_df = df.pivot_table(
            index="model_name", columns="score", values="count", fill_value=0
        )
        st.bar_chart(pivot_df)

        # Gráfico circular para distribución general
        fig, ax = plt.subplots()
        df.groupby("score")["count"].sum().plot.pie(y="count", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.warning("No hay datos de puntuaciones disponibles.")


def display_feedback_types(feedback_data):
    if feedback_data:
        st.subheader("Tipos de Feedback por Modelo")
        df = pd.DataFrame(feedback_data)
        colors = random.sample(colors_allowed, 3)

        # Gráfico de barras apiladas
        pivot_df = df.pivot_table(
            index="model_name", columns="feedback_type", values="count", fill_value=0
        )
        st.bar_chart(pivot_df)
    else:
        st.warning("No hay datos de tipos de feedback disponibles.")


def display_docs_satisfaction(data):
    if data:
        st.subheader("Relación Documentos Consultados vs Satisfacción")
        df = pd.DataFrame(data)
        # Gráfico de promedios
        avg_df = df.groupby("n_documents")["score"].mean().reset_index()
        st.line_chart(avg_df.set_index("n_documents"))
    else:
        st.warning("No hay datos de relación documentos/satisfacción.")


def display_response_quality(data):
    if data:
        st.subheader("Tiempos de Respuesta vs Calidad Percibida")
        df = pd.DataFrame(data)
        colors = random.sample(colors_allowed, 2)

        # Gráfico de doble eje
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax1.plot(
            df["model_name"],
            df["response_time"],
            color=colors[0],
            marker="o",
            label="Tiempo Respuesta",
        )
        ax2.plot(
            df["model_name"],
            df["avg_score"],
            color=colors[1],
            marker="x",
            label="Puntuación Promedio",
        )

        ax1.set_xlabel("Modelo")
        ax1.set_ylabel("Tiempo (s)")
        ax2.set_ylabel("Puntuación")
        fig.legend(loc="upper right")
        st.pyplot(fig)
    else:
        st.warning("No hay datos de tiempos de respuesta.")


def display_low_score_words(word_list):
    if word_list:
        st.subheader("Palabras Clave en Consultas con Baja Puntuación")

        # Nube de palabras
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            " ".join(word_list)
        )
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

        # Top 10 palabras
        count = Counter(word_list)
        top_words = pd.DataFrame(
            count.most_common(10), columns=["Palabra", "Frecuencia"]
        )
        st.bar_chart(top_words.set_index("Palabra"))
    else:
        st.warning("No hay datos de palabras clave.")


def display_high_score_contexts(contexts):
    if contexts:
        st.subheader("Contextos Asociados a Mejores Calificaciones")

        # Análisis de términos comunes
        all_terms = " ".join(contexts).lower().split()
        filtered_terms = [term for term in all_terms if len(term) > 3]
        count = Counter(filtered_terms)
        top_terms = pd.DataFrame(
            count.most_common(10), columns=["Término", "Frecuencia"]
        )

        col1, col2 = st.columns(2)
        with col1:
            st.write("Términos más frecuentes:")
            st.dataframe(
                top_terms,
                hide_index=True,
                use_container_width=True,
            )
        with col2:
            st.bar_chart(top_terms.set_index("Término"))
    else:
        st.warning("No hay datos de contextos.")


def display_feedback_summary(summary):
    if summary:
        st.subheader("Resumen General de Feedback")

        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Puntuación Promedio", f"{summary['avg_score']}/5")
        with col2:
            st.metric("Feedback Positivo", f"{summary['positive_percent']}%")
        with col3:
            st.metric("Modelo Más Usado", summary["top_model"])

        # Modelos más utilizados
        st.write("### Distribución de Modelos")
        model_counts = pd.DataFrame(
            summary["model_distribution"], columns=["Modelo", "Uso"]
        )
        st.bar_chart(model_counts.set_index("Modelo"))

        # Fuentes más consultadas
        st.write("### Fuentes Más Populares")
        source_counts = pd.DataFrame(
            summary["top_sources"],
            columns=["Fuente", "Menciones"],
        )
        st.dataframe(
            source_counts,
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.warning("No hay datos de resumen disponibles.")


def show_feedback_reports():
    n_feedbacks = st.number_input(
        "Número de feedbacks a analizar",
        min_value=1,
        value=50,
        step=10,
        help="Selecciona la cantidad de feedbacks recientes a incluir en el análisis",
    )

    data = fetch_feedback_data(n_feedbacks)

    if not data or any(v is None for v in data.values()):
        st.error("Error al cargar los datos de feedback")
        return

    display_feedback_summary(data["feedback_summary"])
    display_scores_distribution(data["scores_distribution"])
    display_feedback_types(data["feedback_types"])
    display_docs_satisfaction(data["docs_satisfaction"])
    display_response_quality(data["response_quality"])
    display_low_score_words(data["low_score_words"])
    display_high_score_contexts(data["high_score_contexts"])
