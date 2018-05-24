import subprocess
import io

def generate_cartogram(area_data, gen_file, cartogram_executable):

    cartogram_process = subprocess.Popen([
        cartogram_executable,
        '-g',
        gen_file,
        '-s'
    ],stdin=subprocess.PIPE,stdout=subprocess.PIPE)

    output, errors = cartogram_process.communicate(bytes(area_data, 'UTF-8'))

    return io.StringIO(output.decode())

