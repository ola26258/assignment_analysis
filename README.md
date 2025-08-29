# Анализ двух портфелей цессий с использованием SQL

## Условия:
Цессия 1 была продана за 10% от общей суммы задолженности, цессия 2 была продана за 8% от общей суммы задолженности. Необходимо проанализировать качество 2 проданных портфеля и сделать выводы по итогам анализа.

## Решение:

### 1. Для переноса данных воспользуемся скриптом python (файл import_excel).

### 2. После переноса данных переименуем столбцы для дальнейшего удобства работы:
``` sql
ALTER TABLE portfolio_1 RENAME "Количество пролонгаций" TO renewals_amount;
ALTER TABLE portfolio_1 RENAME "Сумма займа" TO loan_amount;
ALTER TABLE portfolio_1 RENAME "Сумма, выданная клиенту" TO issued_amount;
ALTER TABLE portfolio_1 RENAME "Сумма доппродуктов, включенных в з" TO addons_amount;
ALTER TABLE portfolio_1 RENAME "Валюта" TO currency;
ALTER TABLE portfolio_1 RENAME "Срок займа по договору" TO loan_term;
ALTER TABLE portfolio_1 RENAME "Сумма платежа по договору на дату " TO payment_due;
ALTER TABLE portfolio_1 RENAME "Сумма, поступившая от должника в п" TO paid_amount;
ALTER TABLE portfolio_1 RENAME "Оплачено всего процентов по Догов" TO interest_paid;
ALTER TABLE portfolio_1 RENAME "Оплачено всего основного долга" TO debt_paid;
ALTER TABLE portfolio_1 RENAME "Количество платежей, поступивших " TO payments_count;
ALTER TABLE portfolio_1 RENAME "Общая сумма долга" TO total_debt;
ALTER TABLE portfolio_1 RENAME "Основной долг" TO principal_debt;
ALTER TABLE portfolio_1 RENAME "Сумма процентов" TO interest_debt;
ALTER TABLE portfolio_1 RENAME "Штрафы" TO penalties;
ALTER TABLE portfolio_1 RENAME "Срок просрочки в днях" TO days_delinquent;
ALTER TABLE portfolio_1 RENAME "Было ли списание доп.услуг" TO addons_writeoff_flag;
ALTER TABLE portfolio_1 RENAME "Сумма списания доп.услуг" TO addons_writeoff_amount;
ALTER TABLE portfolio_1 RENAME "Сумма по исполнительным производств" TO enforcement_amount;

ALTER TABLE portfolio_2 RENAME "Количество пролонгаций" TO renewals_amount;
ALTER TABLE portfolio_2 RENAME "Сумма займа" TO loan_amount;
ALTER TABLE portfolio_2 RENAME "Сумма, выданная клиенту" TO issued_amount;
ALTER TABLE portfolio_2 RENAME "Сумма доппродуктов, включенных в з" TO addons_amount;
ALTER TABLE portfolio_2 RENAME "Валюта" TO currence;
ALTER TABLE portfolio_2 RENAME "Срок займа по договору" TO loan_term;
ALTER TABLE portfolio_2 RENAME "Сумма платежа по договору на дату " TO payment_due;
ALTER TABLE portfolio_2 RENAME "Сумма, поступившая от должника в п" TO paid_amount;
ALTER TABLE portfolio_2 RENAME "Оплачено всего процентов по Догов" TO interest_paid;
ALTER TABLE portfolio_2 RENAME "Оплачено всего основного долга" TO debt_paid;
ALTER TABLE portfolio_2 RENAME "Количество платежей, поступивших " TO payment_count;
ALTER TABLE portfolio_2 RENAME "Общая сумма долга" TO total_debt;
ALTER TABLE portfolio_2 RENAME "Основной долг" TO principal_debt;
ALTER TABlE portfolio_2 RENAME "Сумма процентов" TO interest_debt;
ALTER TABLE portfolio_2 RENAME "Штрафы" TO penalties;
ALTER TABLE portfolio_2 RENAME "Срок просрочки в днях" TO days_delinquent;
ALTER TABLE portfolio_2 RENAME "Было ли списание доп.услуг" TO addons_writeoff_flag;
ALTER TABLE portfolio_2 RENAME "Сумма списания доп.услуг" TO addons_writeoff_amount;
ALTER TABLE portfolio_2 RENAME "Сумма по исполнительным производс" TO enforcment_amount;
```
### 3. Для оценки качества портфеля сравним основные показатели:
```sql
SELECT 
	'Portfolio 1' as portfolio,
	COUNT(credit_id) as total_loans,
	SUM(loan_amount) as total_loan_amount,
	AVG(loan_amount) as avg_loan_size,
	AVG(days_delinquent) as avg_days_delinquent,
	SUM(total_debt) as total_debt,
	SUM(debt_paid) as total_debt_paid,
	SUM(interest_paid) as total_interes_paid
FROM portfolio_1

UNION ALL

SELECT 
	'Portfolio 2' as portfolio,
	COUNT(credit_id) as total_loans,
	SUM(loan_amount) as total_loan_amount,
	AVG(loan_amount) as avg_loan_size,
	AVG(days_delinquent) as avg_days_delinquent,
	SUM(total_debt) as total_debt,
	SUM(debt_paid) as total_debt_paid,
	SUM(interest_paid) as total_interes_paid
FROM portfolio_2
```
<img width="1043" height="91" alt="{A02D6555-3278-4A74-940E-0E98E985A567}" src="https://github.com/user-attachments/assets/380c441a-e3d3-42ae-bbe4-6a5a9d319abf" />

### 4. Рассчитаем коэффициент возврата долга:

```sql
SELECT 'Portfolio 1' as portfolio,
       SUM(paid_amount) / SUM(total_debt) as recovery_rate
FROM portfolio_1
UNION ALL  
SELECT 'Portfolio 2',
       SUM(paid_amount) / SUM(total_debt)
FROM portfolio_2;
```
<img width="428" height="144" alt="image" src="https://github.com/user-attachments/assets/b502769a-1fa1-4742-88b7-4de5c529160f" />

### 5. Рассчитаем количество кредитов, сумму долга в разрезе дней просрочки для первого портфеля:

```sql
SELECT 
    'Portfolio 1' as portfolio,
	CASE 
        WHEN days_delinquent = 0 THEN '0 (текущие)'
        WHEN days_delinquent BETWEEN 1 AND 30 THEN '1-30 дней'
        WHEN days_delinquent BETWEEN 31 AND 90 THEN '31-90 дней'
        WHEN days_delinquent BETWEEN 91 AND 180 THEN '91-180 дней'
        ELSE '180+ дней'
    END as delinquency_bucket,
    COUNT(credit_id) as loans_count,
    SUM(total_debt) as debt_amount,
    AVG(days_delinquent) as avg_delinquency_days
FROM portfolio_1
GROUP BY portfolio, delinquency_bucket
ORDER BY portfolio, delinquency_bucket
```
<img width="1018" height="200" alt="image" src="https://github.com/user-attachments/assets/0f0d86b9-8068-4fe0-af68-c5b3e529d8ef" />

### 6. Рассчитаем количество кредитов, сумму долга в разрезе дней просрочки для второго портфеля:

```sql
SELECT 
    'Portfolio 2' as portfolio,
	CASE 
        WHEN days_delinquent = 0 THEN '0 (текущие)'
        WHEN days_delinquent BETWEEN 1 AND 30 THEN '1-30 дней'
        WHEN days_delinquent BETWEEN 31 AND 90 THEN '31-90 дней'
        WHEN days_delinquent BETWEEN 91 AND 180 THEN '91-180 дней'
        ELSE '180+ дней'
    END as delinquency_bucket,
    COUNT(credit_id) as loans_count,
    SUM(total_debt) as debt_amount,
    AVG(days_delinquent) as avg_delinquency_days
FROM portfolio_2
GROUP BY portfolio, delinquency_bucket
ORDER BY portfolio, delinquency_bucket
```
<img width="1020" height="184" alt="image" src="https://github.com/user-attachments/assets/f6ee9921-8d93-4af0-a4c4-009dfdfc67b2" />

## Вывод
По резльтатам анализа цессия 2 была продана за 8% от общей суммы задолженности, что по сравнению с цессией 1, проданной за 10% является заниженной ценой. 1 цессия показывает худший процент возрата займов: 18,4% против 28,1% у цессии 2. Также 2 цессия имеет меньше проблемных кредитов в стадии просрочки более 180 дней (313 против 441 у цессии 1). Разница в цене не отражает фактического различия в качестве портфелей. 2 цессия недооценена, в то время как стоимость цессии 1 является переоцененной относительно ее характеристик.
