from abc import ABC, abstractmethod

""" 
class Engine:
    pass
"""


class ObservableEngine(Engine):

    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, sub):
        self.__subscribers.add(sub)

    def unsubscribe(self, sub):
        self.__subscribers.remove(sub)

    def notify(self, message):
        for sub in self.__subscribers:
            sub.update(message)

# ------------ Observers -------------


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, message: dict):
        pass


class ShortNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements: set = set()

    def update(self, message):
        """
        у ShortNotificationPrinter хранится множество названий полученных достижений
        """
        achieve = message["title"]
        self.achievements.add(achieve)


class FullNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements: list = list()
        self.__set_achieve: set = set()  # fast but memory expensive

    def update(self, message):
        """
        у FullNotificationPrinter хранится список достижений в том порядке,
         в котором они генерируются Engine
        """
        if message not in self.__set_achieve:
            self.__set_achieve.add(message)
            self.achievements.append(message)

