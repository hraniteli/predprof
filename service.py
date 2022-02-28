import csv
from datetime import datetime
import matplotlib.pyplot as plt
from providers import add_data


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
            print(row)
            efficiency = calc_efficiency(row[5:8], row[17:20]) if row[
                14] else -1  # ?????
            add_data(sn=sn, t_start=format_date(row[0]), t_stop=format_date(row[1]), cos_a=float(row[11]),
                     cos_b=float(row[12]), cos_c=float(row[13]),
                     p_a=float(row[5]),
                     p_b=float(row[6]), p_c=float(row[7]), q_a=float(row[2]), q_b=float(row[3]), q_c=float(row[4]),
                     ef=efficiency)


def format_date(data):
    date = data.replace('-', '.')
    date = datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
    return date


def calc_efficiency(on, off):
    sum_on = sum(map(float, on))
    sum_off = sum(map(float, off))
    efficiency = round(((sum_off - sum_on) / sum_off) * 100, 2)
    return efficiency


def get_xls(data):
    res = []
    for d in data:
        res.append([
            d.t_start,
            d.t_stop,
            d.cos_a,
            d.cos_b,
            d.cos_c,
            d.p_a,
            d.p_b,
            d.p_c,
            d.q_a,
            d.q_b,
            d.q_c,
            str(d.ef).replace('.', ',') + '%'
        ])
    xls_name = datetime.timestamp()
    with open(f'tmp/xls/{xls_name}.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        writer.writerows(res)
    return xls_name


def get_grphc(data):
    efficiency = [x.ef for x in data if x.ef != -1]
    date = [x.t_start for x in data if x.ef != -1]
    plt.grid()
    plt.plot(date, efficiency)
    grphc_name = datetime.timestamp()
    plt.savefig(f'tmp/grphc_name/{grphc_name}.png')
    with open(f'tmp/grphc_name/{grphc_name}.png', 'rb') as gr:
        gr = gr.read()
    return gr
