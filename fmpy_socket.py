from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result, download_test_file
import numpy as np
import shutil
import keyboard

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

time = start_time

while True:
    if keyboard.is_pressed(72):
        forward = 0.1

    if keyboard.is_pressed(80):
        forward = 0

    if keyboard.is_pressed("left arrow"):
        left_right = -0.2
    
    if keyboard.is_pressed("right arrow"):
        left_right = 0.2

    fmu.setReal([input_gear], [1.0])
    fmu.setReal([input_accel], [forward])
    fmu.setReal([input_handle], [left_right])

    fmu.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)

    output_Vx_real = fmu.getReal([output_Vx])
    output_Vy_real = fmu.getReal([output_Vy])
    output_Wz_real = fmu.getReal([output_Wz])

    print(output_Vx_real, output_Vy_real, output_Wz_real)