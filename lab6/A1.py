import xml.etree.ElementTree as ET


def load_users_data():
    """Загружает данные о пользователях из файла users.xml"""
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
    """Загружает данные о тренировках из файла workouts.xml"""
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

def get_stats(users, workouts):
    """Рассчитывает общую статистику по всем тренировкам"""
    total_workouts = len(workouts)
    total_users = len(users)
    total_calories = sum(workout['calories'] for workout in workouts)
    total_time_hours = sum(workout['duration'] for workout in workouts) / 60
    total_distance = sum(workout['distance'] for workout in workouts)

    print("ОБЩАЯ СТАТИСТИКА")
    print(f"Всего тренировок: {total_workouts}")
    print(f"Всего пользователей: {total_users}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {total_time_hours:.1f} часов")
    print(f"Пройдено дистанции: {total_distance:.1f} км")

# Основной блок программы
if __name__ == "__main__":
    # Загрузка данных
    users_data = load_users_data()
    workouts_data = load_workouts_data()

    # Проверка загрузки данных
    if users_data and workouts_data:
        print(f"Загружено пользователей: {len(users_data)}")
        print(f"Загружено тренировок: {len(workouts_data)}")
        print()

        # Расчет и вывод статистики
        get_stats(users_data, workouts_data)
    else:
        print("Не удалось загрузить данные. Проверьте наличие файлов users.xml и workouts.xml")
