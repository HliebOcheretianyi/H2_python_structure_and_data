# H2 Python Structure and Data  

## Опис  
Цей репозиторій містить набір скриптів для збору, обробки та збереження даних, пов’язаних із інформацією про Україну, аналітикою ISW (Institute for the Study of War) та іншими корисними даними.  

## Функціональність  
### Основні компоненти:  
- **`main.py`** – Головний файл для запуску мікросайту програми.  
- **`ISW_everyday_update.py`** – Скрипт для щоденного оновлення даних ISW.  
- **`ISW_history.py`** – Збір даних ISW.  
- **`alerts_in_ua.py`** – Скрипт для отримання даних про тривоги в Україні на даний момент.  
- **`weather_scrap.py`** – Збір та обробка погодних даних з сайту visualcrossing.com.  
- **`db_loader.py`** – Завантаження даних у базу даних (не актуально на даний момент).  
- **`templates/`** – Шаблони для роботи рендеру сторінок у фласк.  
- **`ISW.parquet`** – Файл у форматі Parquet, що містить структуровані дані з ISW.  

## Вимоги  
Для роботи необхідно встановити:  
- Python 3.x  
- Модулі (перелік можна отримати з `requirements.txt`)  

## Використання  
1. Клонувати репозиторій:  
   ```bash
   git clone https://github.com/HliebOcheretianyi/H2_python_structure_and_data.git  
   cd H2_python_structure_and_data  
   ```  
2. Встановити залежності:  
   ```bash
   pip install -r requirements.txt  
   ```  
3. Запустити головний скрипт:  
   ```bash
   python main.py  
   ```  
