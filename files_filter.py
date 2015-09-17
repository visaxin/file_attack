
import os

def get_file_mb_size(f):
    return os.path.getsize(f) / (1024*1024.0)

def files_filter(files,
    f_type_in=['all'],
    f_type_not_in=['ini'],
    f_size_start=0,
    f_size_end=0):

    filted_files = []
    for f in files:
        #get file extension
        file_type = os.path.splitext(f)[1]
        if file_type in f_type_in and file_type not in f_type_not_in:
            if f_size == 0 or f_size_end == 0:
                filted_files.append(f)
            elif get_file_mb_size(f) > f_size_start \
                    or  get_file_mb_size < f_size_end:
                filted_files.append(f)
            elif get_file_mb_size(f) > f_size_start \
                and get_file_mb_size < f_size_end:
                filted_files.append(f)
    return filted_files
