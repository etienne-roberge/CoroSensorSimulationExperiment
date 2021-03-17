import pybullet as p
import pybulletX as px
import pybullet_data
import time

import simulateData


px.init()
p.resetDebugVisualizerCamera(cameraDistance=0.12, cameraYaw=90, cameraPitch=-45, cameraTargetPosition=[0, 0, 0])

p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
planeId = p.loadURDF("plane.urdf")

# Create and initialize DIGIT
digit_body = px.Body(urdf_path="objects/sensor.urdf", base_position=[0, 0, 0], base_orientation=[0.0, -0.707106, 0.0, 0.707106], use_fixed_base=True)

# Add object to pybullet and tacto simulator
obj = px.Body(urdf_path="objects/sphere_small.urdf", base_position=[0, 0, 0.02], global_scaling=0.15)

simulateData.startStreaming()

for i in range(30000):
    start = time.time()
    #p.stepSimulation()
    results = p.getContactPoints(digit_body.id, obj.id)
    for contact in results:
        posX = contact[5][0]
        posY = contact[5][1]
        #print("position: " + str(contact[5][0:2]) + " force= " + str(contact[9]))
        if 0.01518 > posX > -0.02 and 0.01 > posY > -0.012:
            #interpolate to real
            interX = 4.0 + (posX + 0.02) * ((20.0 - 4.0)/(0.01518 + 0.02))
            interY = 4.0 + (posY + 0.012) * ((36.0 - 4.0) / (0.01 + 0.012))
            #simulateData.getGlobalTaxelValuesFromSpecificPosition(contact[9], interX, interY)
    #print(time.time() - start)
            #print("inside boundary " + str(interX) + " " + str(interY))

    time.sleep(1.)


