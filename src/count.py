import cv2
from scipy.spatial import distance
from itertools import groupby
from operator import itemgetter
import argparse
import math
import csv

#parser = argparse.ArgumentParser(description='Counting algorithm.')
#parser.add_argument('--i', type=str, help='Input gt files.')
#parser.add_argument('--o', type=str, help='Output files.')
#args = parser.parse_args()

right = (1200, 500)
left = (150, 200)
up = (900, 180)
down = (100, 500)
#video = 'test.mp4'
#labels = args.i
#video = '/data/FairMOT/results/result.mp4'
labels = '/data/FairMOT/results/results.txt' 

def sort_dict(d):
    res = {}
    for dict in d:
        for list in dict:
            if list in res:
                res[list] += (dict[list])
            else:
                res[list] = dict[list]
    return res

def get_objects(gt):
    f = open(gt, "r")
    lines = f.readlines()
    lines = [line.strip().split(",") for line in lines]
    frames, ids = [], []
    for line in lines:
        for col in line:
#            frame = int(line[0])
#            _id = int(line[1])
#            xmin = int(line[2])
#            ymin = int(line[3])
#            width = int(line[4])
#            height = int(line[5])
            frame = math.floor(float(line[0]))
            _id = math.floor(float(line[1]))
            xmin = math.floor(float(line[2]))
            ymin = math.floor(float(line[3]))
            width = math.floor(float(line[4]))
            height = math.floor(float(line[5]))
        frames.append({frame: [(xmin + width//2, ymin + height//2)]})
        ids.append({_id: [(frame, (xmin + width//2, ymin + height//2))]})
    frames = sort_dict(frames)
    ids = sort_dict(ids)
    return frames, ids

def draw_center(frame, points):
    for ptn in points:
        frame = cv2.circle(frame, ptn, radius=0, color=(0,0,255), thickness=10)
    return frame

def fixed_dir(frame):
    frame = cv2.circle(frame, right, radius=0, color=(0,255,0), thickness=20)
    frame = cv2.putText(frame, "Right", tuple(map(sum,zip(right,(0,-5)))), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    frame = cv2.circle(frame, up, radius=0, color=(0,255,0), thickness=20)
    frame = cv2.putText(frame, "Up", tuple(map(sum,zip(up,(0,-5)))), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    frame = cv2.circle(frame, left, radius=0, color=(0,255,0), thickness=20)
    frame = cv2.putText(frame, "Left", tuple(map(sum,zip(left,(0,-5)))), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    frame = cv2.circle(frame, down, radius=0, color=(0,255,0), thickness=20)
    frame = cv2.putText(frame, "Bottom", tuple(map(sum,zip(down,(0,-5)))), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    return frame

def nearest_point(ptn, x, y, z, t):
    d1 = distance.euclidean(ptn, x)
    d2 = distance.euclidean(ptn, y)
    d3 = distance.euclidean(ptn, z)
    d4 = distance.euclidean(ptn, t)
    _min = min(d1, d2, d3, d4)
    if (_min == d1):
        return x
    elif (_min == d2):
        return y
    elif (_min == d3):
        return z
    elif (_min == d4):
        return t

def check_dir(first, last):
    if (first == left and last == right):
        return 1
    elif (first == left and last == up):
        return 2
    elif (first == left and last == down):
        return 3
    elif (first == right and last == left):
        return 4
    elif (first == right and last == up):
        return 5
    elif (first == right and last == down):
        return 6
    elif (first == up and last == down):
        return 7
    elif (first == up and last == left):
        return 8
    elif (first == up and last == right):
        return 9
    elif (first == down and last == up):
        return 10
    elif (first == down and last == left):
        return 11
    elif (first == down and last == right):
        return 12
    else:
        return 0

#def group_direction(direction_list):
#    result = {}
#    for x, y in direction_list: 
#        if y in result: 
#            result[y].append((x)) 
#        else: 
#            result[y] = [(x)] 
#    return result

def track_dir(ids):
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c0 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    num_objects = len(ids.items())
    result = []
    for key, value in ids.items():
        first_frame = ids[key][0][0]
        last_frame = ids[key][-1][0]
        first_ptn = nearest_point(ids[key][0][1], right, up, left, down)
        last_ptn = nearest_point(ids[key][-1][1], right, up, left, down)

        if (check_dir(first_ptn, last_ptn) == 1):
            c1 += 1
        elif (check_dir(first_ptn, last_ptn) == 2):
            c2 += 1
        elif (check_dir(first_ptn, last_ptn) == 3):
            c3 += 1
        elif (check_dir(first_ptn, last_ptn) == 4):
            c4 += 1
        elif (check_dir(first_ptn, last_ptn) == 5):
            c5 += 1
        elif (check_dir(first_ptn, last_ptn) == 6):
            c6 += 1
        elif (check_dir(first_ptn, last_ptn) == 7):
            c7 += 1
        elif (check_dir(first_ptn, last_ptn) == 8):
            c8 += 1
        elif (check_dir(first_ptn, last_ptn) == 9):
            c9 += 1
        elif (check_dir(first_ptn, last_ptn) == 10):
            c10 += 1
        elif (check_dir(first_ptn, last_ptn) == 11):
            c11 += 1
        elif (check_dir(first_ptn, last_ptn) == 12):
            c12 += 1
        else:
            c0 += 1

    result.append([num_objects, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c0])
    return result
#    save_result(result)

def save_result(result):
    with open('count.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(result)
        file.close()

def write_index():
    index = [["Video", "Số vật thể", "Hướng 1", "Hướng 2", "Hướng 3", "Hướng 4", "Hướng 5", "Hướng 6", "Hướng 7", "Hướng 8", "Hướng 9", "Hướng 10", "Hướng 11", "Hướng 12", "Không xác định" ]]
    with open('count.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(index)
        file.close()

def display(vid):
    vid = cv2.VideoCapture(vid)
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    frames, ids = get_objects(labels)
    track_dir(ids)
    count = 1
#    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1280, 720), 1)
    while (vid.isOpened()):
        ret, frame = vid.read()
        fixed_dir(frame)
        for key, value in frames.items():
            if (count == key):
                draw_center(frame, frames[key])
#        out.write(frame)
        count += 1
        cv2.imshow('frame', frame)
        cv2.moveWindow('frame', 300, 50)
        if (cv2.waitKey(1000//fps) & 0xff == ord('q')):
            break
    vid.release()
    out.release()
    cv2.destroyAllWindows()

#def get_result(vid):
#    vid = cv2.VideoCapture(vid)
def get_result():
    frames, ids = get_objects(labels)
    return track_dir(ids)

#if __name__ == '__main__':
##    display(video)
#	get_result()
