class Product:
    def __init__(self, id=0, article="", name="", price=0):
        self.id = id
        self.article = article
        self.name = name
        self.price = price
    
    @classmethod
    def from_db_row(cls, row):
        if row and len(row) >= 4:
            return cls(
                id=row[0], 
                article=row[1], 
                name=row[2], 
                price=float(row[3])
            )
        return cls()
    
    def format_price(self):
        return f"{self.price:,.0f} ₽".replace(",", " ")

class Workshop:
    def __init__(self, id=0, name="", description="", employees=0, days=0):
        self.id = id
        self.name = name
        self.description = description
        self.employees = employees
        self.days = days
    
    @classmethod
    def from_db_row(cls, row):
        if row and len(row) >= 5:
            return cls(
                id=row[0], 
                name=row[1], 
                description=row[2] if row[2] else "", 
                employees=row[3] if row[3] else 0, 
                days=row[4] if row[4] else 0
            )
        return cls()