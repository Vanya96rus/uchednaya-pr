class Calculator:
    PRODUCT_COEFF = {
        "Стол": 1.2,
        "Стул": 0.8,
        "Диван": 2.5,
        "Кресло": 1.8,
        "Шкаф": 2.0
    }
    
    MATERIAL_LOSS = {
        "Дуб": 15.0,
        "Сосна": 12.0,
        "Фанера": 8.0,
        "Лён": 5.0,
        "Металл": 3.0
    }
    
    @staticmethod
    def calculate(product_type, material_type, quantity, length, width, height):
        try:
            if quantity <= 0 or length <= 0 or width <= 0 or height <= 0:
                return -1
            
            if product_type not in Calculator.PRODUCT_COEFF:
                return -1
            if material_type not in Calculator.MATERIAL_LOSS:
                return -1
            
            coeff = Calculator.PRODUCT_COEFF[product_type]
            loss = Calculator.MATERIAL_LOSS[material_type]
            
            volume = length * width * height
            total = volume * coeff * quantity
            with_loss = total * (1 + loss / 100)
            
            return int(with_loss) + (1 if with_loss % 1 > 0 else 0)
            
        except:
            return -1
    
    @staticmethod
    def get_product_types():
        return list(Calculator.PRODUCT_COEFF.keys())
    
    @staticmethod
    def get_material_types():
        return list(Calculator.MATERIAL_LOSS.keys())