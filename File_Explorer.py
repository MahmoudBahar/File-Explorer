import os, shutil, win32api, json

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
    def organizer(self):
        fileCategories = {}
        try:
            with open("File_Categories.json", mode="r") as file:
                fileCategories = json.load(file)
        except:
            fileCategories = {
                "Documents": {"Text Documents" : [".txt", ".doc", ".docx", ".pdf", ".rtf", ".odt", ".md", ".wps"], 
                            "Spreadsheet Documents" : [".xls", ".xlsx", ".csv", ".ods", ".tsv"],
                            "Presentation Documents" : [".ppt", ".pptx", ".odp"],
                            "E-Books": [".epub", ".mobi", ".azw"],
                            "Web Documents": [".html", ".htm", ".xhtml", ".xml", ".json"],
                            "Other": [".tex", ".log", ".msg", ".pages"]},
                
                "Images": {"Raster Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".ico"],
                        "Vector Images": [".svg", ".ai", ".eps", ".ps"],
                        "3D and Specialized Images": [".psd", ".xcf", ".cr2", ".nef", ".raw", ".arw", ".dng", ".orf", ".heif", ".heic"],
                        "Other": [".dds", ".jp2", ".jxr", ".hdr", ".exr", ".apng", ".tga"]},
                "Videos": ['.mp4', '.flv', '.avi', '.hevc', '.vob', '.webm', '.mov', '.mpeg', '.3gp', '.swf', '.mkv', '.h265', '.asf', '.rm', '.prores', '.mpg', '.ogv', '.ts', '.dvr-ms', '.avs', '.3dm'],
                "Music": ['.mp3', '.aac', '.flac', '.wma', '.aif', '.aiff', '.mod', '.wv', '.s3m', '.it', '.mpc', '.kar', '.pcm', '.spx', '.opus', '.dts', '.midi', '.ogg', '.ts', '.mp3', '.tak', '.ra', '.alac', '.xm', '.wav'],
                "Compressed": ['.zip', '.gzip', '.bz2', '.7z', '.tar.gz', '.tar.bz2', '.tar.xz', '.rar', '.iso', '.rpm', '.lzma', '.zpaq', '.lz', '.z', '.arj', '.tar', '.cpio', '.war', '.tar.Z', '.uue', '.sit', '.dmg', '.ace', '.jar'],
                "Code": ['.tcl', '.js', '.sql', '.scala', '.tcl', '.hbs', '.ps1', '.cobol', '.bash', '.scala', '.rpy', '.hlsl', '.dart', '.cu', '.go', '.f90', '.py', '.m', '.css', '.c', '.pl', '.hbs', '.pl', '.java', '.h', '.sh', '.zig', '.yaml', '.psm1', '.r', '.swift', '.md', '.cpp', '.vue', '.sass', '.lua', '.v', '.f95', '.perl', '.vhd', '.obj', '.elixir', '.scss', '.yaml', '.tex', '.ruby', '.vhdl', '.java', '.hpp', '.ipynb'],
                "Programs": {"Windows": [".exe", ".bat", ".cmd", ".msi", ".ps1", ".vbs", ".com", ".wsf"], 
                            "Mac": [".app", ".command", ".dmg", ".pkg"],
                            "Linux": [".bin", ".sh", ".run", ".deb", ".rpm"],
                            "Android": [".apk"]},
                "Other": []
            }
            with open("File_Categories.json", mode="w") as file:
                json.dump(fileCategories, file, indent = 4)

        path = self.current_path

        def getFileType(extension):
            for key in fileCategories.keys():
                if isinstance(fileCategories[key], dict):
                    for subKey in fileCategories[key].keys():
                        if extension.lower() in fileCategories[key][subKey]:
                            return (key, subKey)
                else:
                    if extension.lower() in fileCategories[key]:
                        return (key, None)
            fileCategories["Other"].append(extension)
            with open("File_Categories.json", mode="w") as file:
                json.dump(fileCategories, file, indent = 4)
            return ("Other", None)

        for file in os.listdir(path):
            if os.path.isdir(os.path.join(path, file)):
                continue
            fileType = getFileType(os.path.splitext(file)[-1])
            destinationPath = ""
            sourcePath = os.path.join(path, file)
            if fileType[1] != None:
                destinationPath = os.path.join(path, fileType[0], fileType[1])
                if not os.path.exists(destinationPath):
                    os.makedirs(destinationPath)
            else:
                destinationPath = os.path.join(path, fileType[0])
                if not os.path.exists(destinationPath):
                    os.makedirs(destinationPath)
            print(sourcePath, destinationPath)
            self.move_file(sourcePath, os.path.join(destinationPath, file))
''''********************************************************************************************************************'''
def get_local_disks():
    return os.listdrives()
'''********************************************************************************************************************'''
def get_local_disk_size(disk):
    drive = disk
    free_bytes, total_bytes, _ = win32api.GetDiskFreeSpaceEx(drive)
    return ((total_bytes - free_bytes), free_bytes, total_bytes)
