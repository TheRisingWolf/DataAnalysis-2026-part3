# Словарь данных `support_tickets.csv`

| Поле | Тип | Смысл | Доступность для раннего прогноза SLA |
|---|---|---|---|
| `ticket_id` | string | идентификатор обращения | идентификатор, в модель не используем |
| `created_at` | datetime | дата и время создания | да |
| `channel` | category | канал: portal/email/chat/phone | да |
| `category` | category | категория обращения | да |
| `priority` | category | приоритет | да |
| `customer_segment` | category | сегмент клиента | да |
| `previous_tickets_90d` | int | обращения клиента за 90 дней | да |
| `backlog_at_creation` | int | размер очереди при создании | да |
| `agent_experience_months` | int | опыт назначенного сотрудника | да, в учебном сценарии |
| `first_response_minutes` | float | время до первого ответа | нет для прогноза непосредственно в момент создания |
| `messages_count` | int | число сообщений в обращении | нет |
| `reopen_count` | int | число повторных открытий | нет |
| `resolution_minutes` | float | полное время решения | нет; это явная информация будущего |
| `sla_limit_minutes` | int | норматив SLA | технически известен, но в базовой модели его эффект представлен через priority |
| `sla_breached` | int | целевой класс: 0 — соблюдён, 1 — нарушен | target |

## Признаки кластеризации

В кластеризации используются признаки, описывающие фактическое поведение уже завершённых обращений:

- `first_response_minutes`;
- `resolution_minutes`;
- `messages_count`;
- `reopen_count`;
- `backlog_at_creation`;
- `previous_tickets_90d`.

Здесь использование постфактум-признаков допустимо, потому что задача — исследовать структуру исторических обращений, а не прогнозировать будущее.

## Признаки классификации

Для раннего прогноза используются только признаки, доступные на момент создания или назначения обращения:

- `channel`;
- `category`;
- `priority`;
- `customer_segment`;
- `previous_tickets_90d`;
- `backlog_at_creation`;
- `agent_experience_months`;
- производные `created_hour` и `is_weekend`.
