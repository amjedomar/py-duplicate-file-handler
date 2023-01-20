import sys
import os
from hashlib import md5


def parse_dir_path():
    args = sys.argv
    return args[1] if len(args) > 1 else None


def prompt_file_format():
    print('Enter file format:')
    return input()


def prompt_sort_direction():
    print('Size sorting options:')
    print('1. Descending')
    print('2. Ascending')

    while True:
        print('\nEnter a sorting option:')
        chose = input()
        if chose == "1":
            return 'desc'
        elif chose == '2':
            return 'asc'
        else:
            print('\nWrong option')


def prompt_bool_question(msg):
    print(f'\n{msg}')
    chose = input()
    if chose == 'yes':
        return True
    elif chose == 'no':
        return False
    else:
        print('Wrong option')
        return prompt_bool_question(msg)


def prompt_int_list(msg, upperbound):
    print(f'\n{msg}')
    wrong_msg = 'Wrong format'

    inputted_str = input()

    if not inputted_str:
        print(wrong_msg)
        return prompt_int_list(msg, upperbound)

    str_list = inputted_str.split(' ')
    int_list = []
    for str_item in str_list:
        int_item = int(str_item) if str_item.isdigit() else None
        if int_item is None or int_item > upperbound:
            print(wrong_msg)
            return prompt_int_list(msg, upperbound)
        int_list.append(int_item)
    return int_list


def get_files(dir_path, file_format='', is_asc=True):
    grouped_files = {}

    for root_path, dirs, files in os.walk(dir_path):
        for file in files:
            file_ext = os.path.splitext(file)[-1][1:]

            if file_format and file_format != file_ext:
                continue

            file_path = os.path.join(root_path, file)
            file_size = os.path.getsize(file_path)

            if file_size not in grouped_files:
                grouped_files[file_size] = []

            grouped_files[file_size].append(file_path)

    sorted_grouped_files = {}

    for size in sorted(grouped_files.keys(), reverse=not is_asc):
        sorted_grouped_files[size] = grouped_files[size]

    return sorted_grouped_files


def print_sorted_files(grouped_files):
    for size in grouped_files:
        print(f'\n{size} bytes')
        for file in grouped_files[size]:
            print(file)


def print_duplicated_files(grouped_files):
    cur_file_num = 0

    duplicated_files = []

    for size in grouped_files:
        files = grouped_files[size]
        if len(files) > 1:
            hashed_files = {}
            is_have_duplicates = False

            for file_path in files:
                with open(file_path, mode='rb') as f:
                    file_data = f.read()
                    file_hash = md5(file_data).hexdigest()
                    if file_hash not in hashed_files:
                        hashed_files[file_hash] = []
                    hashed_files[file_hash].append(file_path)
                    if len(hashed_files[file_hash]) > 1:
                        is_have_duplicates = True

            if is_have_duplicates:
                print(f'\n{size} bytes')
                for file_hash in hashed_files:
                    hash_duplicated_files = hashed_files[file_hash]
                    if len(hash_duplicated_files) > 1:
                        print(f'Hash: {file_hash}')
                        for duplicated_file in hash_duplicated_files:
                            cur_file_num += 1
                            print(f'{cur_file_num}.', duplicated_file)
                            duplicated_files.append(duplicated_file)

    return duplicated_files


def delete_files(files, delete_positions):
    freed_space = 0

    for file_pos in delete_positions:
        file_idx = file_pos - 1
        file_path = files[file_idx]
        freed_space += os.path.getsize(file_path)
        os.remove(file_path)

    print(f'\nTotal freed up space: {freed_space} bytes')


def main():
    dir_path = parse_dir_path()

    if not dir_path:
        return print('Directory is not specified')

    file_format = prompt_file_format()
    is_asc = prompt_sort_direction() == 'asc'
    grouped_files = get_files(dir_path, file_format, is_asc)

    print_sorted_files(grouped_files)

    is_check_duplicates = prompt_bool_question('Check for duplicates?')

    if not is_check_duplicates:
        return

    duplicated_files = print_duplicated_files(grouped_files)

    is_delete_files = prompt_bool_question('Delete files?')

    if not is_delete_files:
        return

    delete_positions = prompt_int_list('Enter file numbers to delete:', len(duplicated_files))

    delete_files(duplicated_files, delete_positions)


if __name__ == '__main__':
    main()
