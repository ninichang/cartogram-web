import subprocess
import io
from threading import Thread
from queue import Queue

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

