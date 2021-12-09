import enum
import math
import os
from io import StringIO

NEWLINE = os.linesep

NUM_COACH_ROWS: int = 10
NUM_FC_ROWS: int = 4
NUM_COACH_SEATS_PER_ROW: int = 4
NUM_FC_SEATS_PER_ROW: int = 2

EMPTY_STR: str = ""
SPACE: str = " "
BAR: str = "="
EMPTY_MAP: map = {}
EMPTY_LIST: list = []


class Passenger:
    DISCOUNT_LOW_AGE: int = 6
    DISCOUNT_HIGH_AGE: int = 65
    AGE_DISCOUNT: float = 0.2
    MIN_AGE = 0
    MAX_AGE = 130

    def __init__(self, name: str, age: int):

        self.__passenger_name: str = EMPTY_STR
        self.__age: int = -1
        self.__tax_rate = 0.0
        self.__set_data(name, age)

    def get_tax_rate(self) -> float:
        return self.__tax_rate

    def set_tax_rate(self, new_rate: float):
        self.__tax_rate = new_rate

    def get_name(self) -> str:
        return self.__passenger_name

    def __set_name(self, name: str):
        self.__validate_passenger_name(name)
        self.__age = name

    @staticmethod
    def __validate_passenger_name(name):
        if name == EMPTY_STR:
            raise Exception("Name is unspecified")
        elif not name.isalnum():
            raise Exception(f"Name '{name}' contains invalid characters")

    def get_age(self) -> int:
        return self.__age

    def __set_age(self, age: int):
        self.__validate_age(age)
        self.__age = age

    @classmethod
    def __validate_age(cls, age):
        if age < cls.MIN_AGE or age > cls.MAX_AGE:
            raise Exception(f"Age, '{age}' is out of bounds ({cls.MIN_AGE} to {cls.MAX_AGE})")

    def get_discount_rate(self) -> float:
        age: int = self.get_age()
        return 0.0 if age in range(Passenger.DISCOUNT_LOW_AGE, Passenger.DISCOUNT_HIGH_AGE) else 0.2

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)
                and self.get_age() == other.get_age()
                and self.get_name() == other.get_name())

    def copy(self) -> 'Passenger':
        duplicate: Passenger = Passenger(name=self.get_name(), age=self.get_age())
        return duplicate

    def __set_data(self, name: str, age: int):
        errs: str = EMPTY_STR
        try:
            self.__set_name(name=name)
        except Exception as e:
            errs.join(f'{e}{NEWLINE}')
        try:
            self.__set_age(age=age)
        except Exception as e:
            errs.join(f'{e}{NEWLINE}')
        if errs != EMPTY_STR:
            errs = errs.rstrip(errs[-1])
            raise Exception(errs)


class Tier(enum.Enum):
    coach = ["COACH", 19900]
    first_class = ["FIRST CLASS", 50000]

    def get_tier_name(self) -> str:
        return self.value[0]

    def get_tier_base_cost_cents(self) -> int:
        return self.value[1]


class Seat:
    NO_PASSENGER = None

    def __init__(self, seat_letter: str, row_number: int, tier):
        self.__seat_letter: str = seat_letter
        self.__row_number: int = row_number
        self.__tier: Tier = tier
        self.__passenger = self.NO_PASSENGER

    def is_taken(self) -> bool:
        return self.__passenger is not self.NO_PASSENGER

    def assign_passenger(self, passenger: Passenger):
        old_passenger: Passenger = self.__get_passenger()
        if old_passenger == self.NO_PASSENGER:
            self.__passenger = passenger
        else:
            self.__raise_seat_taken_exception()

    def __raise_seat_taken_exception(self):
        name = self.__passenger.get_name()
        tier_name = self.get_tier().get_tier_name()
        row_number = self.get_row_number()
        seat_letter = self.get_seat_letter()
        msg = f"{tier_name} seat ;{row_number}-{seat_letter}; is already booked by {name}"
        raise Exception(msg)

    def remove_passenger(self):
        self.__passenger = self.NO_PASSENGER

    def get_row_number(self) -> int:
        return self.__row_number

    def get_seat_letter(self):
        return self.__seat_letter

    def get_tier(self) -> Tier:
        return self.__tier

    def get_price_cents(self, passenger=NO_PASSENGER) -> int:
        passenger = self.__get_passenger() if (passenger == self.NO_PASSENGER) else passenger
        self.__validate_passenger_existance(passenger)
        validated_passenger: Passenger = passenger
        tier_price = self.get_tier().get_tier_base_cost_cents()
        discount_rate = validated_passenger.get_discount_rate()
        tax_rate = validated_passenger.get_tax_rate()
        total_price = (tier_price * (1 - discount_rate)) * (1 + tax_rate)
        return int(total_price)

    def __validate_passenger_existance(self, passenger):
        if passenger == self.NO_PASSENGER:
            raise Exception("No Passenger supplied or found for price comparison")

    def compare_cost_cents(self, seat: 'Seat') -> int:
        self.__validate_seat_move_possible(seat)
        new_seat_copy = seat.copy()
        new_seat_cost = new_seat_copy.get_price_cents(self.__get_passenger())
        return max(0, new_seat_cost - self.get_price_cents())

    def __validate_seat_move_possible(self, seat):
        if seat.is_taken():
            raise Exception("That seat is already taken")
        if not self.is_taken():
            raise Exception("Unable to compare seat cost without a passenger")

    def copy(self) -> 'Seat':
        seat: Seat = Seat(row_number=self.get_row_number(), seat_letter=self.get_seat_letter(), tier=self.get_tier())
        return seat

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)
                and self.get_seat_letter() == other.__get_letter()
                and self.get_row_number() == other.__get_number()
                and self.get_tier() == other.__get_tier())

    def __get_passenger(self) -> Passenger:
        return self.__passenger


class SeatingStructure:
    UNINITIALIZED_INT = -1
    UNICODE_BASE: int = 65
    MAX_NAME_DISPLAY_LEN: int = 12
    OPEN_SEAT_NAME: str = "OPEN"
    PRINT_HEADER_TEXT: str = "SEATING ASSIGNMENTS"
    CELL_SEPARATOR: str = "|"
    SPACE: str = " "
    INNER_CELL_WIDTH: int = MAX_NAME_DISPLAY_LEN + 2
    OUTER_CELL_WIDTH: int = INNER_CELL_WIDTH + 2 * len(CELL_SEPARATOR)

    def __init__(self, fc_rows, fc_seats, coach_rows, coach_seats):
        self.__structure: dict = EMPTY_MAP
        self.__seating_options: map = EMPTY_MAP
        self.__row_options: map = EMPTY_MAP
        self.__header_width: int = coach_seats * self.OUTER_CELL_WIDTH
        self.__subheader_width: int = fc_seats * self.OUTER_CELL_WIDTH
        self.__side_marker_size: int = len(str(coach_rows))
        self.__title_bar_header: str = EMPTY_STR
        self.__tier_headers: dict = EMPTY_MAP
        self.__seat_headers: dict = EMPTY_MAP

        self.__populate_options(tier=Tier.coach, rows=coach_rows, seats=coach_seats)
        self.__populate_options(tier=Tier.first_class, rows=fc_rows, seats=fc_seats)
        for tier in Tier:
            self.__populate_seating_tier(tier=tier,
                                         rows=self.get_row_options(tier),
                                         seats=self.get_seat_options(tier),
                                         structure=self.__structure)

    def __populate_options(self, tier: Tier, rows: int, seats: int):
        self.__seating_options[tier] = self.__generate_seat_options(seats)
        self.__row_options[tier] = self.__generate_row_options(rows)

    @staticmethod
    def __populate_seating_tier(tier: Tier, structure: map, rows: list, seats: list):
        seat_list: dict = EMPTY_MAP
        for row_number in rows:
            row: dict = EMPTY_MAP
            for seat_letter in seats:
                seat: Seat = Seat(tier=tier, seat_letter=seat_letter, row_number=row_number)
                row[seat_letter] = seat
            seat_list[row_number] = row
        structure[tier] = seat_list

    def set_seat(self, new_seat: Seat):
        self.__validate_seat_existence(new_seat)
        tier: str = new_seat.get_tier().get_tier_name()
        row_number: int = new_seat.get_row_number()
        seat_letter: str = new_seat.get_seat_letter()
        self.__get_structure()[tier][row_number][seat_letter] = new_seat

    def __validate_seat_existence(self, new_seat):
        errs = EMPTY_STR
        tier: Tier = new_seat.get_tier()
        row_number = new_seat.get_row_number()
        seat_letter = new_seat.get_seat_letter()
        if row_number not in self.get_row_options(tier):
            range_first = self.get_row_options(tier)[0]
            range_last = self.get_row_options(tier)[-1]
            errs.join(f"Row number '{tier.get_tier_name()}:{row_number}' does not exist on this flight{NEWLINE}.")
            errs.join(f"Rows in {tier.get_tier_name()} range from {range_first} to {range_last}{NEWLINE}.")
        if seat_letter not in self.get_seat_options(tier):
            range_first = self.get_seat_options(tier)[0]
            range_last = self.get_seat_options(tier)[-1]
            errs.join(f"Seat letter '{tier.get_tier_name()}:{seat_letter}' does not exist on this flight{NEWLINE}.")
            errs.join(f"Seats in {tier.get_tier_name()} range from {range_first} to {range_last}{NEWLINE}.")
        if errs != EMPTY_STR:
            errs = errs.rstrip(errs[-1])  # strip off newline
            raise Exception(errs)

    def get_seat(self, tier: Tier, row_number: int, seat_letter: str) -> Seat:
        return self.__get_structure()[tier][row_number][seat_letter]

    def __str__(self):
        return self.__generate_printout()

    @classmethod
    def __generate_seat_options(cls, size) -> list:
        return list(map(chr, range(cls.UNICODE_BASE, cls.UNICODE_BASE + size)))

    @classmethod
    def __generate_row_options(cls, size) -> list:
        return list(range(1, size + 1))

    def get_row_options(self, tier: Tier) -> list:
        return self.__row_options[tier]

    def get_seat_options(self, tier: Tier) -> list:
        return self.__seating_options[tier]

    def __get_solid_header_bar(self) -> str:
        return self.__header_width * BAR

    def __get_tier_header(self, tier: Tier) -> str:
        if tier not in self.__tier_headers.keys():
            self.__generate_tier_header(tier)
        return self.__tier_headers[tier]

    def __build_grid_section(self, tier: Tier):
        builder: StringIO = StringIO()
        builder.write(self.__get_tier_header(tier))
        rows = self.__get_structure()[tier]
        for row in rows.keys():
            for seat in rows[row].keys():
                builder.write(self.__build_cell(self.__structure[tier][row][seat]))
            builder.write(NEWLINE)
        return builder.getvalue()

    def __generate_printout(self) -> str:
        builder: StringIO = StringIO()
        builder.write(f'{self.__create_title_bar_header(width=self.__header_width, text="some text")}{NEWLINE}')
        builder.write(f'{self.__create_title_bar_header(width=self.__header_width, text="some tex")}')
        return builder.getvalue()

    @classmethod
    def __build_cell(cls, name=OPEN_SEAT_NAME) -> str:
        gap = cls.MAX_NAME_DISPLAY_LEN - len(name)
        data_str = EMPTY_STR
        if gap < 0:
            data_str = data_str[0: cls.MAX_NAME_DISPLAY_LEN:]
        else:
            data_str = f'{SPACE}{name}{SPACE}'
        flip_flop: bool = True
        while len(data_str) < cls.INNER_CELL_WIDTH:
            data_str = data_str.join(SPACE) if flip_flop else SPACE.join(data_str)
            flip_flop = not flip_flop
        return f'{cls.CELL_SEPARATOR}{data_str}{cls.CELL_SEPARATOR}'

    @classmethod
    def __create_title_bar_header(cls, width: int, text: str = EMPTY_STR, outer_buffer_width: int = 0) -> str:
        if text != EMPTY_STR:
            text = f'{SPACE}{text}{SPACE}'
        if len(text) > width:
            raise Exception(f"Cannot fit the text '{text}' within a header of length {width}")
        side_width: float = (width - 2 * outer_buffer_width - len(text))/2
        first_bar_width: int = math.floor(side_width)
        last_bar_width: int = math.ceil(side_width)
        first_bar: str = first_bar_width * BAR
        last_bar: str = last_bar_width * BAR
        end_buffer: str = SPACE * outer_buffer_width
        return f'{end_buffer}{first_bar}{text}{last_bar}{end_buffer}'

    def __generate_tier_header(self, tier: Tier):
        # TODO:
        pass

    def __generate_seat_header(self, tier: Tier):
        # TODO:
        pass

    def __initialize_structures(self):
        # todo:
        pass

    def __get_structure(self):
        return self.__structure


s: SeatingStructure = SeatingStructure(fc_rows=NUM_FC_ROWS,
                                       coach_rows=NUM_COACH_ROWS,
                                       fc_seats=NUM_FC_SEATS_PER_ROW,
                                       coach_seats=NUM_COACH_SEATS_PER_ROW)
print(s)
