import sys
from dataclasses import dataclass, field
from typing import List, Dict, Any

sys.stdout.reconfigure(encoding='utf-8')


@dataclass(order=True)
class PrintJob:
    """Клас для представлення завдання на 3D-друк."""
    priority: int
    volume: float = field(compare=False)
    id: str = field(compare=False)
    print_time: int = field(compare=False)


@dataclass
class PrinterConstraints:
    """Клас для представлення обмежень 3D-принтера."""
    max_volume: float
    max_items: int


def optimize_printing(print_jobs_data: List[Dict[str, Any]], printer_constraints_data: Dict[str, Any]) -> Dict[
    str, Any]:
    """
    Оптимізує чергу завдань для 3D-принтера, повертаючи деталізовані групи.
    """
    constraints = PrinterConstraints(**printer_constraints_data)

    jobs = []
    for data in print_jobs_data:
        if data['volume'] > constraints.max_volume:
            print(f"Попередження: Завдання '{data['id']}' має об'єм {data['volume']} см³, "
                  f"що перевищує ліміт принтера ({constraints.max_volume} см³) і буде проігнороване.")
            continue
        jobs.append(PrintJob(**data))

    jobs.sort(key=lambda j: (j.priority, -j.volume))

    remaining_jobs = list(jobs)
    # Зберігатимемо детальну інформацію про кожну групу
    detailed_groups = []
    total_print_time = 0
    batch_counter = 1

    while remaining_jobs:
        current_batch = []
        current_volume = 0.0
        jobs_to_remove = []

        for job in remaining_jobs:
            if (current_volume + job.volume <= constraints.max_volume and
                    len(current_batch) < constraints.max_items):
                current_batch.append(job)
                current_volume += job.volume
                jobs_to_remove.append(job)

        if not current_batch:
            break

        batch_time = max(job.print_time for job in current_batch)
        total_print_time += batch_time

        # Створюємо деталізований опис групи
        detailed_groups.append({
            "batch_number": batch_counter,
            "jobs": [job.id for job in current_batch],
            "total_volume": round(current_volume, 2),
            "batch_time": batch_time
        })

        batch_counter += 1
        remaining_jobs = [job for job in remaining_jobs if job not in jobs_to_remove]

    final_print_order_ids = [job_id for group in detailed_groups for job_id in group['jobs']]

    return {
        "print_order": final_print_order_ids,
        "grouped_order": detailed_groups,
        "total_time": total_print_time
    }


def display_results(result: Dict[str, Any]):
    """Функція для наочного відображення результатів оптимізації."""
    print("\n" + "=" * 40)
    print("                ДЕТАЛЬНИЙ ПЛАН ДРУКУ")
    print("=" * 40)

    if not result['grouped_order']:
        print("Немає завдань для друку.")
        return

    for group in result['grouped_order']:
        print(f"\n--- Група друку №{group['batch_number']} ---")
        print(f"  Завдання для одночасного друку: {group['jobs']}")
        print(f"  Загальний об'єм групи: {group['total_volume']} см³")
        print(f"  Час виконання цієї групи: {group['batch_time']} хвилин")

    print("\n" + "=" * 40)
    print("                    ЗАГАЛЬНИЙ РЕЗУЛЬТАТ")
    print("=" * 40)
    print(f"Порядок виконання всіх завдань: {result['print_order']}")
    print(f"Загальний розрахований час друку: {result['total_time']} хвилин")
    print("=" * 40 + "\n")


# --- Тестові сценарії ---
if __name__ == "__main__":
    printer_constraints = {
        "max_volume": 1000.0,
        "max_items": 4
    }

    # --- Сценарій 1: Завдання різних пріоритетів ---
    print("--- ЗАПУСК СЦЕНАРІЮ 1: Завдання різних пріоритетів ---")
    mixed_priority_jobs = [
        {"id": "M1-Personal", "volume": 200, "priority": 3, "print_time": 120},
        {"id": "M2-Lab", "volume": 400, "priority": 2, "print_time": 200},
        {"id": "M3-Coursework", "volume": 700, "priority": 1, "print_time": 300},
        {"id": "M4-Lab", "volume": 350, "priority": 2, "print_time": 180},
        {"id": "M5-Personal", "volume": 150, "priority": 3, "print_time": 90},
        {"id": "M6-Coursework", "volume": 250, "priority": 1, "print_time": 150},
    ]
    result1 = optimize_printing(mixed_priority_jobs, printer_constraints)
    display_results(result1)

    # --- Сценарій 2: Перевищення обмежень ---
    print("\n--- ЗАПУСК СЦЕНАРІЮ 2: Перевищення обмежень ---")
    limit_test_jobs = [
        {"id": "L1-Big", "volume": 800, "priority": 1, "print_time": 400},
        {"id": "L2-Medium", "volume": 250, "priority": 2, "print_time": 150},
        {"id": "L3-Small1", "volume": 50, "priority": 2, "print_time": 30},
        {"id": "L4-Small2", "volume": 50, "priority": 2, "print_time": 30},
        {"id": "L5-Small3", "volume": 50, "priority": 2, "print_time": 30},
        {"id": "L6-Small4", "volume": 50, "priority": 2, "print_time": 30},
        {"id": "L7-TooBig", "volume": 1200, "priority": 1, "print_time": 600},
    ]
    result2 = optimize_printing(limit_test_jobs, printer_constraints)
    display_results(result2)