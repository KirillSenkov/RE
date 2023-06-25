import re
import csv
import codecs as c
from pprint import pprint as pp


def get_phone_formatted(p_phone: str): #  +7(999)999-99-99 доб.9999
   pattern = r'\+?(7|8)[ -]?\(?(\d{3})\)?[ -]?(\d{3})[ -]?(\d{2})[ -]?(\d{2})' \
             r'\s?\(?(доб.)?\)?\s?(\d{4})?\)?'
   patetrn_new = r'+7(\2)\3-\4-\5 \6\7'
   result = re.sub(pattern, patetrn_new, p_phone)
   return result.strip()


def get_fixed_list():
    with c.open('phonebook_raw.csv', 'r', 'utf-8') as f:
        fRdr = csv.reader(f, delimiter=',', lineterminator=r'\n')
        rows_lst = []
        for row in fRdr:
            rows_lst.append(row)
    headers = []
    for header in rows_lst.pop(0):
        headers.append(header)
    fixed_rows_lst = []
    for row in rows_lst:
        row_lst = ['', '', '']
        full_name = row[0] + ' ' + row[1] + ' ' + row[2]
        groups = re.search(r'(\b[а-я]*\b)\s+(\b[а-я]*\b)\s++(\b[а-я]*\b)?',
                           full_name,
                           flags=re.I)
        row_lst[0] = groups[1]
        row_lst[1] = groups[2]
        row_lst[2] = (groups[3] or '')
        for i in range(3, 7):
            if i == 5:
                row_lst.append(get_phone_formatted(row[i]))
            else:
                row_lst.append(row[i])
        fixed_rows_lst.append(row_lst)
    fixed_rows_lst.insert(0, headers)
    return fixed_rows_lst


def merge_doubles(p_lst: list):
    headers = []
    for header in p_lst.pop(0):
        headers.append(header)
    sorted_lst = sorted(p_lst, key=lambda x:x[0])
    prev_row = ['']
    result = []
    for row in sorted_lst:
        if prev_row[0] == row[0]:
            del result[len(result) - 1]
            result.append([(row[0] or prev_row[0]),
                           (row[1] or prev_row[1]),
                           (row[2] or prev_row[2]),
                           (row[3] or prev_row[3]),
                           (row[4] or prev_row[4]),
                           (row[5] or prev_row[5]),
                           (row[6] or prev_row[6]),
                          ])
        else:
            result.append(row)
        prev_row = row
    result.insert(0, headers)
    return result


def create_csv(p_lst: list):
    with c.open('phonebook.csv', 'w', 'utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(p_lst)


if __name__ == '__main__':
    fixed_list = get_fixed_list()
    merged_list = merge_doubles(fixed_list)
    create_csv(merged_list)
    pp(merged_list)