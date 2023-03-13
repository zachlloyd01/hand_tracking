import tinyik
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
import json

arm = tinyik.Actuator(['z', [1., 0., 0.], 'z', [1., 0., 0.]])


def setLoc(arm):
    with open('coord.json', 'r') as openfile:
 
        # Reading from json file
        json_object = json.load(openfile)
 
    dist_from_cam = json_object['dist']

    center_pt = json_object['center']
    
    dist_from_cam = 600 - dist_from_cam # Camera mounted at 600mm, inverses to dist above table

    arm.ee = [center_pt[0], center_pt[1], dist_from_cam]

    tinyik.visualize(arm)



sched = BlockingScheduler()

sched.add_job(lambda: setLoc(arm), 'interval', seconds=0.2)
sched.start()