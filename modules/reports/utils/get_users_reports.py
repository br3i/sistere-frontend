# modules/reports/utils/get_users_reports.pyS
import random
from collections import Counter


def get_role_distribution(n_users: int):
    # Simulación de datos de roles
    roles = ["admin", "user", "viewer"]
    return [{"role": role, "count": random.randint(50, 200)} for role in roles]


def get_code_usage_by_role(n_users: int):
    # Simulación de uso de códigos por rol
    roles = ["admin", "user", "viewer"]
    return [
        {
            "role": role,
            "code_count": random.randint(100, 500),
            "user_count": random.randint(50, 200),
        }
        for role in roles
    ]


def get_active_users_metrics(n_users: int):
    # Simulación de usuarios activos por rol
    roles = ["admin", "user", "viewer"]
    return [{"role": role, "active_users": random.randint(50, 200)} for role in roles]
