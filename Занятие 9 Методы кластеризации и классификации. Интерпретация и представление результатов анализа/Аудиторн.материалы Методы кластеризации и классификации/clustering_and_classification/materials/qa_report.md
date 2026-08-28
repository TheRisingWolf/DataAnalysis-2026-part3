# QA-отчёт готовности комплекта

**Статус: ГОТОВО**

## Проверка технической воспроизводимости

| Проверка | Результат |
|---|---|
| Генератор данных выполняется без ошибок | OK |
| Датасет воспроизводится при повторном запуске | ДА |
| `teacher_solution.ipynb` выполняется сверху вниз | OK |
| `student_practice.ipynb` выполняется сверху вниз | OK |
| Абсолютные пути автора в notebook не требуются | OK |
| Есть автоматический поиск `data/raw/` и вариант для Colab | OK |
| Результаты сохраняются в `outputs/` | OK |
| Все импорты создаются до использования | OK |
| Preprocessing классификации выполняется внутри Pipeline | OK |
| Train/test разделение выполняется до обучения preprocessing | OK |
| В классификацию не передаётся `resolution_minutes` | OK |
| Перед K-Means выполняется StandardScaler | OK |
| Есть baseline классификации | OK |
| Используются accuracy, precision, recall и F1 | OK |
| Есть confusion matrix для двух моделей | OK |
| Русские комментарии и markdown-пояснения присутствуют | OK |

## Среда фактического теста

- Python: 3.13.5
- pandas: 2.2.3
- NumPy: 2.3.5
- matplotlib: 3.10.8
- scikit-learn: 1.8.0
- nbformat: 5.10.4
- nbconvert: 7.17.1

## Контрольные результаты

- исходных строк: **2500**;
- пропусков: **0**;
- дубликатов `ticket_id`: **0**;
- доля `sla_breached=1`: **0.302**;
- лучший silhouette среди `k=2...6`: **k=3**, около **0.637**;
- baseline accuracy: **0.698**, recall класса 1: **0.000**;
- Logistic Regression: accuracy **0.878**, precision **0.734**, recall **0.937**, F1 **0.823**;
- Decision Tree: accuracy **0.875**, precision **0.723**, recall **0.952**, F1 **0.822**.

## Создаваемые артефакты

После выполнения notebook присутствуют:

- `outputs/support_tickets_with_clusters.csv`;
- `outputs/cluster_profile.csv`;
- `outputs/classification_metrics.csv`;
- `outputs/classification_predictions.csv`;
- семь учебных графиков в `outputs/charts/`.

## Методическая проверка

Комплект движется от простого к сложному:

1. визуальная гипотеза о группах;
2. K-Means на двух признаках;
3. масштабирование;
4. K-Means на шести признаках;
5. выбор числа кластеров;
6. профилирование кластеров;
7. постановка задачи классификации;
8. target leakage;
9. train/test и baseline;
10. Logistic Regression;
11. Decision Tree;
12. несколько метрик и confusion matrix;
13. сохранение и аналитическая интерпретация результата.

Код рассчитан на учебный сценарий аналитика данных и не требует сложного ML-стека.
