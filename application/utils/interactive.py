

def check_default(default, prompt, check_default, value_error_msg):
    res=default
    outer_cond=True
    while outer_cond:
        response = raw_input(prompt)
        if response.lower() not in ['y', 'n']:
                print("Not an appropriate choice.")
        else:
            if(response.lower()=='n'):
                while True:
                    response = input("Please enter alternative %s: "%input_entity)
                    if checking_handle(response):
                        print(value_error_msg)
                    else:
                        res = response
                        outer_cond=False
                        break
            else:
                outer_cond=False
    print('\n\n')
    return res