from typing import Dict, Type
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    HOUR_IN_MUNUTES: float = 60
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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        raise NotImplementedError(
            'Определите run в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Возвращаем информационное сообщение о выполненной тренировке."""
        return (InfoMessage(type(self).__name__, self.duration,
                self.get_distance(), self.get_mean_speed(),
                self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""

    COEFF_MEAN_SPEED_1: float = 18  # Коэффициент средней скорости 1
    COEFF_MEAN_SPEED_2: float = 20  # Коэффициент средней скорости 2

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        return ((self.COEFF_MEAN_SPEED_1 * self.get_mean_speed()
                - self.COEFF_MEAN_SPEED_2) * self.weight / self.M_IN_KM
                * self.duration * self.HOUR_IN_MUNUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    EXP_MEAN_SPEED: float = 2  # " Экспонента средней скорости
    COEFF_WEIGHT_1: float = 0.035  # Коэффициент веса 1
    COEFF_WEIGHT_2: float = 0.029  # Коэффициент веса 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        return ((self.COEFF_WEIGHT_1 * self.weight + (self.get_mean_speed()
                ** self.EXP_MEAN_SPEED // self.height) * self.COEFF_WEIGHT_2
                * self.weight) * self.duration * self.HOUR_IN_MUNUTES)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # Длина одного гребка
    COEFF_MEAN_SPEED: float = 1.1  # Коэффициент средней скорости
    COEFF_WEIGHT: float = 2  # Коэффициент веса

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_MEAN_SPEED)
                * self.COEFF_WEIGHT * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Получаем данные полученные от датчиков."""
    types_trainings: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in types_trainings:
        raise ValueError(f'Тип тренировки "{workout_type}" не определен')
    return types_trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
