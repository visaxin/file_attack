import ConfigParser
import os
class Config(object):
    def __init__(self,f):
        self.f = f

        self.is_first_time = True
        self.f_type_in = []
        self.f_type_not_in = []
        self.f_size_start = 0
        self.f_size_end = 0

    def _read_config(self):
        if not os.path.exists(self.f):
            return "Cfg Not exist",True
        config = ConfigParser.RawConfigParser()

        config.read(self.f)
        self.is_first_time = config.getboolean('filesys','is_first_time')
        self.f_type_in = config.get('filesfilter','f_type_in').split(',')
        self.f_type_not_in = config.get('filesfilter','f_type_not_in').split(',')
        self.f_size_start = config.get('filesfilter','f_size_start')
        self.f_size_end = config.get('filesfilter','f_size_end')

        info = "Read from Cfg File"
        return (info,
                self.is_first_time,
                self.f_type_in,
                self.f_type_not_in,
                self.f_size_start,
                self.f_size_end)
    def _read_files_filter(self):
        if not os.path.exists(self.f):
            return
        config = ConfigParser.RawConfigParser()

        config.read(self.f)
        #self.is_first_time = config.getboolean('filesys','is_first_time')
        self.f_type_in = config.get('filesfilter','f_type_in').split(',')
        self.f_type_not_in = config.get('filesfilter','f_type_not_in').split(',')
        self.f_size_start = config.get('filesfilter','f_size_start')
        self.f_size_end = config.get('filesfilter','f_size_end')

        info = "Read Filter Condition from Cfg File"
        return (info,
                self.f_type_in,
                self.f_type_not_in,
                self.f_size_start,
                self.f_size_end)

    def _init_config(self):
        config = ConfigParser.RawConfigParser()

        help_msg = ''' 'Please insert file type you want to monitor.
            If you want to .exe file only, you can add "exe".
            Add more using "," to split.
            The same as file type not in.
            By default, all files will be monitored.'
        '''

        config.add_section('filesys')
        config.set('filesys','is_first_time','true')
        config.add_section('filesfilter')
        config.set('filesfilter','f_type_in',help_msg)
        config.set('filesfilter','f_type_not_in',help_msg)
        config.set('filesfilter','f_size_start',0)
        config.set('filesfilter','f_size_end',0)

        with open(self.f,'wb') as cfg:
            config.write(cfg)
            cfg.close()
        return self.f

    def _update_config(self, section, name, val):
        config = ConfigParser.RawConfigParser()

        config.read(self.f)

        if config.has_section(section):
            config.set(section, name, val)
        else:
            config.add_section(section)
            config.set(section, name, val)
        with open(f, 'w') as cfg:
            config.write(cfg)
            cfg.close()


if __name__ == '__main__':
    s = Config(os.getcwd()+"/config_test.cfg")
    s._init_config()
    info,is_first_time,f_type_in,f_type_not_in,f_size_start,f_size_end= s._read_config()
    print f_type_in
