from typing import List, Dict, Tuple


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію (top-down).

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком, списком довжин частин та кількістю розрізів.
    """
    # memo зберігає максимальний прибуток для довжини i: (profit, first_cut)
    memo = {}

    def solve(n: int) -> Tuple[int, int]:
        """Рекурсивна функція з кешуванням результатів."""
        if n == 0:
            return 0, 0
        if n in memo:
            return memo[n]

        max_profit = -1
        best_first_cut = -1

        # Перебираємо всі можливі довжини першого розрізу
        for i in range(1, n + 1):
            # i - довжина першого шматка (від 1 до n)
            # ціна за цей шматок - prices[i-1]
            current_profit = prices[i - 1] + solve(n - i)[0]

            if current_profit > max_profit:
                max_profit = current_profit
                best_first_cut = i

        memo[n] = (max_profit, best_first_cut)
        return memo[n]

    # Запускаємо рекурсію для початкової довжини
    max_profit, _ = solve(length)

    # Відновлюємо послідовність розрізів
    cuts = []
    remaining_length = length
    while remaining_length > 0:
        _, first_cut = memo[remaining_length]
        cuts.append(first_cut)
        remaining_length -= first_cut

    # Кількість розрізів = кількість шматків - 1
    # Якщо шматок один, розрізів 0.
    number_of_cuts = len(cuts) - 1 if len(cuts) > 0 else 0

    return {
        "max_profit": max_profit,
        "cuts": sorted(cuts),  # Сортуємо для консистентності
        "number_of_cuts": number_of_cuts
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію (bottom-up).

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком, списком довжин частин та кількістю розрізів.
    """
    # dp[i] зберігає максимальний прибуток для стрижня довжини i
    dp = [0] * (length + 1)
    # first_cuts[i] зберігає довжину першого розрізу для оптимального рішення для довжини i
    first_cuts = [0] * (length + 1)

    # Заповнюємо таблицю знизу вгору
    for j in range(1, length + 1):
        max_profit_for_j = -1
        # Перебираємо всі можливі перші розрізи для довжини j
        for i in range(1, j + 1):
            current_profit = prices[i - 1] + dp[j - i]
            if current_profit > max_profit_for_j:
                max_profit_for_j = current_profit
                first_cuts[j] = i
        dp[j] = max_profit_for_j

    # Відновлюємо послідовність розрізів
    cuts = []
    remaining_length = length
    while remaining_length > 0:
        cut = first_cuts[remaining_length]
        cuts.append(cut)
        remaining_length -= cut

    number_of_cuts = len(cuts) - 1 if len(cuts) > 0 else 0

    return {
        "max_profit": dp[length],
        "cuts": sorted(cuts),  # Сортуємо для консистентності
        "number_of_cuts": number_of_cuts
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок",
            "expected_profit": 12,  # 2+10 (2+2+1 ціни 5+5+2=12, або 2+3 ціни 5+7=12)
            # Очікувані розрізи в завданні [1, 2, 2] дають 2+5+5=12
            "expected_cuts": [1, 2, 2]
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати",
            "expected_profit": 8,
            "expected_cuts": [3]
        },
        # Тест 3: Розрізи по 1 вигідніші
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи",
            "expected_profit": 12,  # 3*4
            "expected_cuts": [1, 1, 1, 1]
        },
        # Тест 4: Більш складний випадок
        {
            "length": 8,
            "prices": [1, 5, 8, 9, 10, 17, 17, 20],
            "name": "Складний випадок",
            "expected_profit": 22,  # 6+2
            "expected_cuts": [2, 6]
        }
    ]

    for test in test_cases:
        print(f"\n--- Тест: {test['name']} ---")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"  Максимальний прибуток: {memo_result['max_profit']}")
        print(f"  Розрізи: {memo_result['cuts']}")
        print(f"  Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"  Максимальний прибуток: {table_result['max_profit']}")
        print(f"  Розрізи: {table_result['cuts']}")
        print(f"  Кількість розрізів: {table_result['number_of_cuts']}")

        # Перевірка
        assert memo_result['max_profit'] == test['expected_profit']
        assert table_result['max_profit'] == test['expected_profit']
        assert sorted(memo_result['cuts']) == sorted(test['expected_cuts'])
        assert sorted(table_result['cuts']) == sorted(test['expected_cuts'])

        print("\n--> Перевірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()