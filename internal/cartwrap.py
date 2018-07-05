import subprocess
import io
from threading import Thread
from queue import Queue
import re
import math
import gen2dict

def reader(pipe, pipe_name, queue):
    try:
        with pipe:
            for line in iter(pipe.readline, b''):
                queue.put((pipe_name, line))
    finally:
        queue.put(None)

def generate_cartogram(area_data, gen_file, cartogram_executable):

    cartogram_process = subprocess.Popen([
        cartogram_executable,
        '-g',
        gen_file,
        '-s'
    ],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=1)

    q = Queue()

    Thread(target=reader,args=[cartogram_process.stdout, "stdout", q]).start()
    Thread(target=reader,args=[cartogram_process.stderr, "stderr", q]).start()

    cartogram_process.stdin.write(str.encode(area_data))
    cartogram_process.stdin.close()

    for _ in range(2):
        for source, line in iter(q.get, None):
            yield source,line
    
    #output, errors = cartogram_process.communicate(bytes(area_data, 'UTF-8'))

    #return io.StringIO(output.decode())

def generate_cartogram_set(maps, cartogram_executable, default_color):

    maximum_progress = 95.0
    current_progress = 0.0
    main_average_density = 0.0

    map_number = 1

    for cart_map in maps:

        cartogram_gen = ""
        cartogram_json = {}

        cartogram_area = 0.0
        cartogram_average_density = 0.0

        initial_area_error = None
        one_region_cartogram = False

        yield "loading", {'loading_point': current_progress, 'stderr_line': 'Computing Map {} of {}'.format(map_number, len(maps))}

        for source, line in generate_cartogram(cart_map['area_data'], cart_map['gen_file'], cartogram_executable):

            if source == "stdout":
                map_gen += line
            else:
                s = re.search(r'max\. abs\. area error: (.+)', line.decode())

                if s != None:

                    if initial_area_error == None:
                        initial_area_error = float(s.groups(1)[0])
                        current_progress = (0 if map_number == 1 else maximum_progress / map_number) + (maximum_progress / len(maps)) * 0.2
                    else:
                        current_progress = (0 if map_number == 1 else maximum_progress / map_number) + (((initial_area_error - float(s.groups(1)[0]))/((initial_area_error-0.01)))*((maximum_progress / len(maps))))
                
                area_search = re.search(r'total cartogram area: (.+)', line.decode())

                if area_search != None:
                    cartogram_area = float(area_search.groups(1)[0])
                
                one_region_search = re.search(r'WARNING: There is only one region. The output cartogram will', line.decode())

                if one_region_search != None:
                    one_region_cartogram = True
                
                yield "loading", {'loading_point': current_progress, 'stderr_line': line.decode()}
        
        # Now we want to calculate the average density
        cartogram_average_density = sum([float(entry.split(' ')[1]) for entry in cart_map['area_data'].split('\n')]) / cartogram_area
        

        if map_number == 1:
            main_average_density = cartogram_average_density
        
        cartogram_json = gen2dict.translate(io.StringIO(cartogram_gen.decode()), default_color)

        # If we're not dealing with the main map (i.e., the first one) and we
        # only one region, then we need to do the scaling here.
        
        if map_number != 1 and one_region_cartogram:

            # In this case, cartogram_average_density is the same as the user-
            # supplied area for the one region in this map.

            scaling_factor = math.sqrt(cartogram_average_density / main_average_density)

            for feature in cartogram_json['features']:

                for pair in feature['coordinates']:

                    pair[0] *= scaling_factor
                    pair[1] *= scaling_factor
        
        yield "output", cartogram_json

        map_number += 1



        
        

                    






