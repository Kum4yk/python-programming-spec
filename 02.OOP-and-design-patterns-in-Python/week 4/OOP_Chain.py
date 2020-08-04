class SomeObject:
    def __init__(self, integer_field=0, float_field=0.0, string_field=""):
        self.integer_field = integer_field
        self.float_field = float_field
        self.string_field = string_field


event_dict = {int: "INT", str: "STR", float: "FLOAT"}


class EventGet:
    """
    EventGet(<type>) создаёт событие получения данных соответствующего типа
    """
    def __init__(self, _type):
        self.kind = event_dict[_type]


class EventSet:
    """
    EventSet(<value>) создаёт событие изменения поля типа type(<value>)
    """
    def __init__(self, value):
        self.kind = event_dict[type(value)]
        self.value = value


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, char, event):
        if self.__successor is not None:
            return self.__successor.handle(char, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == "INT":
            if isinstance(event, EventGet):
                return obj.integer_field
            else:
                obj.integer_field = event.value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == "STR":
            if isinstance(event, EventGet):
                return obj.string_field
            else:
                obj.string_field = event.value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == "FLOAT":
            if isinstance(event, EventGet):
                return obj.float_field
            else:
                obj.float_field = event.value
        else:
            return super().handle(obj, event)


if __name__ == "__main__":
    test = SomeObject()
    test.integer_field = 42
    test.float_field = 3.14
    test.string_field = "some text"

    chain = IntHandler(FloatHandler(StrHandler(NullHandler())))

    print(chain.handle(test, EventGet(int)), "1")
    print(chain.handle(test, EventGet(float)), "2")
    print(chain.handle(test, EventGet(str)), "3")

    print(chain.handle(test, EventSet(100)), "4")
    print(chain.handle(test, EventGet(int)), "5")

    print(chain.handle(test, EventSet(0.5)), "6")
    print(chain.handle(test, EventGet(float)), "7")

    print(chain.handle(test, EventSet("new text")), "8")
    print(chain.handle(test, EventGet(str)), "9")

    test = SomeObject(integer_field=76, float_field=15.7546, string_field="OxMYqF")
    print(chain.handle(test, EventGet(int)))

    test = SomeObject(integer_field=33, float_field=-15.0501, string_field="jSxvNm")
    print(chain.handle(test, EventGet(float)))
