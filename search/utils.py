from unidecode import unidecode


def split_string(input_str):
    list = input_str.split(' ')
    list_remove_accents = []
    for i in range(len(list)):
        list_remove_accents.append(unidecode(list[i]))
    return list + list_remove_accents

