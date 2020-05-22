import unittest


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        for x in ("string", 1.5):
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        for x in (-1,  -10,  -100):
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        for x, ans in enumerate(((0, ), (1, ))):
            with self.subTest(x=x):
                self.assertTupleEqual(factorize(x), ans)

    def test_simple_numbers(self):
        x_ = (3, 13, 29)
        ans_ = ((3, ), (13, ), (29, ))
        for x, ans in zip(x_, ans_):
            with self.subTest(x=x):
                self.assertTupleEqual(factorize(x), ans)

    def test_two_simple_multipliers(self):
        x_ = (6, 26, 121)
        ans_ = ((2, 3), (2, 13), (11, 11))
        for x, ans in zip(x_, ans_):
            with self.subTest(x=x):
                self.assertTupleEqual(factorize(x), ans)

    def test_many_multipliers(self):
        x_ = (1001, 9699690)
        ans_ = ((7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19))
        for x, ans in zip(x_, ans_):
            with self.subTest(x=x):
                self.assertTupleEqual(factorize(x), ans)


'''
def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    pass
'''
