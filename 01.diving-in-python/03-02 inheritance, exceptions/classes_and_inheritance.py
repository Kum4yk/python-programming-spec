import csv


class CarBase:
    def __init__(self, brand: str, photo_file_name: str, carrying: float):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return "." + self.photo_file_name.split(".")[-1]
    
    @property
    def car_type(self):
        raise NotImplementedError

class Car(CarBase):
    car_type = "car"
    
    def __init__(self, brand: str, photo_file_name: str, carrying: float, passenger_seats_count: int):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    car_type = "truck"
    
    def __init__(self, brand: str, photo_file_name: str, carrying: float, body_whl: str):
        super().__init__(brand, photo_file_name, carrying)
        self.body_length, self.body_width, self.body_height = Truck.take_values_from_str(body_whl)

    @staticmethod
    def take_values_from_str(body_whl):
        answer = (0.0, 0.0, 0.0)
        body_whl = body_whl.split("x")
        if len(body_whl) == 3:
            try:
                answer = map(float, body_whl)
            except ValueError:
                answer = (0.0, 0.0, 0.0)
        return answer

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = "spec_machine"
    
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def check_params(car_type: str, brand: str, passenger_seat_count: str,
                 photo_file_name: str, body_whl, carrying: str, extra: str):
    car_type = car_type.lower()
    possible_cars = {"car", "truck", "spec_machine"}

    if car_type not in possible_cars:
        return False
    if not brand:
        return False
    if photo_file_name.split(".")[-1] not in {"jpg", "jpeg", "png", "gif"}:
        return False

    if car_type == "car" and (not passenger_seat_count or not passenger_seat_count.isdigit()):
        return False
    if car_type == "spec_machine" and not extra:
        return False

    try:
        float(carrying)
    except ValueError:
        return False

    return True


def create_vehicle_from_params(params):
    car_type, brand, passenger_seats_count, photo_file_name, body_whl, carrying, extra = params
    carry = float(carrying)
    
    if car_type == "car":
        seats = int(passenger_seats_count)
        return Car(brand, photo_file_name, carry, seats)

    if car_type == "truck":
        return Truck(brand, photo_file_name, carry, body_whl)

    return SpecMachine(brand, photo_file_name, carry, extra)


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if len(row) != 7 or not check_params(*row):
                continue
            car_list.append(create_vehicle_from_params(row))
    return car_list


if __name__ == "__main__":
    cars = get_car_list("coursera_week3_cars.csv")
    for car in cars:
        print(type(car))
    print(cars[0].passenger_seats_count)
    print(cars[1].get_body_volume())
