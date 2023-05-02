#this is to fix pickling issues


import pickle 



def check_gallery_count():
    loaded_dict_array = load_dict_array()
    return(len(loaded_dict_array))

def load_dict_array():

    try:
        with open('gallery.txt', 'rb') as f:
            loaded_dict_array = pickle.load(f)


    except:
        loaded_dict_array = []
    return loaded_dict_array


def load_dict_array_fix():
    try:
        with open('gallery.txt', 'rb') as f:
            loaded_dict_array = pickle.load(f)
            # Decode bytes to strings
            for item in loaded_dict_array:
                for key in item:
                    if isinstance(item[key], bytes):
                        item[key] = item[key].decode()
            save_dict(loaded_dict_array)
    except:
        loaded_dict_array = []
    
    
    return loaded_dict_array

    
def save_dict(current_dict_array):
    with open('gallery_fixed.txt', 'wb') as f:
        pickle.dump(current_dict_array, f)


print(load_dict_array())

print("--------")

print(load_dict_array_fix())