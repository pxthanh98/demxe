python extract_frames.py -i may_10/ -m 10
#python extract_frames.py -i may_11/ -m 11
for dir in /data/FairMOT/data/src/images/train/*/img1
    do 
        cd "$dir";  
        ffmpeg -i video.mp4 %6d.jpg -hide_banner;
        rm video.mp4;
done
