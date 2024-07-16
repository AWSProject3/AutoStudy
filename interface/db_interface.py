from abc import ABC, abstractmethod

from models.orm import Quiz

class DBInterface(ABC):
    @abstractmethod
    def get_quiz_list(self, user: dict) -> list[Quiz]:
        pass

    @abstractmethod
    def save_quiz(self, quiz_data: dict, user: dict) -> None:
        pass