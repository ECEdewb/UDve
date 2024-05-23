import os, sys, getopt
import pickle, json
from demo_structs import Demo_session
from common_structs import Executor


demo_command_path = 'demo_config.cfg'

command_baud_rate = 115200
data_baud_rate = 921600
max_buffer_size = 2**30 #1 Gigabyte

#Get CLI arguments
opts, _ =  getopt.getopt(sys.argv[1:], "", ["command_port=", "data_port=", "duration=" ,
                                            "visualizer_data_loc=", "pickle_data_loc="
                                            "indent_json"])
opts = {item[0].replace("--", ""):item[1] for item in opts}

if "visualizer_data_loc" in opts:
    with open(opts["visualizer_data_loc"], "rb") as f:
        bin_str = f.read()
    with open("tmp_raw.pickle", "wb") as f:
        pickle.dump(bin_str, f)

executor_args = {
                    "command_port":opts["command_port"],
                    "data_port":opts["data_port"],
                    "command_baud_rate":command_baud_rate,
                    "data_baud_rate":data_baud_rate,
                    "commands":None,
                    "session_class":Demo_session
                }

executor = Executor(**executor_args)
executor.load_raw_data("tmp_raw.pickle")
executor.parse()
executor.set_dir("../data/Demo", timestamp_subdir=True)
executor.save_parsed_data()