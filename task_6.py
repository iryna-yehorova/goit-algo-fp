import argparse


items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def _validate(food, budget):
    if not isinstance(budget, int) or budget < 0:
        raise ValueError("Бюджет має бути невід'ємним цілим числом")
    for name, data in food.items():
        if not isinstance(data["cost"], int) or data["cost"] <= 0:
            raise ValueError(f"Вартість {name} має бути додатним цілим числом")
        if not isinstance(data["calories"], int) or data["calories"] < 0:
            raise ValueError(f"Калорійність {name} має бути невід'ємним цілим числом")


def greedy_algorithm(food, budget):
    _validate(food, budget)
    ordered = sorted(food, key=lambda name: food[name]["calories"] / food[name]["cost"],
                     reverse=True)
    selected = []
    calories = 0
    remaining = budget
    for name in ordered:
        cost = food[name]["cost"]
        if cost <= remaining:
            selected.append(name)
            calories += food[name]["calories"]
            remaining -= cost
    return selected, calories


def dynamic_programming(food, budget):
    _validate(food, budget)
    names = list(food)
    dp = [[0] * (budget + 1) for _ in range(len(names) + 1)]

    for index, name in enumerate(names, start=1):
        cost = food[name]["cost"]
        calories = food[name]["calories"]
        for capacity in range(budget + 1):
            dp[index][capacity] = dp[index - 1][capacity]
            if cost <= capacity:
                candidate = dp[index - 1][capacity - cost] + calories
                if candidate > dp[index][capacity]:
                    dp[index][capacity] = candidate

    selected = []
    capacity = budget
    for index in range(len(names), 0, -1):
        name = names[index - 1]
        cost = food[name]["cost"]
        if cost <= capacity and dp[index][capacity] > dp[index - 1][capacity]:
            selected.append(name)
            capacity -= cost
    selected.reverse()
    return selected, dp[len(names)][budget]


def main():
    parser = argparse.ArgumentParser(description="Порівняння способів вибору страв")
    parser.add_argument("budget", type=int, nargs="?", default=100,
                        help="бюджет (типово 100)")
    args = parser.parse_args()
    for title, algorithm in (("Жадібний алгоритм", greedy_algorithm),
                             ("Динамічне програмування", dynamic_programming)):
        try:
            selected, calories = algorithm(items, args.budget)
        except ValueError as error:
            parser.error(str(error))
        cost = sum(items[name]["cost"] for name in selected)
        print(f"{title}: {selected}; вартість: {cost}; калорії: {calories}")


if __name__ == "__main__":
    main()
