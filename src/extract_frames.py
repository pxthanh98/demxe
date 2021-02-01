import argparse
import subprocess
import os
import os.path as osp
from os.path import isfile, join
import shutil

parser = argparse.ArgumentParser(description='Extract frame in Vatic tool format.')
parser.add_argument('-i', type=str, help='Video directory.')
parser.add_argument('-o', type=str, help='Frame directory.')
parser.add_argument('-m', type=str, help='Which machine.')

args = parser.parse_args()

def mkdirs(d):
    if not osp.exists(d):
        os.makedirs(d)

def create_output_dir(videos):
    # Change 'frame' to args.frame
    frame_dir = [join('images', 'train', args.m + '_' + seq + '_' + f.split('.')[0], 'img1') for f in videos]
    gt_dir = [join('images', 'train', args.m + '_' + seq + '_' + f.split('.')[0], 'gt') for f in videos]
    for d in frame_dir:
        mkdirs(d)
    for g in gt_dir:
        mkdirs(g)

def copy_videos(videos):
    curr_vid = [join(seq_root, seq, f) for f in videos]
    # Change 'frame' to args.frame
#    frame_dst = [join('images', 'train', args.m + '_' + seq + '_' + f.split('.')[0]) for f in videos]
    dst_vid = [join('images', 'train', args.m + '_' + seq +  '_' + f.split('.')[0], 'img1', 'video.mp4') for f in videos]
    for i, vid in enumerate(curr_vid):
        shutil.copy2(curr_vid[i], dst_vid[i])

seq_root = args.i
seqs = sorted([s for s in os.listdir(seq_root)])
for seq in seqs:
    videos_dir = join(seq_root, seq)
    videos = [f for f in os.listdir(videos_dir)]
    create_output_dir(videos)
    copy_videos(videos)
