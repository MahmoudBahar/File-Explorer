import shutil, os
def compressor(archive_name, source, directory):
    if directory:
        os.mkdir(os.path.join(source, archive_name))
        shutil.copytree(source, os.path.join(source, archive_name), dirs_exist_ok=True)
        shutil.make_archive(archive_name, 'zip', root_dir=os.path.join(source, archive_name))
        shutil.rmtree(os.path.join(source, archive_name))
    else:
        os.mkdir(os.path.join(source, archive_name))
        shutil.copy2(source, os.path.join(source, archive_name))
        shutil.make_archive(archive_name, 'zip', root_dir=os.path.join(source, archive_name))
        shutil.rmtree(os.path.join(source, archive_name))

def decompressor(archive_name, destination):
    shutil.unpack_archive(archive_name, destination, 'zip')