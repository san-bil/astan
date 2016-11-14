import errno, os, inspect

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    return path

def touch(file_path):
    open(file_path, 'a').close()

def to_unix_path(path):
    return path.replace('\\', '/')

def create_increment_folder( folder_prefix, parent_folder ):
    
    parent_folder = to_unix_path(parent_folder);
    folders = [name for name in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, name))]
    matching_folders_numbers = [];
    
    for i in range(0,len(folders)):
        folder_name = folders[i];
        contains_pattern =  folder_prefix in folder_name
    
        if(contains_pattern):
            split_result = int(folder_name.replace(folder_prefix,''));
            matching_folders_numbers.append(split_result);
                    
    
                    
    matching_folders_numbers = sorted(matching_folders_numbers);
    
    if( matching_folders_numbers ):
        highest_folder = matching_folders_numbers[-1];
    else:
        highest_folder = 0;
    
    new_folder_idx=highest_folder+1;
    new_folder_path = os.path.join(parent_folder,folder_prefix+str(new_folder_idx));
    
    mkdir_p(new_folder_path);
    return (new_folder_path,new_folder_idx)

def create_increment_file( file_prefix, parent_folder,ext='',dont_touch=True):
    mkdir_p(parent_folder)
    parent_folder = to_unix_path(parent_folder)
    files = [name for name in os.listdir(parent_folder) if os.path.isfile(os.path.join(parent_folder, name))]
    matching_files_numbers = [];
    matching_files = []
    for filename in files:
        filestem=os.path.splitext(filename)[0]
            
        contains_pattern =  file_prefix in filestem
    
        if(contains_pattern):
            try:
                split_result = int(filestem.replace(file_prefix,''));
            except Exception as err:
                split_result = 0
            matching_files_numbers.append(split_result);
            matching_files.append(filename)


    matching_files_numbers = sorted(matching_files_numbers);
    if ext=='':
        ext=os.path.splitext(matching_files[0])[-1]

    if( matching_files_numbers ):
        highest_file = matching_files_numbers[-1]
    else:
        highest_file = 0

    new_file_idx=highest_file+1;
    new_file_path = os.path.join(parent_folder,file_prefix+str(new_file_idx)+'.'+ext)
    if(not dont_touch):
        touch(new_file_path)
    return (new_file_path,new_file_idx)

def get_python_func_tempdir():
    mycaller=inspect.getouterframes(inspect.currentframe(), 2)[1][3]

    out = os.path.join('/tmp','python_'+mycaller)
    mkdir_p(out)
    tmpdir = create_increment_folder(get_simple_date(), out); 
    return (out, tmpdir)
    
    
    
