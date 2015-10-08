
import os
def get_file_mb_size(f):
    return os.path.getsize(f) / (1024*1024.0)
class FileFilter(object):

    def __init__(self,files,cfg):
        self.files_to_filter = files
        self.cfg = cfg

    def filter(self):
        self.cfg._read_files_filter()
        info, f_type_in, f_type_not_in, f_size_start, f_size_end = self.cfg._read_files_filter()

        filted_files = []

        for f in self.files_to_filter:
            #get file extension
            if os.path.exists(f):
                file_type = os.path.splitext(f)[1]
                file_type = file_type.replace('.','')

                if file_type not in f_type_not_in or file_type in f_type_in and file_type:
                    if f_size_start == 0 or f_size_end == 0:
                        filted_files.append(f)
                    elif get_file_mb_size(f) > f_size_start \
                            or  get_file_mb_size < f_size_end:
                        filted_files.append(f)
                    elif get_file_mb_size(f) > f_size_start \
                        and get_file_mb_size < f_size_end:
                        filted_files.append(f)
        return filted_files

if __name__ == '__main__':
    from config_utils import Config

    files = ['2015-09-28 10-03-26.log','test.txt']

    f = FileFilter(files,Config("config_test.cfg"))
    print f.filter()
