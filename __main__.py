import File_Explorer as fe, CMD_Modifiers as cmd_mod, keyboard as kb, time, archiver as arch
from datetime import datetime

size_of_file_name = 20
max_windows_files_size = 20
shifted_by = 0

def simplify_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size/1024:.2f} KB"
    elif size < 1024**3:
        return f"{size/(1024**2):.2f} MB"
    elif size < 1024**4:
        return f"{size/(1024**3):.2f} GB"
    else:
        return f"{size/(1024**4):.2f} TB"
def print_local_disks(local_disks, selected_disk):
    print(f"Drive Letter    Used Space    Free Space    Total Space")
    for index, i in enumerate(local_disks, start=1):
        size = fe.get_local_disk_size(i)
        if index == selected_disk:
            print(f"\033[1;92;40m {i[0].center(12, ' ')}    {simplify_size(size[0]).center(10, ' ')}    {simplify_size(size[1]).center(10, ' ')}    {simplify_size(size[2]).center(11, ' ')}\033[0m")
        else:
            print(f"{i[0].center(12, ' ')}    {simplify_size(size[0]).center(10, ' ')}    {simplify_size(size[1]).center(10, ' ')}    {simplify_size(size[2]).center(11, ' ')}")
def update_printed_disks(local_disks, selected_disk, movement):
    size = fe.get_local_disk_size(local_disks[selected_disk-1])
    print(f"\033[{selected_disk + 3};1H\033[2K\033[1;92;40m {local_disks[selected_disk-1][0].center(12, ' ')}    {simplify_size(size[0]).center(10, ' ')}    {simplify_size(size[1]).center(10, ' ')}    {simplify_size(size[2]).center(11, ' ')}\033[0m")
    ''
    movement = (1 if movement == 'up' else -1)
    if (selected_disk + movement) == 0:
        selected_disk = len(local_disks)
    elif (selected_disk + movement) == len(local_disks) + 1:
        selected_disk = 1
    else:
        selected_disk += movement
    size = fe.get_local_disk_size(local_disks[selected_disk-1])
    print(f"\033[{selected_disk+3};1H\033[2K{local_disks[selected_disk-1][0].center(12, ' ')}    {simplify_size(size[0]).center(10, ' ')}    {simplify_size(size[1]).center(10, ' ')}    {simplify_size(size[2]).center(11, ' ')}")
def print_files(files_list, selected_file, explorer):
    print(f"{'Name'.center(size_of_file_name, ' ')}    {'Date Modified'.center(19, ' ')}    {'Type'.center(8,' ')}    {'Size'.center(10, ' ')}")
    for index, i in enumerate(files_list[shifted_by:], start=shifted_by+1):
            if index > max_windows_files_size:
                break
            date = explorer.get_file_modification_time(i) 
            date2 = datetime.fromtimestamp(date)
            date3 = date2.strftime('%Y-%m-%d %H:%M:%S')
            file_type = explorer.get_file_type(i)
            _index = i.rfind('.')
            temp = i
            if _index != -1 and _index != 0:
                temp = temp[:_index]
            temp = temp.ljust(size_of_file_name, ' ')
            if len(temp) > size_of_file_name:
                temp = temp[:size_of_file_name - 3] + "..."
            if index == selected_file:
                print(f"\033[1;92;40m {temp}    {date3}    {file_type[1:].center(8,' ') if len(file_type) != 0 else ' Folder '}    {simplify_size(explorer.get_file_size(i)).center(10, ' ')}\033[0m")
            else:
                print(f"{temp}    {date3}    {file_type[1:].center(8,' ') if len(file_type) != 0 else ' Folder '}    {simplify_size(explorer.get_file_size(i)).center(10, ' ')}")
    print(f"\n\033[1;93;40mTotal Files: {len(files_list)}\033[0m")
def update_printed_files(files_list, selected_file, explorer, movement):
    date = explorer.get_file_modification_time(files_list[selected_file-1]) 
    date2 = datetime.fromtimestamp(date)
    date3 = date2.strftime('%Y-%m-%d %H:%M:%S')
    file_type = explorer.get_file_type(files_list[selected_file-1])
    _index = files_list[selected_file-1].rfind('.')
    temp = files_list[selected_file-1]
    if _index != -1 and _index != 0:
        temp = temp[:_index]
    temp = temp.ljust(size_of_file_name, ' ')
    if len(temp) > size_of_file_name:
        temp = temp[:size_of_file_name - 3] + "..."
    print(f"\033[{selected_file+3-shifted_by};1H\033[2K\033[1;92;40m {temp}    {date3}    {file_type[1:].center(8,' ') if len(file_type) != 0 else ' Folder '}    {simplify_size(explorer.get_file_size(files_list[selected_file-1])).center(10, ' ')}\033[0m")
    movement = 1 if movement == 'up' else -1
    if (selected_file + movement) == 0:
        selected_file = len(files_list)
    elif (selected_file + movement) == len(files_list) + 1:
        selected_file = 1
    else:
        selected_file += movement
    date = explorer.get_file_modification_time(files_list[selected_file-1]) 
    date2 = datetime.fromtimestamp(date)
    date3 = date2.strftime('%Y-%m-%d %H:%M:%S')
    file_type = explorer.get_file_type(files_list[selected_file-1])
    _index = files_list[selected_file-1].rfind('.')
    temp = files_list[selected_file-1]
    if _index != -1 and _index != 0:
        temp = temp[:_index]
    temp = temp.ljust(size_of_file_name, ' ')
    if len(temp) > size_of_file_name:
        temp = temp[:size_of_file_name - 3] + "..."
    print(f"\033[{selected_file+3-shifted_by};1H\033[2K{temp}    {date3}    {file_type[1:].center(8,' ') if len(file_type) != 0 else ' Folder '}    {simplify_size(explorer.get_file_size(files_list[selected_file-1])).center(10, ' ')}\033[0m")
def shift_printed_files(files_list, selected_file, explorer, shift):
    global shifted_by
    if shift == 'up':
        if shifted_by == 0:
            shifted_by = max(len(files_list) - max_windows_files_size, 0)
        else:
            shifted_by -= 1
    else:
        if shifted_by == (len(files_list) - max_windows_files_size):
            shifted_by = 0
        else:
            shifted_by += 1
    for index, i in enumerate(files_list[shifted_by:], start=shifted_by+1):
        if index > max_windows_files_size+shifted_by:
            break
        date = explorer.get_file_modification_time(i) 
        date2 = datetime.fromtimestamp(date)
        date3 = date2.strftime('%Y-%m-%d %H:%M:%S')
        file_type = explorer.get_file_type(i)
        _index = i.rfind('.')
        temp = i
        if _index != -1 and _index != 0:
            temp = temp[:_index]
        temp = temp.ljust(size_of_file_name, ' ')
        if len(temp) > size_of_file_name:
            temp = temp[:size_of_file_name - 3] + "..."
        if index == selected_file:
            print(f"\033[{index-shifted_by+3};1H\033[2K\033[1;92;40m {temp}    {date3}    {file_type[1:].center(8,' ') if len(file_type) != 0 else ' Folder '}    {simplify_size(explorer.get_file_size(i)).center(10, ' ')}\033[0m")
        else:
            print(f"\033[{index-shifted_by+3};1H\033[2K{temp}    {date3}    {file_type[1:].center(8,' ') if len(file_type) != 0 else ' Folder '}    {simplify_size(explorer.get_file_size(i)).center(10, ' ')}")
def print_help_menu():
    print('''up - Select the previous file
down - Select the next file
left - Go back
right - Go forward
enter - Open file or enter directory
delete - Delete file or directory
c - Copy file or directory
x - Cut file or directory
v - Paste file or directory
m - More options
r - Refresh
    ''')
def sub_menu(explorer, selected_file, directory):
    options_list=['Get File Owner',
                    'Get File Permissions',
                    'Get File Access Time',
                    'Get File Creation Time',
                    'Search For a File/Directory',
                    'Create Directory',
                    'Create File',
                    'Compress File/Directory',
                    'Decompress File/Directory',
                    'Rename',
                    'Change Local Disk',
                    'Change Current Path',
                    'Change File/Directory displayed Name Size',
                    'Change File/Directory Window Displayed Size']
    selected_option=1
    pressed_key = 'a'
    empty = False
    if len(explorer.get_files()) == 0:
        empty = True
        del options_list[:5]
        del options_list[2:5]
    if not empty:
        if explorer.get_files()[selected_file-1][explorer.get_files()[selected_file-1].rfind('.'):] == '.zip':
            archived = True
            del options_list[7]
        else:
            archived = False
            del options_list[8]
    cmd_mod.clear_screen()
    print(f"File Explorer\t\tCurrent Directory: {explorer.current_path + '' if empty else '\\' + explorer.get_files()[selected_file-1]}")
    print('Select the option you want to preform: ')
    for index, i in enumerate(options_list, start=1):
        if index == selected_option:
            print(f"\033[1;92;40m {i}\033[0m")
        else:
            print(f"{i}")
    while pressed_key not in ('left', 'enter'):
        pressed_key = kb.read_key()
        time.sleep(0.2)
        if pressed_key == 'up':
            if selected_option == 1:
                selected_option = len(options_list)
            else:
                selected_option -= 1
            temp = selected_option
            print(f"\033[{temp+2};1H\033[2K\033[1;92;40m {options_list[temp-1]}\033[0m\033[13;1H")
            if (temp + 1) == len(options_list) + 1:
                temp = 1
            else:
                temp += 1
            print(f"\033[{temp+2};1H\033[2K{options_list[temp-1]}\033[0m\033[13;1H")
        elif pressed_key == 'down':
            if selected_option == len(options_list):
                selected_option = 1
            else:
                selected_option += 1
            temp = selected_option
            print(f"\033[{temp+2};1H\033[2K\033[1;92;40m {options_list[temp-1]}\033[0m\033[13;1H")
            if (temp - 1) == 0:
                temp = len(options_list)
            else:
                temp -= 1
            print(f"\033[{temp+2};1H\033[2K{options_list[temp-1]}\033[0m\033[13;1H")
    cmd_mod.flush_input()
    if pressed_key == 'left':
        return selected_file
    if empty:
        if selected_option < 3:
            selected_option += 5
        else:
            selected_option += 7
    if selected_option == 1:
        print(f"\033[1;93;40m\033[17;1H\033[2KFile Owner: {explorer.get_file_owner(explorer.get_files()[selected_file-1])}\033[0m")
        temp = kb.read_key()
        while kb.is_pressed(temp):
            pass
    elif selected_option == 2:
        print(f"\033[1;93;40m\033[17;1H\033[2KFile Permissions: {explorer.get_file_permissions(explorer.get_files()[selected_file-1])}\033[0m")
        temp = kb.read_key()
        while kb.is_pressed(temp):
            pass
    elif selected_option == 3:
        date = explorer.get_file_access_time(explorer.get_files()[selected_file-1])
        date2 = datetime.fromtimestamp(date)
        date3 = date2.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\033[1;93;40m\033[17;1H\033[2KFile Access Time: {date3}\033[0m")
        temp = kb.read_key()
        while kb.is_pressed(temp):
            pass
    elif selected_option == 4:
        date = explorer.get_file_creation_time(explorer.get_files()[selected_file-1])
        date2 = datetime.fromtimestamp(date)
        date3 = date2.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\033[1;93;40m\033[17;1H\033[2KFile Creation Time: {date3}\033[0m")
        temp = kb.read_key()
        while kb.is_pressed(temp):
            pass
    elif selected_option == 5:
        cmd_mod.Show_cursor()
        search_name = input("\033[1;32;40m\033[17;1H\033[2KEnter the name of the file or directory you want to search for: \033[0m")
        cmd_mod.Hide_cursor()
        while kb.is_pressed('enter'):
            pass
        searcher = explorer.search_file_dir(search_name)
        if searcher:
            print(f"\033[1;93;40m\033[17;1H\033[2KFile(s)/Directory(ies) Found at:\033[0m")
            for index, path in enumerate(searcher, start=1):
                print(f"\033[1;93;40m\033[{17+index};1H\033[2K{' '*32}{index} - {path}\033[0m")
        else:
            print("\033[1;91;40m\033[17;1H\033[2KFile/Directory not found\033[0m")
        cmd_mod.flush_input()
        temp = kb.read_key()
        while kb.is_pressed(temp):
            pass
    elif selected_option == 6:
        cmd_mod.Show_cursor()
        dir_name = input("\033[1;32;40m\033[17;1H\033[2KEnter the name of the directory you want to create: \033[0m")
        cmd_mod.Hide_cursor()
        explorer.create_dir(dir_name)
        while kb.is_pressed('enter'):
            pass
    elif selected_option == 7:
        cmd_mod.Show_cursor()
        file_name = input("\033[1;32;40m\033[17;1H\033[2KEnter the name of the file you want to create: \033[0m")
        cmd_mod.Hide_cursor()
        explorer.create_file(file_name)
        while kb.is_pressed('enter'):
            pass
    elif selected_option == 8:
        temp = explorer.get_files()[selected_file-1]
        if archived:
            arch.decompressor(explorer.current_path + '\\' + temp, explorer.current_path + '\\' + temp.replace('.zip', ''))
        else:    
            cmd_mod.Show_cursor()
            archive_name = input("\033[1;32;40m\033[17;1H\033[2KEnter the name of the archive: \033[0m")
            cmd_mod.Hide_cursor()
            arch.compressor(explorer.current_path + '\\' + archive_name, explorer.current_path + '\\' + temp, directory)
        while kb.is_pressed('enter'):
            pass
    elif selected_option == 9:
        cmd_mod.Show_cursor()
        new_name = input("\033[1;32;40m\033[17;1H\033[2KEnter the new name of the file or directory: \033[0m")
        cmd_mod.Hide_cursor()
        explorer.rename(explorer.get_files()[selected_file-1], new_name)
        while kb.is_pressed('enter'):
            pass
    elif selected_option == 10:
        cmd_mod.clear_screen()
        local_disks = fe.get_local_disks()
        input_index = 1
        pressed_key = 'left'
        print("File Explorer")
        print("Select a Local disk to explore:")
        print_local_disks(local_disks, input_index)
        while pressed_key not in ('enter', 'esc'):
            if pressed_key == 'h':
                cmd_mod.clear_screen()
                print("File Explorer")
                print('''up - select the previous disk\ndown - select the next disk\nenter - select the disk''')
                temp = kb.read_key()
                while kb.is_pressed(temp):
                    pass
                input_index = 1
                cmd_mod.clear_screen()
                print("File Explorer")
                print("Select a Local disk to explore:")
                print_local_disks(local_disks, input_index)
            pressed_key = kb.read_key()
            time.sleep(0.2)
            if pressed_key == 'up':
                if input_index == 1:
                    input_index = len(local_disks)  
                else:
                    input_index -= 1
                update_printed_disks(local_disks, input_index, 'up')
            elif pressed_key == 'down':
                if input_index == len(local_disks):
                    input_index = 1
                else:
                    input_index += 1
                update_printed_disks(local_disks, input_index, 'down')
        if pressed_key == 'esc':
            return selected_file
        explorer.change_path(local_disks[input_index-1])
        return 1
    elif selected_option == 11:
        cmd_mod.Show_cursor()
        new_path = input("\033[1;32;40m\033[17;1H\033[2KEnter the new path: \033[0m")
        cmd_mod.Hide_cursor()
        while kb.is_pressed('enter'):
            pass
        if explorer.change_path(new_path):
            print(f"\033[1;91;40m\033[18;1H\033[2K{' '*19}Path not found\033[0m")
            temp = kb.read_key()
            while kb.is_pressed(temp):
                pass
    elif selected_option == 12:
        cmd_mod.Show_cursor()
        size = int(input("\033[1;32;40m\033[17;1H\033[2KEnter the new size of the file/directory displayed name: \033[0m"))
        while size > 100:
            size = int(input("\033[1;91;40m\033[18;1H\033[2KPlease enter size not more than 100: \033[0m"))
        cmd_mod.Hide_cursor()
        global size_of_file_name
        size_of_file_name = size
        while kb.is_pressed('enter'):
            pass
    elif selected_option == 13:
        cmd_mod.Show_cursor()
        size = int(input("\033[1;32;40m\033[17;1H\033[2KEnter the new size of the displayed files window: \033[0m"))
        while size > 35:
            size = int(input("\033[1;91;40m\033[18;1H\033[2KPlease enter size not more than 35: \033[0m"))
        cmd_mod.Hide_cursor()
        global max_windows_files_size
        max_windows_files_size = size
        while kb.is_pressed('enter'):
            pass
    return selected_file
def main():
    global shifted_by
    cmd_mod.Hide_cursor()
    cmd_mod.clear_screen()
    local_disks = fe.get_local_disks()
    input_index = 1
    pressed_key = 'left'
    print("File Explorer")
    print("Select a Local disk to explore:")
    print_local_disks(local_disks, input_index)
    while pressed_key not in ('enter', 'esc'):
        if pressed_key == 'h':
            cmd_mod.clear_screen()
            print("File Explorer")
            print('''up - select the previous disk\ndown - select the next disk\nenter - select the disk''')
            temp = kb.read_key()
            while kb.is_pressed(temp):
                pass
            input_index = 1
            cmd_mod.clear_screen()
            print("File Explorer")
            print("Select a Local disk to explore:")
            print_local_disks(local_disks, input_index)
        pressed_key = kb.read_key()
        time.sleep(0.2)
        if pressed_key == 'up':
            if input_index == 1:
                input_index = len(local_disks)  
            else:
                input_index -= 1
            update_printed_disks(local_disks, input_index, 'up')
        elif pressed_key == 'down':
            if input_index == len(local_disks):
                input_index = 1
            else:
                input_index += 1
            update_printed_disks(local_disks, input_index, 'down')
    if pressed_key == 'esc':
        return
    explorer = fe.FileExplorer(local_disks[input_index-1])
    pressed_key = 'left'
    cmd_mod.flush_input()
    selected_file = 1
    directory = False
    files_list = explorer.get_files()
    refresh = True
    window_counter = 1
    while pressed_key != 'esc':
        if len(files_list) != 0:
                directory = len(explorer.get_file_type(files_list[selected_file-1])) == 0
        if pressed_key == 'up':
            if selected_file == 1:
                selected_file = len(files_list)
            else:
                selected_file -= 1
            if selected_file == len(files_list) and len(files_list) > max_windows_files_size and window_counter == 1:
                shift_printed_files(files_list, selected_file, explorer, 'up')
                window_counter = max_windows_files_size
            elif window_counter == 1 and len(files_list) > max_windows_files_size:
                shift_printed_files(files_list, selected_file, explorer, 'up')
            else:
                window_counter -= 1
                update_printed_files(files_list, selected_file, explorer, 'up')
        elif pressed_key == 'down':
            if selected_file == len(files_list):
                selected_file = 1
            else:
                selected_file += 1
            if selected_file == 1 and len(files_list) > max_windows_files_size and window_counter == max_windows_files_size:
                shift_printed_files(files_list, selected_file, explorer, 'down')
                window_counter = 1
            elif window_counter == max_windows_files_size and len(files_list) > max_windows_files_size:
                shift_printed_files(files_list, selected_file, explorer, 'down')
            else:
                window_counter += 1
                update_printed_files(files_list, selected_file, explorer, 'down')
        elif pressed_key == 'left':
            selected_file = window_counter = 1
            explorer.go_back()
            refresh = True
            shifted_by = 0
        elif pressed_key == 'right':
            selected_file = window_counter = 1
            explorer.go_forward()
            refresh = True
            shifted_by = 0
        elif pressed_key == 'enter':
            if directory:
                explorer.select_dir(files_list[selected_file-1])
                selected_file = window_counter = 1
                shifted_by = 0
                refresh = True
            else:
                explorer.open_file(files_list[selected_file-1])
        elif pressed_key == 'delete':
            if len(files_list) == 0:
                selected_file = 1
            else:
                if directory:
                    explorer.delete_dir(files_list[selected_file-1])
                else:
                    explorer.delete_file(files_list[selected_file-1])
                if selected_file == len(files_list):
                    selected_file -= 1
                refresh = True
        elif pressed_key == 'c':
            explorer.take_copy_path(files_list[selected_file-1], 'c', directory)
        elif pressed_key == 'x':
            explorer.take_copy_path(files_list[selected_file-1], 'x', directory)
        elif pressed_key == 'v':
            explorer.paste_file()
            refresh = True
        elif pressed_key == 'm':
            selected_file = sub_menu(explorer, selected_file, directory)
            if selected_file == 1:
                window_counter = 1
                shifted_by = 0
            refresh = True
        elif pressed_key == 'r':
            refresh = True
            selected_file = window_counter = 1
        elif pressed_key == 'h':
            refresh = True
            selected_file = window_counter = 1
            shifted_by = 0
        if refresh:
            cmd_mod.clear_screen()
            if pressed_key == 'h':
                print(f"File Explorer\t\tCurrent Directory: {explorer.current_path}", end='')
                print_help_menu()
                temp = kb.read_key()
                while kb.is_pressed(temp):
                    pass
                cmd_mod.clear_screen()
            print(f"File Explorer\t\tCurrent Directory: {explorer.current_path}        press h for help")
            print('Select File Or Directory: ')
            files_list = explorer.get_files()
            if len(files_list) == 0:
                print("\n\033[1;91;40mNo files or directories found\033[0m")
            else:
                print_files(files_list, selected_file, explorer)
            refresh = False
        pressed_key = kb.read_key(suppress=True)
        time.sleep(0.2)



if __name__ == '__main__':
    main()