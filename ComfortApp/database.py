import sqlite3
import random

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('furniture.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.migrate_database()
        self.check_and_add_test_data()
        print("✅ База данных SQLite подключена")
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS workshops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                employees_count INTEGER DEFAULT 5,
                production_time_days INTEGER DEFAULT 3
            )
        ''')
        
        self.conn.commit()
    
    def migrate_database(self):
        try:
            self.cursor.execute("PRAGMA table_info(products)")
            columns = [column[1] for column in self.cursor.fetchall()]
            
            if 'article' not in columns:
                print("🔄 Обновление структуры базы данных...")
                
                self.cursor.execute('''
                    CREATE TABLE products_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        article TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        price REAL NOT NULL
                    )
                ''')
                
                self.cursor.execute("SELECT id, name, price FROM products")
                old_products = self.cursor.fetchall()
                
                for product in old_products:
                    article = self.generate_article()
                    self.cursor.execute(
                        "INSERT INTO products_new (id, article, name, price) VALUES (?, ?, ?, ?)",
                        (product[0], article, product[1], product[2])
                    )
                
                self.cursor.execute("DROP TABLE products")
                self.cursor.execute("ALTER TABLE products_new RENAME TO products")
                
                self.conn.commit()
                print("✅ Структура базы данных обновлена")
                
        except Exception as e:
            print(f"❌ Ошибка миграции: {e}")
            self.conn.rollback()
    
    def generate_article(self):
        while True:
            article = f"КМ-{random.randint(1000, 9999)}"
            try:
                self.cursor.execute("SELECT id FROM products WHERE article = ?", (article,))
                if not self.cursor.fetchone():
                    return article
            except:
                return article
    
    def check_and_add_test_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM products")
        if self.cursor.fetchone()[0] == 0:
            test_products = [
                ("КМ-1001", "Стол дубовый Классик", 25000),
                ("КМ-1002", "Стул металлический Лофт", 8500),
                ("КМ-1003", "Диван мягкий Модерн", 55000),
                ("КМ-1004", "Шкаф-купе трехдверный", 45000),
                ("КМ-1005", "Кресло с подлокотниками", 15000)
            ]
            try:
                self.cursor.executemany(
                    "INSERT INTO products (article, name, price) VALUES (?, ?, ?)", 
                    test_products
                )
                print("✅ Добавлены тестовые продукты")
            except:
                for _, name, price in test_products:
                    self.cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
                print("✅ Добавлены тестовые продукты (без артикулов)")
        
        self.cursor.execute("SELECT COUNT(*) FROM workshops")
        if self.cursor.fetchone()[0] == 0:
            test_workshops = [
                ("Столярный цех", "Изготовление корпусной мебели из дерева", 12, 3),
                ("Сборочный цех", "Сборка готовых изделий и фурнитуры", 8, 2),
                ("Цех мягкой мебели", "Производство диванов, кресел и пуфов", 15, 5),
                ("Покрасочный цех", "Окраска и лакировка изделий", 6, 2),
                ("Цех металлообработки", "Изготовление металлических каркасов", 10, 4)
            ]
            self.cursor.executemany(
                "INSERT INTO workshops (name, description, employees_count, production_time_days) VALUES (?, ?, ?, ?)",
                test_workshops
            )
            print("✅ Добавлены тестовые цеха")
        
        self.conn.commit()
    
    def get_products(self):
        try:
            self.cursor.execute("SELECT id, article, name, price FROM products ORDER BY id")
            return self.cursor.fetchall()
        except:
            self.cursor.execute("SELECT id, name, price FROM products ORDER BY id")
            rows = self.cursor.fetchall()
            return [(row[0], "---", row[1], row[2]) for row in rows]
    
    def get_product_by_id(self, pid):
        try:
            self.cursor.execute("SELECT id, article, name, price FROM products WHERE id = ?", (pid,))
            return self.cursor.fetchone()
        except:
            self.cursor.execute("SELECT id, name, price FROM products WHERE id = ?", (pid,))
            row = self.cursor.fetchone()
            if row:
                return (row[0], "---", row[1], row[2])
            return None
    
    def add_product(self, name, price):
        article = self.generate_article()
        try:
            self.cursor.execute(
                "INSERT INTO products (article, name, price) VALUES (?, ?, ?)", 
                (article, name, price)
            )
        except:
            self.cursor.execute(
                "INSERT INTO products (name, price) VALUES (?, ?)", 
                (name, price)
            )
            article = "---"
        
        self.conn.commit()
        return self.cursor.lastrowid, article
    
    def update_product(self, pid, name, price):
        try:
            self.cursor.execute(
                "UPDATE products SET name = ?, price = ? WHERE id = ?", 
                (name, price, pid)
            )
        except Exception as e:
            print(f"Ошибка обновления: {e}")
            return False
        
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_product(self, pid):
        self.cursor.execute("DELETE FROM products WHERE id = ?", (pid,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_workshops(self):
        self.cursor.execute("SELECT id, name, description, employees_count, production_time_days FROM workshops ORDER BY id")
        return self.cursor.fetchall()
    
    def get_workshop_by_id(self, wid):
        self.cursor.execute("SELECT id, name, description, employees_count, production_time_days FROM workshops WHERE id = ?", (wid,))
        return self.cursor.fetchone()
    
    def add_workshop(self, name, description, employees, days):
        self.cursor.execute(
            "INSERT INTO workshops (name, description, employees_count, production_time_days) VALUES (?, ?, ?, ?)",
            (name, description, employees, days)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_workshop(self, wid, name, description, employees, days):
        self.cursor.execute(
            "UPDATE workshops SET name = ?, description = ?, employees_count = ?, production_time_days = ? WHERE id = ?",
            (name, description, employees, days, wid)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_workshop(self, wid):
        self.cursor.execute("DELETE FROM workshops WHERE id = ?", (wid,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def close(self):
        self.conn.close()
        print("🔌 Соединение с БД закрыто")