# # modules/reports/utils/get_feedback_reports.py
# from sqlalchemy import func, cast, Float, Integer, String
# from sqlalchemy.orm import Session
# from models.feedback import Feedback
# from collections import defaultdict
# import json
# from datetime import datetime, timedelta


def get_scores_distribution(n_feedbacks: int):
    return [
        {"model_name": "Model A", "score": 5, "count": 120},
        {"model_name": "Model B", "score": 4, "count": 85},
        {"model_name": "Model A", "score": 3, "count": 65},
    ]


#     return (
#         session.query(
#             Feedback.model_name,
#             cast(Feedback.score, Integer).label("score"),
#             func.count().label("count"),
#         )
#         .group_by(Feedback.model_name, cast(Feedback.score, Integer))
#         .order_by(Feedback.model_name, cast(Feedback.score, Integer))
#         .limit(n_feedbacks)
#         .all()
#     )


def get_feedback_types(n_feedbacks: int):
    return [
        {"model_name": "Model A", "feedback_type": "positive", "count": 150},
        {"model_name": "Model A", "feedback_type": "negative", "count": 30},
        {"model_name": "Model B", "feedback_type": "positive", "count": 100},
    ]


#     return (
#         session.query(
#             Feedback.model_name, Feedback.feedback_type, func.count().label("count")
#         )
#         .group_by(Feedback.model_name, Feedback.feedback_type)
#         .order_by(Feedback.model_name, func.count().desc())
#         .limit(n_feedbacks)
#         .all()
#     )


def get_docs_satisfaction(n_feedbacks: int):
    return [
        {"n_documents": 3, "score": 4.5},
        {"n_documents": 5, "score": 3.8},
        {"n_documents": 2, "score": 2.0},
    ]


#     return (
#         session.query(Feedback.n_documents, cast(Feedback.score, Float).label("score"))
#         .order_by(Feedback.created_at.desc())
#         .limit(n_feedbacks)
#         .all()
#     )


def get_response_quality_metrics(n_feedbacks: int):
    return [
        {"model_name": "Model A", "avg_score": 4.2, "response_time": 2.5},
        {"model_name": "Model B", "avg_score": 3.7, "response_time": 3.1},
        {"model_name": "Model C", "avg_score": 4.5, "response_time": 2.1},
    ]


#     # Obtener tiempos de respuesta promedio y puntuaciones por modelo
#     return (
#         session.query(
#             Feedback.model_name,
#             func.avg(cast(Feedback.score, Float)).label("avg_score"),
#             func.avg(func.extract("epoch", func.now() - Feedback.created_at)).label(
#                 "response_time"
#             ),
#         )
#         .group_by(Feedback.model_name)
#         .order_by(func.avg(cast(Feedback.score, Float)).desc())
#         .limit(n_feedbacks)
#         .all()
#     )


def get_low_score_words(n_feedbacks: int):
    return ["error", "incomplete", "slow"]


#     low_scores = (
#         session.query(Feedback.word_list)
#         .filter(cast(Feedback.score, Float) <= 2.0)
#         .order_by(Feedback.created_at.desc())
#         .limit(n_feedbacks)
#         .all()
#     )

#     words = []
#     for entry in low_scores:
#         words.extend(json.loads(entry[0]))
#     return words


def get_high_score_contexts(n_feedbacks: int):
    return [
        "The document provided a thorough explanation of the topic, supported by well-researched references.",
        "The context was highly relevant and accurate, giving a clear answer to the question asked.",
    ]


#     return (
#         session.query(Feedback.context)
#         .filter(cast(Feedback.score, Float) >= 4.0)
#         .order_by(Feedback.created_at.desc())
#         .limit(n_feedbacks)
#         .all()
#     )


def get_feedback_summary(n_feedbacks: int):
    return {
        "total_feedbacks": 500,
        "avg_score": 4.2,
        "positive_percent": 78.5,
        "top_model": "Model A",
        "model_distribution": [
            ["Model A", 200],
            ["Model B", 150],
            ["Model C", 100],
            ["Model D", 50],
            ["Model E", 25],
        ],
        "top_sources": [
            ["Source 1", 120],
            ["Source 2", 100],
            ["Source 3", 80],
            ["Source 4", 50],
            ["Source 5", 30],
        ],
    }


#     # Obtener datos básicos
#     total_feedbacks = session.query(func.count(Feedback.id)).limit(n_feedbacks).scalar()

#     avg_score = (
#         session.query(func.avg(cast(Feedback.score, Float))).limit(n_feedbacks).scalar()
#     )

#     positive_percent = (
#         session.query(
#             func.coalesce(
#                 func.round(
#                     100.0
#                     * func.sum(func.cast(Feedback.feedback_type == "positive", Integer))
#                     / func.count(),
#                     2,
#                 ),
#                 0,
#             )
#         )
#         .limit(n_feedbacks)
#         .scalar()
#     )

#     top_model = (
#         session.query(Feedback.model_name)
#         .group_by(Feedback.model_name)
#         .order_by(func.count().desc())
#         .limit(1)
#         .scalar()
#     )

#     # Fuentes más consultadas
#     sources = (
#         session.query(func.json_each_text(Feedback.sources).table_valued("value"))
#         .limit(n_feedbacks)
#         .all()
#     )

#     source_counts = defaultdict(int)
#     for source in sources:
#         source_counts[source[0]] += 1

#     return {
#         "total_feedbacks": total_feedbacks,
#         "avg_score": round(avg_score, 2) if avg_score else 0,
#         "positive_percent": positive_percent,
#         "top_model": top_model,
#         "model_distribution": [
#             (model, count)
#             for model, count in session.query(
#                 Feedback.model_name, func.count().label("count")
#             )
#             .group_by(Feedback.model_name)
#             .order_by(func.count().desc())
#             .limit(5)
#             .all()
#         ],
#         "top_sources": sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[
#             :5
#         ],
#     }
