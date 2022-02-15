import csv
from datetime import datetime
import matplotlib.pyplot as plt

res_data = []
def parse_file(_file, sn, file_name):
    _file = _file.split(';')
    x = 26
    while x < len(_file):
        _file[x] = _file[x][:-20] + '\n' + _file[x][1:] if len(_file) - x != 1 else _file[x]
        x += 26
    _file = ';'.join(_file)
    with open(file_name, 'w') as fd:
        fd.write(_file)

    with open(file_name, 'r') as fd:
        reader = csv.reader(fd, delimiter=';')
        for row in reader:
            mes_data = []
            mes_data.append(format_date(row[0]))
            mes_data.append(format_date(row[1]))
            mes_data.append(float(row[11]))
            mes_data.append(float(row[12]))
            mes_data.append(float(row[13]))
            mes_data.append(float(row[5]))
            mes_data.append(float(row[6]))
            mes_data.append(float(row[7]))
            mes_data.append(float(row[8]))
            mes_data.append(float(row[9]))
            mes_data.append(float(row[10]))
            if row[14]:
                efficiency = calc_effeciency(row[5:8], row[17:20])
                mes_data.append(efficiency)
            else:
                mes_data.append(None)
            mes_data.append(sn)
            global res_data
            res_data.append(mes_data)
            res_data.sort(key= lambda x: x[0])


def format_date(data):
    date = data.replace('-', '.')
    date = datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
    return date


def calc_effeciency(on, off):
    sum_on = sum(map(float, on))
    sum_off = sum(map(float, off))
    efficiency = round(((sum_off - sum_on) / sum_off) * 100, 2)
    return efficiency


def get_grphc(date, data):
    call_data = list(
        filter(lambda x: datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) < x[0] < datetime.now(),
               data)) \
        if date == 'day' else \
        list(
            filter(lambda x: datetime.now().replace(day=datetime.now().day - 7, hour=0, minute=0, second=0,
                                                    microsecond=0) < x[0] < datetime.now(), data))
    effeciency = [x[11] for x in call_data if x[11]]
    date = [datetime.strftime(x[0], '%d.%m.%Y %H:%M:%S') for x in call_data if x[11]]
    plt.plot(date, effeciency)
    plt.savefig('tmp/test.png')
    with open('tmp/test.png', 'rb') as gr:
        gr = gr.read()
    return gr


def get_xls():
    with open('tmp/example.csv', 'rb') as fd:
        data = fd.read()
        return data


