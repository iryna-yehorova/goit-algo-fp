import argparse
import random


def simulate_dice_rolls(rolls, seed=None):
    if not isinstance(rolls, int) or rolls <= 0:
        raise ValueError("Кількість кидків має бути додатним цілим числом")

    rng = random.Random(seed)
    counts = {total: 0 for total in range(2, 13)}
    for _ in range(rolls):
        total = rng.randint(1, 6) + rng.randint(1, 6)
        counts[total] += 1
    return counts


def analytical_probability(total):
    if not 2 <= total <= 12:
        raise ValueError("Сума має бути від 2 до 12")
    return (6 - abs(7 - total)) / 36


def print_comparison(counts):
    rolls = sum(counts.values())
    print("Сума | Кількість | Монте-Карло | Аналітично | Різниця, в.п.")
    print("-----|-----------|-------------|------------|--------------")
    for total in range(2, 13):
        simulated = counts[total] / rolls
        analytical = analytical_probability(total)
        difference = abs(simulated - analytical) * 100
        print(f"{total:>4} | {counts[total]:>9} | {simulated * 100:>10.2f}% | "
              f"{analytical * 100:>9.2f}% | {difference:>12.3f}")

    max_difference = max(
        abs(counts[total] / rolls - analytical_probability(total)) * 100
        for total in range(2, 13)
    )
    print(f"\nНайбільше відхилення: {max_difference:.3f} відсоткового пункту")


def main():
    parser = argparse.ArgumentParser(description="Симуляція кидків двох кубиків")
    parser.add_argument("rolls", type=int, nargs="?", default=1_000_000,
                        help="кількість кидків (типово 1 000 000)")
    parser.add_argument("--seed", type=int, default=42,
                        help="початкове значення генератора випадкових чисел (типово 42)")
    args = parser.parse_args()
    try:
        counts = simulate_dice_rolls(args.rolls, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(f"Кидків: {args.rolls}; seed: {args.seed}\n")
    print_comparison(counts)


if __name__ == "__main__":
    main()
