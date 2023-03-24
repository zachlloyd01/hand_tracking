import cv2
import mediapipe as mp
import imutils
import math
import json

center_pt = None
dist_from_cam = None

cap = cv2.VideoCapture(0)

handSolution = mp.solutions.hands # Model of hands
hands = handSolution.Hands(max_num_hands=1) 
draw = mp.solutions.drawing_utils # Get landmark points put on display



def pr_image(img):
    '''
        A function that returns an object containing every landmark for each hand,
        after being processed into a B&W image to improve speed.
    '''
    im_grey = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return hands.process(im_grey)
    
def disp_marks(img, res):
    '''
        Function that modifies cv2 image input
        by drawing on each landmark using Medianp.pipe.
        Returns coordinate of center point under middle
        finger.
    '''

    pts = [[], []]
    if res.multi_hand_landmarks:
        for mark in res.multi_hand_landmarks:
            for id, lm in enumerate(mark.landmark):
                height, width, chans = img.shape
                scale_x, scale_y = int(lm.x * width), int(lm.y * height)
                
                if id == 5:
                    pts[0] = [scale_x, scale_y]

                elif id == 17:
                    pts[1] = [scale_x, scale_y]
            # draw.draw_landmarks(img, mark, handSolution.HAND_CONNECTIONS)

    return pts

def calc_len(pt1, pt2):
    '''
        A function that returns the length in np.pixels between two given points,
        which are given as [x, y]
    '''

    try:
        x_term = pt2[0] - pt1[0]
        x_term = math.pow(x_term, 2)

        y_term = pt2[1] - pt1[1]
        y_term = math.pow(y_term, 2)

        res = math.sqrt(x_term + y_term)

        return res
    except:
        return False
    

def calc_focal_len(hand_len, dist=5.78, irl_width=3.5):
    '''
        A function that gets the focal length 
        of my webcam, using the known width
        of my hand being 3.5 inches wide, 
        and the distance (using an iPhone 12 to approximate).

        I can then  use the ratio of that to the width in np.pixels, which
        gives F.
    '''
    F = (hand_len * dist) / irl_width
    return F

def calc_approx_dist(hand_len,focal_len=231, irl_width=3.5):
    '''
        A function that calculates the approximate width of my hand,
        given the real width, and the focal length
    '''
    try:
        D = (irl_width * (focal_len)) / hand_len
        return D
    except:
        return False
    
def calc_center(pt1, pt2):
    '''
        Function returns the center point
    '''
    try:
        return [int((pt1[0] + pt2[0]) / 2), int((pt1[1] + pt2[1]) / 2)]
    except:
        return False
    

def data_loop():
    while True:

        succ, image = cap.read()

        if not succ:
            continue

        image = imutils.resize(image, width=600, height=600)

        # image = cv2.flip(image, 1)
        res = pr_image(image)
        pts = disp_marks(image, res)

        hand_len = calc_len(pts[0], pts[1])

        global dist_from_cam

        global center_pt
        
        dist_from_cam = int(calc_approx_dist(hand_len=hand_len) * 25.4)
        
        center_pt = calc_center(pts[0], pts[1])

        # print(dist_from_cam)

        if center_pt and dist_from_cam > 0:

            dictionary = {
                "dist": dist_from_cam,
                "center": center_pt
            }

            json_object = json.dumps(dictionary, indent=4)
    
            # Writing to sample.json
            with open("coord.json", "w") as outfile:
                outfile.write(json_object)
        
        try:
            cv2.circle(image, (center_pt[0], center_pt[1]), 10, (255, 0, 0), -dist_from_cam)
            image = cv2.putText(image, f'({center_pt[0]}, {center_pt[1]}, {dist_from_cam})', (center_pt[0], center_pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0), 1, cv2.LINE_AA)
            
        except Exception as e:
            # print(e)
            pass

        cv2.imshow("View Tracking", image)

        


        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()

data_loop() 