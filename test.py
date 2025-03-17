import psycopg2

connection = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="34.238.247.150", port=5432)

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        city VARCHAR(100)
    )
""")

# Вставляємо дані
cursor.execute(
    "INSERT INTO users (name, age, city) VALUES (%s, %s, %s)",
    ("Maya", 18, "Kyiv")
)

# Зберігаємо зміни
connection.commit()
# Fetch all rows from database
cursor.execute("SELECT * FROM users")
records = cursor.fetchall()
# Закриваємо підключення
cursor.close()
connection.close()





print("Data from Database:- ", records)