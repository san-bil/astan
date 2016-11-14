

def check_default(default, prompt, checking_handle, value_error_msg):
    res=default
    outer_cond=True
    while outer_cond:
        response = raw_input(prompt+" ")
        if response.lower() not in ['y', 'n']:
                print("Not an appropriate choice.")
        else:
            if(response.lower()=='n'):
                while True:
                    response = input("Please enter alternative %s: "%input_entity)
                    if not checking_handle(response):
                        print(value_error_msg)
                    else:
                        res = response
                        outer_cond=False
                        break
            else:
                outer_cond=False
    print('\n\n')
    return res

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1", "y")

def bool_input(prompt):
    valid_responses=("yes", "true", "t", "1", "y","no", "false", "f", "0", "n",)
    checking_handle=lambda v: v.lower() in valid_responses
    return valid_input(prompt + ' (y/n): ', checking_handle, "Invalid response!")


def valid_input(prompt, checking_handle, value_error_msg):
    while True:
        response = raw_input(prompt)
        if not checking_handle(response):
            print(value_error_msg)
            print('\n\n')
        else:
            res = response
            print('\n\n')
            break
    return res
