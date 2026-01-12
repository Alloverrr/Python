import xml.etree.ElementTree as ET
from collections import defaultdict, Counter


def load_users_data():
    """Загрузка данных о пользователях из файла users.xml"""
    try:
        users_tree = ET.parse('users.xml')
        users = []
        for user_elem in users_tree.getroot().findall('user'):
            user = {
                'user_id': int(user_elem.find('user_id').text),
                'name': user_elem.find('name').text,
                'age': int(user_elem.find('age').text),
                'weight': int(user_elem.find('weight').text),
                'fitness_level': user_elem.find('fitness_level').text
            }
            users.append(user)
        return users
    except FileNotFoundError:
        print("Файл users.xml не найден")
        return []


def load_workouts_data():
    """Загрузка данных о тренировках из файла workouts.xml"""
    try:
        workouts_tree = ET.parse('workouts.xml')
        workouts = []
        for workout_elem in workouts_tree.getroot().findall('workout'):
            workout = {
                'workout_id': int(workout_elem.find('workout_id').text),
                'user_id': int(workout_elem.find('user_id').text),
                'date': workout_elem.find('date').text,
                'type': workout_elem.find('type').text,
                'duration': int(workout_elem.find('duration').text),
                'distance': float(workout_elem.find('distance').text),
                'calories': int(workout_elem.find('calories').text),
                'avg_heart_rate': int(workout_elem.find('avg_heart_rate').text),
                'intensity': workout_elem.find('intensity').text
            }
            workouts.append(workout)
        return workouts
    except FileNotFoundError:
        print("Файл workouts.xml не найден")
        return []


def analyze_user_activity(users, workouts):
    """Анализ активности и вывод топ-3 пользователей"""
    # Создаем статистику для каждого пользователя
    stats = []

    for user in users:
        user_id = user['user_id']
        # Фильтруем тренировки текущего пользователя
        user_trainings = [w for w in workouts if w['user_id'] == user_id]

        if user_trainings:  # Если есть тренировки
            trainings_count = len(user_trainings)
            calories_total = sum(w['calories'] for w in user_trainings)
            time_total = sum(w['duration'] for w in user_trainings) / 60

            stats.append({
                'имя': user['name'],
                'уровень': user['fitness_level'],
                'тренировки': trainings_count,
                'калории': calories_total,
                'время': time_total
            })

    # Сортируем по тренировкам и калориям
    stats.sort(key=lambda x: (x['тренировки'], x['калории']), reverse=True)

    # Выводим результаты
    print("\nТОП-3 АКТИВНЫХ ПОЛЬЗОВАТЕЛЕЙ:")
    for i, user in enumerate(stats[:3], 1):
        print(f"{i}. {user['имя']} ({user['уровень']}):")
        print(f"   Тренировок: {user['тренировки']}")
        print(f"   Калорий: {user['калории']}")
        print(f"   Время: {user['время']:.1f} часов\n")


def analyze_workout_types(workouts):
    """Анализ распределения тренировок по типам"""
    # Создаем словарь для сбора статистики
    type_data = defaultdict(lambda: {'количество': 0, 'длительность': 0, 'калории': 0})

    for training in workouts:
        t_type = training['type']
        type_data[t_type]['количество'] += 1
        type_data[t_type]['длительность'] += training['duration']
        type_data[t_type]['калории'] += training['calories']

    total_trainings = len(workouts)

    print("РАСПРЕДЕЛЕНИЕ ПО ТИПАМ ТРЕНИРОВОК:")
    for t_type, data in type_data.items():
        процент = (data['количество'] / total_trainings) * 100
        avg_duration = data['длительность'] / data['количество']
        avg_calories = data['калории'] / data['количество']

        print(f"{t_type.capitalize()}: {data['количество']} тренировок ({процент:.1f}%)")
        print(f"   Средняя длительность: {avg_duration:.0f} мин")
        print(f"   Средние калории: {avg_calories:.0f} ккал\n")


def get_user_workouts(users, workouts, user_name):
    """Получение тренировок пользователя по имени"""
    # Ищем пользователя
    user = next((u for u in users if u['name'].lower() == user_name.lower()), None)

    if not user:
        return []

    # Возвращаем все его тренировки
    return [w for w in workouts if w['user_id'] == user['user_id']]


def analyze_user_performance(users, workouts, user_name):
    """Подробный анализ результатов пользователя"""
    # Находим пользователя
    user = next((u for u in users if u['name'].lower() == user_name.lower()), None)

    if not user:
        print(f"Пользователь '{user_name}' не найден")
        return

    # Получаем его тренировки
    user_trainings = [w for w in workouts if w['user_id'] == user['user_id']]

    if not user_trainings:
        print(f"У пользователя {user_name} нет тренировок")
        return

    # Рассчитываем показатели
    trainings_count = len(user_trainings)
    calories_total = sum(t['calories'] for t in user_trainings)
    time_total = sum(t['duration'] for t in user_trainings) / 60
    distance_total = sum(t['distance'] for t in user_trainings)
    calories_avg = calories_total / trainings_count

    # Определяем предпочтительный тип
    preferred_type = Counter(t['type'] for t in user_trainings).most_common(1)[0][0]

    # Формируем отчет
    print(f"\nАНАЛИЗ РЕЗУЛЬТАТОВ: {user_name}")
    print("=" * 55)
    print(f"Возраст: {user['age']} лет, Вес: {user['weight']} кг")
    print(f"Уровень подготовки: {user['fitness_level']}")
    print(f"Всего тренировок: {trainings_count}")
    print(f"Сожжено калорий: {calories_total}")
    print(f"Общее время: {time_total:.1f} часов")
    print(f"Пройдено расстояние: {distance_total:.1f} км")
    print(f"Средние калории за тренировку: {calories_avg:.0f}")
    print(f"Наиболее частый тип: {preferred_type}")


def execute_analysis():
    """Основная функция для выполнения анализа"""
    users_data = load_users_data()
    workouts_data = load_workouts_data()

    if not users_data or not workouts_data:
        print("Ошибка загрузки данных")
        return

    # Анализ активности
    analyze_user_activity(users_data, workouts_data)

    # Анализ типов тренировок
    analyze_workout_types(workouts_data)

    # Поиск тренировок пользователя
    trainings = get_user_workouts(users_data, workouts_data, "Борис")
    print(f"Найдено тренировок у Бориса: {len(trainings)}")

    # Детальный анализ
    analyze_user_performance(users_data, workouts_data, "Борис")


if __name__ == "__main__":
    execute_analysis()