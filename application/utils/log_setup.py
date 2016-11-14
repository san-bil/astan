import os, logging
from interactive import check_default

def setup_experiment_logging():
    default_log_path = '/var/log/astan'
    default_log_path = check_default(default_log_path, 'Is this location ok for the main logs: \n\n\t\t%s  \n\n (y/n): ' % default_log_path, os.path.isdir, 'Please enter alternative location')
    os.system('mkdir -p '+default_log_path)
   
    global_log_file_path=os.path.join(default_log_path,'astan.log')
    logging.basicConfig(filename=global_log_file_path,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    return global_log_file_path