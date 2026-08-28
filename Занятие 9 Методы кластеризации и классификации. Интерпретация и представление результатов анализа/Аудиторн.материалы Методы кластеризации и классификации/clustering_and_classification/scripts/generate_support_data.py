from pathlib import Path
import numpy as np
import pandas as pd

# Фиксируем генератор случайных чисел, чтобы датасет всегда воспроизводился одинаково.
rng = np.random.default_rng(42)

# Задаём количество учебных обращений.
n_rows = 2500

# Скрытый профиль нужен только для генерации данных.
# В итоговый CSV он НЕ попадает: слушатель должен найти структуру с помощью кластеризации.
latent_profile = rng.choice([0, 1, 2], size=n_rows, p=[0.40, 0.35, 0.25])

# Профили задают разные типы поведения обращений.
# 0: быстрые стандартные обращения;
# 1: коммуникационно сложные обращения;
# 2: обращения, созданные при высокой операционной нагрузке.
profile_params = {
    0: dict(response=12, resolution=170, messages=3, reopen=0.10, backlog=10, previous=1.0),
    1: dict(response=30, resolution=650, messages=14, reopen=1.70, backlog=20, previous=5.0),
    2: dict(response=95, resolution=900, messages=7, reopen=0.50, backlog=50, previous=2.5),
}

# Категориальные признаки генерируем так, чтобы они были связаны с характером обращения,
# но не определяли результат идеально. Это делает классификацию реалистичной учебной задачей.
priorities = np.array(['low', 'medium', 'high', 'critical'])
priority_probs = {
    0: [0.45, 0.38, 0.14, 0.03],
    1: [0.22, 0.38, 0.30, 0.10],
    2: [0.10, 0.28, 0.40, 0.22],
}

categories = np.array(['how_to', 'billing', 'account', 'technical', 'incident'])
category_probs = {
    0: [0.34, 0.30, 0.20, 0.10, 0.06],
    1: [0.10, 0.15, 0.22, 0.31, 0.22],
    2: [0.08, 0.12, 0.24, 0.30, 0.26],
}

channels = np.array(['portal', 'email', 'chat', 'phone'])
channel_probs = {
    0: [0.50, 0.29, 0.17, 0.04],
    1: [0.24, 0.32, 0.32, 0.12],
    2: [0.25, 0.36, 0.29, 0.10],
}

segments = np.array(['standard', 'business', 'vip'])
segment_probs = {
    0: [0.60, 0.30, 0.10],
    1: [0.38, 0.38, 0.24],
    2: [0.42, 0.36, 0.22],
}

# Для каждой строки выбираем категориальные значения с вероятностями своего скрытого профиля.
priority = np.array([rng.choice(priorities, p=priority_probs[p]) for p in latent_profile])
category = np.array([rng.choice(categories, p=category_probs[p]) for p in latent_profile])
channel = np.array([rng.choice(channels, p=channel_probs[p]) for p in latent_profile])
customer_segment = np.array([rng.choice(segments, p=segment_probs[p]) for p in latent_profile])

# Генерируем даты в пределах примерно шести месяцев.
start = np.datetime64('2026-01-01T00:00')
minutes_from_start = rng.integers(0, 180 * 24 * 60, size=n_rows)
created_at = pd.to_datetime(start + minutes_from_start.astype('timedelta64[m]'))
is_weekend = (created_at.dayofweek.to_numpy() >= 5).astype(int)

# Подготавливаем массивы для числовых признаков.
previous_tickets_90d = np.zeros(n_rows, dtype=int)
backlog_at_creation = np.zeros(n_rows, dtype=int)
agent_experience_months = np.zeros(n_rows, dtype=int)
first_response_minutes = np.zeros(n_rows)
resolution_minutes = np.zeros(n_rows)
messages_count = np.zeros(n_rows, dtype=int)
reopen_count = np.zeros(n_rows, dtype=int)

# Генерируем числовые признаки построчно.
for i, profile in enumerate(latent_profile):
    params = profile_params[profile]

    # История клиента: число обращений за последние 90 дней.
    previous_tickets_90d[i] = max(0, int(round(rng.normal(params['previous'], 0.8))))

    # Очередь в момент создания обращения.
    backlog_at_creation[i] = max(0, int(round(rng.normal(params['backlog'], 4.5))))

    # Опыт сотрудника связан с профилем лишь статистически, а не жёстко.
    experience_base = {0: 34, 1: 24, 2: 18}[profile]
    agent_experience_months[i] = int(np.clip(round(rng.normal(experience_base, 9)), 2, 72))

    # Коэффициенты моделируют влияние приоритета, выходного дня, очереди и опыта.
    priority_factor = {'low': 0.92, 'medium': 1.00, 'high': 1.10, 'critical': 1.18}[priority[i]]
    weekend_factor = 1.12 if is_weekend[i] else 1.00
    experience_factor = np.clip(1.16 - agent_experience_months[i] / 180, 0.78, 1.15)
    backlog_factor = 1 + backlog_at_creation[i] / 240

    # Логнормальное распределение даёт положительные значения и естественную правую асимметрию.
    first_response_minutes[i] = max(
        1,
        rng.lognormal(np.log(params['response']), 0.24) * backlog_factor * weekend_factor,
    )

    resolution_minutes[i] = max(
        15,
        rng.lognormal(np.log(params['resolution']), 0.24)
        * priority_factor
        * weekend_factor
        * experience_factor
        * backlog_factor,
    )

    # Количество сообщений и повторных открытий — дискретные признаки.
    messages_count[i] = max(1, int(round(rng.normal(params['messages'] * priority_factor, 1.3))))
    reopen_count[i] = max(0, int(rng.poisson(params['reopen'])))

# Добавляем небольшое число контролируемых длинных обращений как естественные выбросы.
outlier_index = rng.choice(n_rows, size=15, replace=False)
resolution_minutes[outlier_index] *= rng.uniform(1.6, 2.2, size=len(outlier_index))

# Норматив SLA зависит от приоритета обращения.
sla_by_priority = {'critical': 420, 'high': 780, 'medium': 1200, 'low': 1800}
sla_limit_minutes = np.array([sla_by_priority[p] for p in priority])

# Факт нарушения SLA определяется сравнением реального времени решения с нормативом.
sla_breached = (resolution_minutes > sla_limit_minutes).astype(int)

# Добавляем 2% операционного шума, чтобы задача не была искусственно идеальной.
noise_mask = rng.random(n_rows) < 0.02
sla_breached = np.where(noise_mask, 1 - sla_breached, sla_breached)

# Собираем итоговую таблицу.
df = pd.DataFrame({
    'ticket_id': [f'TKT-{i:05d}' for i in range(1, n_rows + 1)],
    'created_at': created_at,
    'channel': channel,
    'category': category,
    'priority': priority,
    'customer_segment': customer_segment,
    'previous_tickets_90d': previous_tickets_90d,
    'backlog_at_creation': backlog_at_creation,
    'agent_experience_months': agent_experience_months,
    'first_response_minutes': np.round(first_response_minutes, 1),
    'messages_count': messages_count,
    'reopen_count': reopen_count,
    'resolution_minutes': np.round(resolution_minutes, 1),
    'sla_limit_minutes': sla_limit_minutes,
    'sla_breached': sla_breached,
})

# Определяем корень проекта независимо от того, откуда запускается скрипт.
project_root = Path(__file__).resolve().parents[1]
output_path = project_root / 'data' / 'raw' / 'support_tickets.csv'
output_path.parent.mkdir(parents=True, exist_ok=True)

# Сохраняем CSV в UTF-8.
df.to_csv(output_path, index=False, encoding='utf-8')

# Выводим контрольную информацию для преподавателя.
print(f'Файл создан: {output_path}')
print(f'Количество строк: {len(df)}')
print(f'Доля нарушений SLA: {df["sla_breached"].mean():.3f}')
print('Пропуски:', int(df.isna().sum().sum()))
print('Дубликаты ticket_id:', int(df['ticket_id'].duplicated().sum()))
