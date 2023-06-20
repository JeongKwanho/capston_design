from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result, download_test_file
import socket
import time
import fmpy
import pygame

def num_mapping(input, a, b, c, d):
    result = ((d-c)/(b-a))*(input-a)+c

    return(result)

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
pygame.init()

handle = 0
accel = 0
gear = 0.0
# car_break = 0

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
# input_break = vrs['Break']

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
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                handle = pygame.joystick.Joystick(0).get_axis(0)*10
                accel = pygame.joystick.Joystick(0).get_axis(1)
                # car_break = pygame.joystick.Joystick(0).get_axis(2)

                accel = num_mapping(accel, -1, 1, 1, 0)
                # car_break = num_mapping(car_break, -1, 1, 1, 0)

            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(13):
                    gear += 1.0

                    if gear > 7:
                        gear = 7.0

                if pygame.joystick.Joystick(0).get_button(12):
                    gear -= 1.0

                    if gear < 0:
                        gear = 0.0    

        fmu.setReal([input_gear], [gear])
        # fmu.setReal([input_break], [car_break])
        fmu.setReal([input_accel], [accel])
        fmu.setReal([input_handle], [handle])

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