import os, random, logging, getpass
from utils.decrypt_string import decrypt_string
# Get application base dir.
_basedir = os.path.abspath(os.path.dirname(__file__))
from utils.interactive import check_default, bool_input
from utils.log_setup import setup_experiment_logging

global_log_file_path = setup_experiment_logging()
start_process_id = ('').join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(6)])
prompt_suffix=': \n\n\t\t%s    \n\n (y/n): '

DEBUG = True 
RELOAD = True
SECRET_KEY = 'mysecretkeyvalue'


SECURITY_TRACKABLE = True
SECURITY_POST_LOGIN_VIEW = '/home'
SECURITY_CHANGEABLE = True
SECURITY_CHANGE_URL = '/change_password'
SECURITY_REGISTERABLE = True
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = 'astan_is_awesome_and_you_should_totally_use_it_and_cite'
SECURITY_RESET_URL = '/reset_password'
SECURITY_RECOVERABLE = True
SECURITY_EMAIL_SENDER = "*An"
SECURITY_CONFIRMABLE = bool_input('\n\nForce account confirmation?')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'astan.annotation.app'
MAIL_USERNAME = check_default(MAIL_USERNAME,
                         "Is this the username (omitting @domain) for the server's email account?"+prompt_suffix % MAIL_USERNAME,
                         lambda:True,
                         "Please enter alternative username: ")
MAIL_PASSWORD = getpass.getpass('Password for AstAn email account: ')
print('\n\n\n')

#####  Verify locations from where to fetch taskdefs and store resulting data
reject_prompt="Please enter alternative location: "

TASK_DESCS_URI = os.path.join(_basedir, 'tasks/descriptions')
TASK_DESCS_URI = check_default(TASK_DESCS_URI,
                         "Is this the root location of all the task definition files?"+prompt_suffix % TASK_DESCS_URI,
                         os.path.isdir,
                         reject_prompt)

USERMAPS = os.path.join(_basedir, 'tasks/usermaps')
USERMAPS = check_default(USERMAPS,
                         "Is this the root location of all the user->task mappings?"+prompt_suffix % USERMAPS,
                         os.path.isdir,
                         reject_prompt)


DATA_SOURCE_URIS = os.path.join(_basedir, 'tasks/data_source_uris.json')
DATA_SOURCE_URIS = check_default(DATA_SOURCE_URIS,
                         "Is this the root location of all the datasource URIs?"+prompt_suffix % DATA_SOURCE_URIS,
                         os.path.isdir,
                         reject_prompt)



DATA_SINK = os.path.join(_basedir, 'data')
DATA_SINK = check_default(DATA_SINK,
                         "Is this root location of the resulting annotations?"+prompt_suffix % DATA_SINK,
                         os.path.isdir,
                         reject_prompt)

SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(_basedir, 'db/app_dev.db')
SQLALCHEMY_DATABASE_URI = check_default(SQLALCHEMY_DATABASE_URI,
                         "Is this root location of the resulting annotations?"+prompt_suffix % SQLALCHEMY_DATABASE_URI,
                         os.path.isfile,
                         reject_prompt)

logging.info('%s Initializing with TASK_DESCS_URI: %s'%(start_process_id, TASK_DESCS_URI))
logging.info('%s Initializing with USERMAPS: %s'%(start_process_id, USERMAPS))
logging.info('%s Initializing with DATA_SOURCE_URIS: %s'%(start_process_id, DATA_SOURCE_URIS))
logging.info('%s Initializing with DATA_SINK: %s'%(start_process_id, DATA_SINK))
logging.info('%s Initializing with SQLALCHEMY_DATABASE_URI: %s'%(start_process_id, SQLALCHEMY_DATABASE_URI))




