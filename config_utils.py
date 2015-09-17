import ConfigParser
import os
def _read_config(f):

    if not os.path.exists(f):
        return "Not exist",True
    config = ConfigParser.RawConfigParser()

    config.read(f)
    is_first_time = config.getboolean('filesys','is_first_time')
    info = "Read from Cfg File"
    return (info, is_first_time)


def _init_config(f):
    config = ConfigParser.RawConfigParser()

    config.add_section('filesys')
    config.set('filesys','is_first_time','true')

    with open(f,'w') as cfg:
        config.write(cfg)
        cfg.close()
    return f

def _update_config(f, section, name, val):
    config = ConfigParser.RawConfigParser()

    config.read(f)

    if config.has_section(section):
        config.set(section, name, val)
    else:
        config.add_section(section)
        config.set(section, name, val)
    with open(f, 'w') as cfg:
        config.write(cfg)
        cfg.close()
