import pickle
import os, sys
import random

ROOT = '../bin' # pick path to save data to
pre_filename = f'dummy_data_iter'

# -- generate data --
def gen_dummy_data(dummy_dict = {}, timestep = 0):

    data1 = [i for i in range(random.randint(0,100))]
    data2 = [i for i in range(random.randint(0,10))]
    dummy_dict[timestep] = {'data1':data1, 'data2':data2}

# -- save data -- 
def save_data (dummy_dict= {}, iter=0) :
    filename = pre_filename + f'{iter}.pkl'
    data_path = os.path.join(ROOT, filename)

    with open( data_path,'wb') as outfile :
        pickle.dump(dummy_dict, outfile )
    
# -- load data -- 
def load_data(path=ROOT) :
    file_list = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path,file)) and (pre_filename in file and 'pkl' in file) ]
    file_list.sort(key=lambda x: os.path.getmtime(x))

    consolidated_dict = {}
    loaded_times = []
    for filepath in file_list:        
        with open( filepath,'rb') as outfile :
            loaded_dummy_dict = pickle.load(outfile)
        
        # extract key (time) from chunk of time in dummy_dict
        loaded_times  = [ct for ct in loaded_dummy_dict]
        
        # merge into consolidation dictionary
        for ct in loaded_times:
            consolidated_dict[ct] = loaded_dummy_dict[ct]

    return consolidated_dict

# -- data generator and periodic storage --
def data_gen_save(MAX_TIME = 100, TIME_CHUNK=10) :
    
    # -- Time --
    dummy_dict = {}
    t_count = 0
    for t in range(0, MAX_TIME):
        gen_dummy_data (dummy_dict, timestep=t) 

        # save: chunks
        if ((t+1)%TIME_CHUNK == 0) :
            save_data(dummy_dict, iter=t_count)
            # reset the dict - so only the data generated in new chunk is stored 
            dummy_dict = {}
            t_count += 1

# --  -- 
if __name__ == "__main__":
    # Generate and save
    data_gen_save()

    # Reload the data:
    out_data = load_data()

    # Print the data: key values
    out = [t for t in out_data]
    print(out)


