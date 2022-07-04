class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000  # Коэффициент перевода м в км
    LEN_STEP: float = 0.65  # Длина одного шага

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получаем дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращаем информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.__class__.__name__, self.duration,
                self.get_distance(), self.get_mean_speed(),
                self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        coeff_callorie_1: int = 18  # Коэффициент 1 для расчета калорий
        coeff_callorie_2: int = 20  # Коэффициент 2 для расчета калорий
        duration_minutes = self.duration * 60  # Переводим время в минуты
        spent_calories = ((coeff_callorie_1 * self.get_mean_speed()
                          - coeff_callorie_2) * self.weight / self.M_IN_KM
                          * duration_minutes)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        coeff_callorie_3: float = 0.035  # Коэффициент 3 для расчета калорий
        coeff_callorie_4: int = 2  # Коэффициент 4 для расчета калорий
        coeff_callorie_5: float = 0.029  # Коэффициент 5 для расчета калорий
        duration_minutes = self.duration * 60  # Переводим время в минуты
        spent_calories = ((coeff_callorie_3 * self.weight
                          + (self.get_mean_speed() ** coeff_callorie_4
                             // self.height) * coeff_callorie_5 * self.weight)
                          * duration_minutes)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # Длина одного гребка

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        coeff_callorie_6: float = 1.1
        coeff_callorie_7: int = 2
        spent_calories = ((self.get_mean_speed() + coeff_callorie_6)
                          * coeff_callorie_7 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Получаем данные полученные от датчиков."""
    trainings: dict[str, training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
