import json
import write2JSON
import produce
import generic_objects
import cycle_connect
import generate
import innerLayer
import read_file
import initLSystem
import complexity 

import sys
import numpy as np
from timeit import default_timer as timer

if len(sys.argv) < 4:
    print("Usage: python main.py <file_path> <decorate_path> <export_path> <optional:matryoshka_path>")
    sys.exit(1)


file_path = sys.argv[1]
decorate_path = sys.argv[2]
generic_export_path = sys.argv[3]

count = 0

complexity_min = 3
complexity_max = 13
sample = 10
total_sample = (complexity_max - complexity_min) * sample
start_time = timer()

generic_visual_bridge_info,generic_object_list,global__object_list,extra_system_list = read_file.read_object_file(file_path)

for cur_complexity in range (complexity_min, complexity_max):

    cur_level = 0
    while True:
        if cur_level == sample:
            break

        visual_bridge_info = generic_visual_bridge_info
        visual_bridge_info['complexity'] = cur_complexity
        export_path = generic_export_path + str(count) + '.json' 

        #read the inputs
        result_list = []

        if visual_bridge_info is None:
            print("L-System backbone")
            result_list = initLSystem.initSystem(decorate_path)
        else:
            visual_bridge_info = complexity.calc_complexity(visual_bridge_info)
            class_generate = generate.generate_helper(generic_object_list, global__object_list, extra_system_list, visual_bridge_info, decorate_path)
            result_list = class_generate.smc_process()

        if len(result_list) == 0:
            print("failed")
            continue

        count += 1
        cur_level += 1

        if len(sys.argv) == 5:
            matryoshka_path = sys.argv[4]
            result_list += innerLayer.produce_innerLayer(matryoshka_path, decorate_path)

        used_time = round(timer() - start_time, 1)
        print("Finished:", count, "of total:", total_sample, "current complexity:", cur_complexity, "current level:", cur_level, "/", sample, "used:", used_time, "seconds")
        output_writer = write2JSON.output()
        output_writer.write_result(result_list, export_path)
