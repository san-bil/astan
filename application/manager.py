from application import app, db, usermaps, task_defs
from flask import render_template, redirect, request
from application.models import *
from flask.ext.security import login_required
import flask_security.core, flask.ext.login
import os, json, datetime, shutil
from utils.file_system import create_increment_file

@app.route('/')
@app.route('/index/')
def index():
    user = flask.ext.login.current_user
    if user.is_authenticated():
        return redirect("/home", code=302)
    else:
        return render_template('info/landing.html', title='Flask-Bootstrap')


@app.route('/home')
@login_required
def home():
    user = flask.ext.login.current_user
    tasks = get_user_tasks(user)
    relevant_task_defs = find_relevant_tasks(tasks)
    print user.email + " : /home"
    return render_template('info/home.html', title='*An', tasks=relevant_task_defs, username=user.email)


@app.route('/annotator/<task_name>')
@login_required
def annotator(task_name):
    tmp = find_relevant_tasks_helper(task_name)
    task_def = tmp[0]
    task_details = task_def['task_details']
    task_type = task_details['type']

    task_to_template_map = {"segmentation":"evan.html", "continuous_annotation":"conan.html"}
    user = flask.ext.login.current_user
    print user.email + " : /annotator/"+task_name

    template_name = task_to_template_map[task_type]
    user = flask.ext.login.current_user
    username = user.email
    return render_template(template_name, task_def=task_def, username=username)











@app.route('/fetch_json_annos')
@login_required
def fetch_json_annos():
    subj = request.args.get('subject')
    videoname = request.args.get('video')
    task_name = request.args.get('task_name')
    annos_obj = read_json_annos(subj, videoname, task_name)

    user = flask.ext.login.current_user
    print user.email + " : /fetch_json_annos : "+task_name+", "+videoname

    return annos_obj
 
def read_json_annos(subj, videoname, task_name):
    data_sink = app.config['DATA_SINK']
    subj_results_dir = os.path.join(data_sink,task_name,subj)
    ensure_dir(subj_results_dir)
    results_file_name = os.path.join(subj_results_dir,videoname+".json")
    if os.path.isfile(results_file_name):
        with open (results_file_name) as tmpfile:
            annos_obj=json.loads(tmpfile.read())
            if not annos_obj.get("annos"):
                annos_obj["annos"]=[]
    else:
        annos_obj = {"video": videoname, "annos":[]}
    return json.dumps(annos_obj)


@app.route('/push_json_annos', methods=['POST'])
@login_required
def push_json_annos():
    subj = request.args.get('subject')
    task_name = request.args.get('task_name')
    my_buffer = request.get_json()
    videoname = my_buffer['video']

    user = flask.ext.login.current_user
    print user.email + " : /fetch_json_annos : "+task_name+", "+videoname

    write_json_annos(subj, videoname, task_name, my_buffer)
    return "Done"


def write_json_annos(subj, videoname, task_name, obj):
    data_sink = app.config['DATA_SINK']
    subj_results_dir = os.path.join(data_sink, task_name, subj)
    ensure_dir(subj_results_dir)
    results_file_name = os.path.join(subj_results_dir,videoname+".json")
    with open(results_file_name, 'w') as outfile:
        json.dump(obj, outfile)


conan_csv_order=['clienttime',
                 'subject',
                 'video',
                 'dimension',
                 'time',
                 'value',
                 'playing',
                 'interval_id',
                 'isdeleted']

@app.route('/push_csv_annos', methods=['POST'])
@login_required
def push_csv_annos():
    subj = request.args.get('subject')
    task_name = request.args.get('task_name')
    chunk = ""
    tmp=request.get_json();
    for obj in tmp["buffer"]:
        obj['isdeleted']=False
        formattedDate = datetime.datetime.now().strftime("\"%A, %B %d, %Y, %I:%M:%S %p\"")
        chunk += formattedDate + ',' + ','.join([ str(obj[k]) for k in conan_csv_order]) + "\n"
        videoname=obj['video']
        dimension=obj['dimension']
    write_csv_chunk(subj,videoname,dimension, task_name, chunk)

    user = flask.ext.login.current_user
    print user.email + " : /push_csv_annos : "+task_name+", "+videoname

    return "success"

def write_csv_chunk(subj, videoname, dimension, task_name, csv):
    data_sink = app.config['DATA_SINK']
    subj_results_dir = os.path.join(data_sink,task_name, subj)
    ensure_dir(subj_results_dir)

    results_file_name = os.path.join(subj_results_dir,videoname + '-' + dimension + ".csv")
    with open(results_file_name, 'a') as outfile:
        outfile.write(csv)

    outfile.close()

@app.route('/del_csv_annos', methods=['POST'])
@login_required
def del_csv_annos():
    subj = request.args.get('subject')
    videoname = request.args.get('video')
    task_name = request.args.get('task_name')
    dimension = request.args.get('dimension')
    json_data = request.get_json()
    print(json_data)
    interval_id = json_data['interval_id']
    filter_handle = lambda csvl: csvl['interval_id']==interval_id and csvl['dimension']==dimension

    filter_csv(subj, videoname, dimension, task_name,filter_handle)

    user = flask.ext.login.current_user
    print user.email + " : /del_csv_annos : "+task_name+", "+videoname
    return "success"

import csv
conan_csv_fieldnames=['server_receive_time',
                     'clienttime',
                     'subject',
                     'video',
                     'dimension',
                     'time',
                     'value',
                     'playing',
                     'interval_id',
                     'isdeleted']

def filter_csv(subj, videoname, dimension, task_name, filter_handle):
    data_sink = app.config['DATA_SINK']
    subj_results_dir = os.path.join(data_sink,task_name, subj)
    ensure_dir(subj_results_dir)

    results_file_name = os.path.join(subj_results_dir,videoname + '-' + dimension + ".csv")
    tmp_results_file_name = os.path.join(subj_results_dir,videoname + '-' + dimension + ".csv.tmp")

    with open(results_file_name,'r') as infile:
        with open(tmp_results_file_name, 'w') as outfile:

            csv_lines_in = csv.DictReader(infile,fieldnames=conan_csv_fieldnames)
            csv_lines_out = csv.DictWriter(outfile, fieldnames=conan_csv_fieldnames)
            csv_lines_out.writeheader()

            for csvl in csv_lines_in:
                csvl_filtered=csvl
                if(filter_handle(csvl)):
                    csvl_filtered['isdeleted']='True'

                csv_lines_out.writerow(csvl_filtered)
    results_file_name_bak = create_increment_file(os.path.basename(results_file_name), 
                              os.path.dirname(results_file_name), 
                              ext='bak',
                              dont_touch=True)[0]
    shutil.move(results_file_name, results_file_name_bak)
    shutil.move(tmp_results_file_name, results_file_name)
    


@app.route('/fetch_csv_annos', methods=['POST','GET'])
@login_required
def fetch_csv_annos():
    subj = request.args.get('subject')
    task_name = request.args.get('task_name')
    videoname = request.args.get('video')
    dimension = request.args.get('dimension')
    try:
        csv_annos = json.dumps(read_csv(subj, videoname, dimension, task_name))
    except Exception as err:
        csv_annos = json.dumps([])
    user = flask.ext.login.current_user
    print user.email + " : /fetch_csv_annos : "+task_name+", "+videoname

    return csv_annos

import csv
def read_csv(subj, videoname, dimension, task_name):
    data_sink = app.config['DATA_SINK']
    subj_results_dir = os.path.join(data_sink,task_name, subj)
    ensure_dir(subj_results_dir)

    results_file_name = os.path.join(subj_results_dir,videoname + '-' + dimension + ".csv")
    conan_csv_order_trunc=[el for el in conan_csv_order if el not in ['clienttime','subject','server_receive_time']]

    with open(results_file_name,'r') as infile:
        csv_lines = csv.DictReader(infile,fieldnames=conan_csv_fieldnames)
        json_dict_list=[]
        for csvl in csv_lines:
            tmp_dict={i:csvl[i] for i in conan_csv_order_trunc}
            if(tmp_dict['playing']=='True' and tmp_dict['isdeleted']=='False'):
                json_dict_list.append(tmp_dict)

    return json_dict_list



def get_user_tasks(user):
    for usermap in usermaps:
 #       print usermap["email"]
        task_list = usermap["tasks"]
 #       print task_list
        if usermap["email"] == user.email:
            if task_list is None:
                return []
            else:
                return task_list
    return []
    
def find_relevant_tasks_helper(task_name):
    tmp_task_objs = [ t for t in task_defs if t["task_name"] == task_name ]
    return tmp_task_objs

def find_relevant_tasks(task_list):
    task_objs = []
    for task_name in task_list:
        tmp_task_objs = find_relevant_tasks_helper(task_name)
        task_objs += tmp_task_objs
    return task_objs

def ensure_dir(f):
#    d = os.path.dirname(f)
    if not os.path.exists(f):
        os.makedirs(f)



# 404 page not found "route"
@app.errorhandler(404)
def not_found(error):
    title = "404 Page not found"
    return render_template('404.html', title=title), 404


# 500 server error "route"
@app.errorhandler(500)
def server_error(error):
    title = "500 Server Error"
    db.session.rollback()
    return render_template('500.html', title=title), 500
