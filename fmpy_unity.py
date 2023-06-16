from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result, download_test_file
import socket
import keyboard
import time
import fmpy

fmu_file = 'All_simulation.fmu'
start_time = 0
threshold = 2.0
step_size = 1e-3
forward = 0
left_right = 0

model_description = read_model_description(fmu_file)

vrs = {}

for variable in model_description.modelVariables:
    vrs[variable.name] = variable.valueReference

input_gear = vrs['gear']
input_handle = vrs['handle']
input_accel = vrs['accel']
output_Vx = vrs['body.Vx']
output_Vy = vrs['body.Vy']
output_Wz = vrs['body.Wz']

unzipdir = extract(fmu_file)

fmu = FMU2Slave(guid = model_description.guid, unzipDirectory = unzipdir, modelIdentifier=model_description.coSimulation.modelIdentifier, instanceName='instance1')

fmu.instantiate()
fmu.setupExperiment(startTime = start_time)
fmu.enterInitializationMode()
fmu.exitInitializationMode()

host, port = "127.0.0.1", 25001
data_arr = [0, 0, 0]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((host, port))

    while True:
        if keyboard.is_pressed(72):
            forward = 0.1

        if keyboard.is_pressed(80):
            forward = 0

        if keyboard.is_pressed("left arrow"):
            left_right += -1
            time.sleep(1)
        
        if keyboard.is_pressed("right arrow"):
            left_right += 1
            time.sleep(1)

        fmu.setReal([input_gear], [1.0])
        fmu.setReal([input_accel], [forward])
        fmu.setReal([input_handle], [left_right])

        fmu.doStep(currentCommunicationPoint=start_time, communicationStepSize=step_size)

        data_arr[0] = fmu.getReal([output_Vx])[0]
        data_arr[1] = fmu.getReal([output_Vy])[0]
        data_arr[2] = fmu.getReal([output_Wz])[0]

        data = "".join(str(data_arr))
        data = data.strip('[')
        data = data.strip(']')

        sock.sendall(data.encode("utf-8"))
        response = sock.recv(1024).decode("utf-8")

        print(response)

finally:
    sock.close()