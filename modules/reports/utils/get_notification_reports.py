# modules/reports/utils/get_notification_reports.py
from datetime import datetime, timedelta
import random
from collections import Counter


def fetch_notification_data(n_notifications: int):
    return {
        "notification_types": get_notification_types(n_notifications),
        "frequency_by_role": get_notification_frequency_by_role(n_notifications),
        "notification_summary": get_notification_summary(n_notifications),
    }


def get_notification_types(n_notifications: int):
    # Simulación de distribución por tipo de notificación
    types = ["urgent", "normal", "informative", "reminder", "alert"]
    return [{"type": nt_type, "count": random.randint(50, 200)} for nt_type in types]


def get_notification_frequency_by_role(n_notifications: int):
    # Simulación de frecuencia de notificaciones por rol
    roles = ["admin", "user", "viewer"]
    return [{"role": role, "count": random.randint(100, 500)} for role in roles]


def get_notification_summary(n_notifications: int):
    # Simulación de resumen general de notificaciones
    return {
        "total_notifications": random.randint(500, 1000),
        "most_common_type": random.choice(["urgent", "normal", "informative"]),
        "most_active_role": random.choice(["admin", "user", "viewer"]),
    }
