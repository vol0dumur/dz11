from collections import UserDict
from collections.abc import Iterator
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.__value = new_value

class Phone(Field):
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if self.__is_phone(new_value):
            raise ValueError("WrongPhone")
        self.__value = new_value

    def __is_phone(self, user_data):
        return not user_data.isnumeric() or len(user_data) != 10
    
class Birthday(Field):
    def __init__(self, value):
        self.__value = datetime(*value)

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.__value = datetime(*new_value)
        today_date = datetime.now()
        if not datetime(today_date.year - 100, today_date.month, today_date.day) <= self.birthday_date <= today_date:
            self.__value = None
            raise ValueError("WrongBirthdayDate")

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, user_data):
        phone = Phone(user_data)
        self.phones.append(phone)

    def remove_phone(self, user_data):
        for phone in self.phones:
            if phone.value == user_data:
                self.phones.remove(phone)
                break
        else:
            raise ValueError("NoSuchRecord")

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.phones.remove(phone)
                self.add_phone(new_phone)
                break
        else:
            raise ValueError("NoSuchRecord")
    
    def find_phone(self, user_data):
        for phone in self.phones:
            if phone.value == user_data:
                return phone
            else:
                raise ValueError("NoSuchRecord")
        
    def add_birthday(self, user_data):
        self.birthday = Birthday(user_data)
    
    def days_to_birthday(self):
        if hasattr(self, "birthday"):

            birthday_date = self.birthday.value.date()
            today = datetime.today().date()
            next_birthday = birthday_date.replace(year=today.year)  # Дата дня народження у поточному році

            if next_birthday < today:                               # Якщо день народження у поточному році вже минув...
                next_birthday = next_birthday.replace(year=today.year + 1)  # встановлюємо ДН на наступний рік

            days_untill_birthday = (next_birthday - today).days     # Отримуємо кількість днів
            
            return days_untill_birthday

    def __str__(self):
        bday = ""
        if hasattr(self, "birthday"):                               # Якщо доданий ДН, то під час друку запису покажемо його
            bday = f", birthday: {self.birthday.value.strftime("%m-%d-%Y")}"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}" + bday

class AddressBook(UserDict):
    def __init__(self, n=3):
        super().__init__()
        self.n = n                          # За замовчуванням 3 (три) записи на сторінку
        self.keys = list(self.data.keys())  # Ключі для ітерації
        self.current_index = 0              # Поточний індекс

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        self.keys = list(self.data.keys())  # Оновлюємо ключі для ітерації

    def find(self, user_data):
        if user_data in self.data:
            return self.data[user_data]
        else:
            raise ValueError("NoSuchRecord")

    def delete(self, user_data):
        if user_data in self.data:
            del self.data[user_data]
        else:
            raise ValueError("NoSuchRecord")
        self.keys = list(self.data.keys())   # Оновлюємо ключі для ітерації
        
    def __str__(self) -> str:
        book_data = ""
        for i in self.data:
            book_data += f"{self.data[i]}\n"
        return book_data[:-1]
    
    def __iter__(self) -> Iterator:
        return self
    
    def __next__(self):
        if self.current_index >= len(self.keys):
            raise StopIteration  # Коли досягли кінця словника
        
        # Беремо наступні N ключів
        end_index = min(self.current_index + self.n, len(self.keys))
        current_keys = self.keys[self.current_index:end_index]
        
        # Оновлюємо індекс на наступну групу ключів
        self.current_index = end_index
        
        current_book_data = ""
        for i in current_keys:
            current_book_data += f"{self.data[i]}\n"
        return current_book_data[:-1]
    
    def set_records_per_page(self, n):
        self.n = n

if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    print("== 1 ==")
    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    print("== 2 ==")
    # Додавання запису John до адресної книги
    book.add_record(john_record)

    print("== 3 ==")
    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print("== 4 ==")
    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    print("== 5 ==")
    # Знаходження та редагування телефону для John
    john = book.find("John")
    print(f"john = {john}")
    john.edit_phone("1234567890", "1112223333")

    print("== 6 ==")
    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
    
    print("== 7 ==")
    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    print("== 8 ==")
    # Видалення запису Jane
    book.delete("Jane")

    print("== 9 ==")
    # Додавання дня народження для John
    john_record.add_birthday((1990, 9, 11))
    print(f"John bithday: {john_record.birthday.value}")

    print("== 10 ==")
    # Перевіряємо скільки днів до наступного дня народження
    print(f"Days to birthday: {john_record.days_to_birthday()}")

    print("== 11 ==")
    # Додаємо запис
    jane_record = Record("Jane", (1995, 5, 1))
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    # Друкуємо всю адресну книгу
    print(book)

    print("== 12 ==")
    # Додаємо багато записів у адресну книгу, щоб було що розбивати на сторінки
    bob_record = Record("Bob", (1988, 12, 11))
    bob_record.add_phone("9876543888")
    book.add_record(bob_record)

    steve_record = Record("Steve", (1999, 6, 18))
    steve_record.add_phone("9876543888")
    book.add_record(steve_record)

    jill_record = Record("Jill", (1992, 3, 13))
    jill_record.add_phone("9812345698")
    book.add_record(jill_record)

    meg_record = Record("Meg", (1998, 7, 11))
    meg_record.add_phone("1232345698")
    book.add_record(meg_record)

    alice_record = Record("Alice", (1996, 9, 20))
    alice_record.add_phone("8642345698")
    book.add_record(alice_record)

    # Друкуємо адресну книгу по сторінках
    book.set_records_per_page(2)
    page = 1
    for i in book:
        print(i)
        print(f"End of page {page}")
        page += 1