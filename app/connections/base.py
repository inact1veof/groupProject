from abc import ABC, abstractmethod


class BaseConnection(ABC):
    """
    Базовый класс для работ с БД.
    """

    def __int__(self) -> None:
        """
        Конструктор.

        :param connection: Соединение с БД
        """
        self.connection = None

    @abstractmethod
    def conncet(self) -> None:
        """
        Соединение с БД
        :return:
        """