from math import log
from abc import ABC, abstractmethod
from numbers import Number


class Base(ABC):
    def __len__(self, data, result):
        self.data = data
        self.result = result

    def get_answer(self) -> list:
        return [int(x >= 0.5) for x in self.data]

    @abstractmethod
    def get_score(self) -> Number:
        pass

    @abstractmethod
    def get_loss(self) -> Number:
        pass


class A(Base):
    def get_score(self) -> Number:
        ans = self.get_answer()
        return sum([int(x == y) for (x, y) in zip(ans, self.result)]) \
            / len(ans)

    def get_loss(self) -> Number:
        return sum(
            [(x - y) * (x - y) for (x, y) in zip(self.data, self.result)])


class B(A):
    def get_loss(self) -> Number:
        return -sum([
            y * log(x) + (1 - y) * log(1 - x)
            for (x, y) in zip(self.data, self.result)
        ])

    def get_pre(self) -> Number:
        ans = self.get_answer()
        res = [int(x == 1 and y == 1) for (x, y) in zip(ans, self.result)]
        return sum(res) / sum(ans)

    def get_rec(self) -> Number:
        ans = self.get_answer()
        res = [int(x == 1 and y == 1) for (x, y) in zip(ans, self.result)]
        return sum(res) / sum(self.result)

    def get_score(self):
        pre = self.get_pre()
        rec = self.get_rec()
        return 2 * pre * rec / (pre + rec)


class C(A):
    def get_loss(self) -> Number:
        return sum([abs(x - y) for (x, y) in zip(self.data, self.result)])
