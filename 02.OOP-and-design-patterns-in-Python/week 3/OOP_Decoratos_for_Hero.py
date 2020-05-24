from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(ABC, Hero):
    def __init__(self, base):
        self.base = base

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        pass


# --------------------------- Positives

class AbstractPositive(AbstractEffect):
    def get_positive_effects(self):
        pos_effects: list = self.base.get_positive_effects()
        pos_effects.append(self.__class__.__name__)
        return pos_effects

    def get_stats(self):
        pass


class Berserk(AbstractPositive):
    __pos = 7
    __negs = -3
    effects = (
        ("Strength", __pos), ("Endurance", __pos), ("Agility", __pos),
        ("Luck", __pos), ("Perception", __negs), ("Charisma", __negs),
        ("Intelligence", __negs), ("HP", 50),
    )

    def get_stats(self):
        new_stats: dict = self.base.get_stats()
        for name, value in Berserk.effects:
            new_stats[name] += value
        return new_stats


class Blessing(AbstractPositive):
    def get_stats(self):
        new_stats: dict = self.base.get_stats()
        for name in new_stats.keys():
            if name in ("HP", "MP", "SP"):
                continue
            new_stats[name] += 2
        return new_stats


# --------------------------- Negatives
class AbstractNegative(AbstractEffect):
    def get_negative_effects(self):
        new_negative: list = self.base.get_negative_effects()
        new_negative.append(self.__class__.__name__)
        return new_negative

    def get_stats(self):
        pass


class Weakness(AbstractNegative):
    def get_stats(self):
        new_stats: dict = self.base.get_stats()
        for name in ("Strength", "Endurance", "Agility"):
            new_stats[name] -= 4
        return new_stats


class EvilEye(AbstractNegative):
    def get_stats(self):
        new_stats: dict = self.base.get_stats()
        new_stats["Luck"] -= 10
        return new_stats


class Curse(AbstractNegative):
    def get_stats(self):
        new_stats: dict = self.base.get_stats()
        for name in new_stats.keys():
            if name in ("HP", "MP", "SP"):
                continue
            new_stats[name] -= 2
        return new_stats


if __name__ == "__main__":
    hero = Hero()
    print(hero.get_stats())
    print(hero.stats)
    print(hero.get_negative_effects())
    print(hero.get_positive_effects())
    # накладываем эффект
    brs1 = Berserk(hero)
    print(brs1.get_stats())
    print(brs1.get_negative_effects())
    print(brs1.get_positive_effects())
    # накладываем эффекты
    brs2 = Berserk(brs1)
    cur1 = Curse(brs2)
    print(cur1.get_stats())
    print(cur1.get_positive_effects())
    print(cur1.get_negative_effects())
    # снимаем эффект Berserk
    cur1.base = brs1
    print(cur1.get_stats())
    print(cur1.get_positive_effects())
    print(cur1.get_negative_effects())
