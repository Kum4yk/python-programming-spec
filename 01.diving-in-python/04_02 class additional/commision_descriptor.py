class Value:
    def __init__(self):
        self.value = None

    def __get__(self, obj, obj_type):
        return self.value

    def __set__(self, obj, value):
        if not hasattr(obj, "commission"):
            raise NotImplementedError(
                f"class {type(obj).__name__} has no attribute \"commission\""
            )

        result = value - value * obj.commission
        result = int(result) if result - int(result) == 0 else result
        self.value = result


if __name__ == "__main__":
    def init(self, name):
        self.commission = name

    Test = type(
        "Test",
        (),
        {"amount": Value(), "__init__": init}
    )

    new_account = Test(0.1)
    new_account.amount = 100

    print(new_account.amount)
