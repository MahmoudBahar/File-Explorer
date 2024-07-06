import os, shutil

def copyfile(src, dst, len_buff, callback=None):
    len_buff = 64 * 1024 if os.path.getsize(src) < 50 * 1024 * 1024 else 1024 * 1024
    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            buffer = fsrc.read(len_buff)
            if callback:
                callback(len(buffer))
class FileExplorer:
    def __init__(self, path = 'C:\\'):
        self.current_path = path
        self.previous_path = []
        self.copy_path = ''
        self.copy_path_type = ''
        self.copy_file_directory = False
    def get_files(self):
        return os.listdir(self.current_path)
    '''********************************************************************************************************************'''
    def change_path(self, path):
        if os.path.exists(path):
            self.current_path = path
            self.previous_path.clear()
            return 0
        else:
            return -1
    '''********************************************************************************************************************'''
    def select_dir(self, file_name):
        self.current_path = os.path.join(self.current_path, file_name)
    '''********************************************************************************************************************'''
    def open_file(self, file_name):
        os.system('start ' + os.path.join(self.current_path, file_name))
    '''********************************************************************************************************************'''
    def go_back(self):
        if self.current_path in os.listdrives():
            return -1
        self.previous_path.append(self.current_path[self.current_path.rfind('\\')+1:])
        self.current_path = os.path.dirname(self.current_path)
    '''********************************************************************************************************************'''
    def go_forward(self):
        if len(self.previous_path) == 0:
            return -1
        self.current_path = os.path.join(self.current_path, self.previous_path.pop())
    '''********************************************************************************************************************'''
    def create_dir(self, dir_name):
        if os.path.exists(os.path.join(self.current_path, dir_name)):
            return -1
        else:
            os.mkdir(os.path.join(self.current_path, dir_name))
    '''********************************************************************************************************************'''
    def create_file(self, file_name):
        if os.path.exists(os.path.join(self.current_path, file_name)):
            return -1
        else:
            open(os.path.join(self.current_path, file_name), 'w').close()
    '''********************************************************************************************************************'''
    def delete_dir(self, dir_name):
        if os.path.exists(os.path.join(self.current_path, dir_name)):
            shutil.rmtree(os.path.join(self.current_path, dir_name))
        else:
            return -1
    '''********************************************************************************************************************'''
    def rename(self, old_name, new_name):
        if os.path.exists(os.path.join(self.current_path, old_name)):
            os.rename(os.path.join(self.current_path, old_name), os.path.join(self.current_path, new_name))
        else:
            return -1
    '''********************************************************************************************************************'''
    def directory_expander(self, additional_path = ''):
        list = os.listdir(os.path.join(self.current_path, additional_path))
        for i in range(len(list)):
            if len(self.get_file_type(list[i])) == 0:
                list += self.directory_expander(os.path.join(additional_path, list[i]))
            list[i] = os.path.join(self.current_path, additional_path, list[i])
        return list
    '''********************************************************************************************************************'''
    def search_file_dir(self, file_name):
        list = self.directory_expander()
        founded_pathes = []
        file_name = file_name.casefold()
        for path in list:
            if file_name in path[path.rfind('\\')+1:].casefold():
                founded_pathes.append(path)
        return founded_pathes
    '''********************************************************************************************************************'''
    def get_file_size(self, file_name):
        return os.path.getsize(os.path.join(self.current_path, file_name))
    '''********************************************************************************************************************'''
    def get_file_type(self, file_name):
        return os.path.splitext(os.path.join(self.current_path, file_name))[1]
    '''********************************************************************************************************************'''
    def get_file_owner(self, file_name):
        return os.stat(os.path.join(self.current_path, file_name)).st_uid
    '''********************************************************************************************************************'''
    def get_file_permissions(self, file_name):
        return os.stat(os.path.join(self.current_path, file_name)).st_mode
    '''********************************************************************************************************************'''
    def get_file_modification_time(self, file_name):
        return os.path.getmtime(os.path.join(self.current_path, file_name))
    '''********************************************************************************************************************'''
    def get_file_access_time(self, file_name):
        return os.path.getatime(os.path.join(self.current_path, file_name))
    '''********************************************************************************************************************'''
    def get_file_creation_time(self, file_name):
        return os.path.getctime(os.path.join(self.current_path, file_name))
    '''********************************************************************************************************************'''
    def delete_file(self, file_name):
        if os.path.exists(os.path.join(self.current_path, file_name)):
            os.remove(os.path.join(self.current_path, file_name))
        else:
            return -1
    '''********************************************************************************************************************'''
    def copy_file(self, source, destination):
        if os.path.exists(source) and not os.path.exists(destination):
            shutil.copyfile(source, destination)
        else:
            return -1
    '''********************************************************************************************************************'''
    def move_file(self, source, destination):
        if os.path.exists(source) and not os.path.exists(destination):
            shutil.move(source, destination, copy_function=shutil.copy2)
        else:
            return -1
    '''********************************************************************************************************************'''
    def copy_dir(self, source, destination):
        if os.path.exists(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            return -1
    '''********************************************************************************************************************'''
    def move_dir(self, source, destination):
        if os.path.exists(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
            shutil.rmtree(source)
        else:
            return -1
    '''********************************************************************************************************************'''
    def get_date_modified(self):
        return os.path.getmtime(self.current_path)
    '''********************************************************************************************************************'''
    def take_copy_path(self, name, type_of_copy, type_of_file):
        self.copy_path = os.path.join(self.current_path, name)
        self.copy_path_type = type_of_copy
        self.copy_file_directory = type_of_file
    '''********************************************************************************************************************'''
    def paste_file(self):
        if self.copy_file_directory:
            if self.copy_path_type == 'c':
                self.copy_dir(self.copy_path, os.path.join(self.current_path, self.copy_path[self.copy_path.rfind('\\')+1:]))
            else:
                self.move_dir(self.copy_path, os.path.join(self.current_path, self.copy_path[self.copy_path.rfind('\\')+1:]))                
        else:
            if self.copy_path_type == 'c':
                self.copy_file(self.copy_path, os.path.join(self.current_path, self.copy_path[self.copy_path.rfind('\\')+1:]))
            else:
                self.move_file(self.copy_path, os.path.join(self.current_path, self.copy_path[self.copy_path.rfind('\\')+1:]))
    '''********************************************************************************************************************'''
''''********************************************************************************************************************'''
def get_local_disks():
    return os.listdrives()
'''********************************************************************************************************************'''
def get_local_disk_size(disk):
    import win32api
    drive = disk
    free_bytes, total_bytes, _ = win32api.GetDiskFreeSpaceEx(drive)
    return ((total_bytes - free_bytes), free_bytes, total_bytes)