from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import json
import time

import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D





# def setLoc(arm):
#     with open('coord.json', 'r') as openfile:
 
#         # Reading from json file
#         json_object = json.load(openfile)
 
#     dist_from_cam = json_object['dist']

#     center_pt = json_object['center']
    
#     dist_from_cam = 600 - dist_from_cam # Camera mounted at 600mm, inverses to dist above table

#     arm.ee = [center_pt[0], center_pt[1], dist_from_cam]

#     tinyik.visualize(arm)



# sched = BlockingScheduler()

# sched.add_job(lambda: setLoc(arm), 'interval', seconds=0.2)
# sched.start()


while True:
    with open('coord.json', 'r') as openfile:

        my_chain = Chain(name='left_arm', links=[
            OriginLink(),
            URDFLink(
            name="shoulder",
            origin_translation=[-10, 0, 5],
            origin_orientation=[0, 1.57, 0],
            rotation=[0, 1, 0],
            ),
            URDFLink(
            name="elbow",
            origin_translation=[25, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 1, 0],
            ),
            URDFLink(
            name="wrist",
            origin_translation=[22, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 1, 0],
            )
        ])

        ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
    
        # Reading from json file
        json_object = json.load(openfile)
    
        dist_from_cam = json_object['dist']

        center_pt = json_object['center']
        
        dist_from_cam = 600 - dist_from_cam # Camera mounted at 600mm, inverses to dist above table
        my_chain.plot(my_chain.inverse_kinematics([center_pt[0], center_pt[1], dist_from_cam]), ax)
        matplotlib.pyplot.show()
        matplotlib.pyplot.pause(.25)
        matplotlib.pyplot.close()
