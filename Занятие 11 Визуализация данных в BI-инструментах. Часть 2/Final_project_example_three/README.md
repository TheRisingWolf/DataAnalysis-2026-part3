# Учебный пример итоговой работы: продажи магазина электроники

Полный синтетический учебный комплект для прохождения аналитического цикла от исходных данных до подготовленных витрин для Yandex DataLens.

## Что внутри

```text
Final_project_example_three/
├── README.md
├── STUDENT_TASK.md
├── METADATA_electronics_sales.md
├── DATALENS_DASHBOARD_GUIDE.md
├── RESULTS_SUMMARY.md                  # формируется после выполнения notebook
├── QA_REPORT.md
├── requirements_electronics_analysis.txt
├── CHECKSUMS_SHA256.txt
├── electronics_store_sales_analysis_starter.ipynb
├── electronics_store_sales_analysis_final.ipynb
├── data/
│   ├── product_catalog_reference.csv
│   ├── raw/electronics_sales_10000.csv
│   ├── processed/electronics_sales_clean.csv
│   └── datalens/
│       ├── datalens_sales_mart.csv
│       ├── datalens_monthly_sales.csv
│       ├── datalens_product_abc_xyz.csv
│       ├── datalens_customer_rfm.csv
│       ├── datalens_category_channel.csv
│       ├── datalens_hypothesis_summary.csv
│       └── datalens_kpi.csv
└── outputs/charts/
```

## С чего начать

1. Установите зависимости из `requirements_electronics_analysis.txt`.
2. Для самостоятельной работы откройте `electronics_store_sales_analysis_starter.ipynb`.
3. Для изучения полного решения откройте `electronics_store_sales_analysis_final.ipynb`.
4. Исходные данные находятся в `data/raw/electronics_sales_10000.csv` и содержат ровно **10 000 строк**.
5. После выполнения решения будут сформированы очищенный датасет, витрины для DataLens, сводка результатов и графики.
6. Для построения BI-дашборда используйте `DATALENS_DASHBOARD_GUIDE.md`.

## Учебная логика

Бизнес-вопрос → первичный осмотр → качество данных → очистка/ETL → preprocessing → EDA → KPI → гипотезы → ABC-XYZ → RFM → подготовка BI-витрин → рекомендации и ограничения.

## Важно

Все данные полностью синтетические. Они не описывают реальный магазин, покупателей, цены, бренды, акции или коммерческие результаты. Значения брендов и товарных категорий используются только как узнаваемые учебные ярлыки.
