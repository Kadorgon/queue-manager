def load_requests(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return [line.strip() for line in f.read().splitlines() if line.strip()]
    except FileNotFoundError:
        return []

def parse_request(line):
    names, numbers, time = line.split(";")
    numbers, names, time = numbers.strip(), names.strip(), time.strip()
    numbers = numbers.upper()
    return [time, names, numbers]

def build_queue(request):
    result = []
    for req_part in request:
        result.append(parse_request(req_part))
    result = sorted(result)

    return result

def format_queue(queue):
    lines = []
    for i, entry in enumerate(queue, 1):
        lines.append(str(i) + ". " + " ".join(entry))
    return "\n".join(lines)

def find_position(queue, plate):
    plate = plate.strip().upper()
    for i, entry in enumerate(queue, 1):
        if entry[2] == plate:
            return i

def next_car(queue, now):
    for entry in queue:
        if entry[0] >= now:
            return entry

def is_valid_time(time):
    if len(time) != 5 or time[2] != ":":
        return False
    hours, minutes = time[:2], time[3:]
    if not (hours.isdigit() and minutes.isdigit()):
        return False
    return int(hours) <= 23 and int(minutes) <= 59

def remove_request(req, plate):
    kept = []
    plate = plate.strip().upper()
    for entry in req:
        names, check_plate, time = entry.split(";")
        check_plate = check_plate.strip().upper()
        if check_plate != plate:
            kept.append(entry)
    return kept

#############################################################################################

requests = load_requests("requests.txt")
queue = build_queue(requests)

#############################################################################################

while True:
    command = input("Команды:\n1 - позиция по номеру\n2 - кто следующий\n3 - вся очередь\n4 - добавление нового водителя\n5 - удаление водителя\nвыход - 'выход': ").strip().lower()
    if command == "1":
        while True:
            text = input("Номер машины (или 'выход'): ")
            if text.strip().lower() == "выход":
                break
            pos = find_position(queue, text)
            if pos is None:
                print('Такой машины нет в очереди')
            else:
                print('Позиция в очереди: ',pos)
    elif command == "2": # Следующий водитель
        while True:
            text = input("Кто следующий в очереди: 'ЧЧ:ММ' (или 'выход'): ")
            if text.strip().lower() == "выход":
                break
            if not is_valid_time(text):
                print('Неверное время. Нужно ЧЧ:ММ, например 09:15')
                continue
            car = next_car(queue, text)
            if car is None:
                print('Очередь закончилась')
            else:
                print('Следующий: ', " ".join(car))

    elif command == "3": #Очередь
        print(format_queue(queue))
    elif command == "4": #Добавление водителя
        while True:
            text = input("Фамилия;номер;время\nвыход - 'выход': ")
            if text.strip().lower() == "выход":
                break
            try:
                parsed = parse_request(text)
                if not is_valid_time(parsed[0]):
                    print('Неверное время. Нужно ЧЧ:ММ, например 09:15')
                    continue
                if find_position(queue, parsed[2]) != None:
                    print('Этот водитель уже есть в очереди')
                    continue
                requests.append(text)
                with open("requests.txt", "a", encoding="utf-8") as f:
                    f.write("\n" + text)
                queue = build_queue(requests)
                print('Заявка добавлена')
            except ValueError:
                print('Неверный формат. Нужно: Фамилия;номер;время')

    elif command == "5": #Удаление водителя
        while True:
            text = input("Введите номер авто или выход - 'выход': ")
            if text.strip().lower() == "выход":
                break
            if find_position(queue, text) is None:
                print('Такой машины нет в списке')
                continue
            requests = remove_request(requests,text)
            with open("requests.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(requests))
            queue = build_queue(requests)
            print('Заявка удалена')

    elif command == 'выход': # Выход из программы
        break
    else:
        print('Такой команды нет! Введите корректную команду.')
