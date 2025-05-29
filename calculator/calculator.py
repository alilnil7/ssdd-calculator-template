"""Calculator implementation."""

## Mmmmm... here should be some missing imports
"""Calculator implementation."""

from RemoteCalculator import Calculator as IceCalculator
from RemoteCalculator import ZeroDivisionError  # Добавьте этот импорт

class Calculator(IceCalculator):
    """Реализация интерфейса калькулятора для Ice."""
    
    def sum(self, a: float, b: float, current=None) -> float:
        """Сложение двух чисел."""
        return a + b

    def sub(self, a: float, b: float, current=None) -> float:
        """Вычитание двух чисел."""
        return a - b

    def mult(self, a: float, b: float, current=None) -> float:
        """Умножение двух чисел."""
        return a * b

    def div(self, a: float, b: float, current=None) -> float:
        """Деление двух чисел."""
        if b == 0:
            raise ZeroDivisionError()  # Используем импортированное исключение
        return a / b
    """Divide two numbers."""
    """BAD skeleton for the implementation (missing parent class)."""
