import unittest


class TestFactorization(unittest.TestCase):
    def test_simple_multipliers(self):
        x = 77
        a, b = factorize(x)
        self.assertEqual(a * b, 77)


def factorize(x):
    for i in range(2, x):
        if x % i == 0:
            return i, x // i
    return 1, x


if __name__ == "__main__":
    unittest.main()
