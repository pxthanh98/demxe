import argparse
import subprocess
import os
import os.path as osp
from os.path import isfile, join
import count

parser = argparse.ArgumentParser(description='Demo loading models.')
parser.add_argument('--model_dir', type=str, help='Model directory.')
parser.add_argument('--data_dir', type=str, help='Data directory.')
parser.add_argument('--time', type=str, help='Time stamp.')
args = parser.parse_args()

data_dir = "/data/FairMOT/"
conf_thres = 0.4

# 06:00 to 17:59 - am
# 18:00 to 05:59 - pm
def get_timestamp(time):
	if (int(time) >= 0):
		if int(time) < 1800 and int(time) >= 600:
			return "am"
		elif int(time) >= 0 and int(time) < 600:
			return "pm"
		elif int(time) >= 1800 and int(time) < 2400:
			return "pm"

def get_input(data_dir, time):
#    t = str(time)
    hour, minute = time[:len(time)//2], time[len(time)//2:]
    name = hour + ":" + minute
    video = minute + ".mp4"
    if (get_timestamp(time) == "am"):
        model = os.path.join(data_dir, "models/day_hrnet.pth")
#        model = os.path.join(data_dir, "models/mix_hrnet.pth")
        vid = os.path.join(data_dir, "data/videos", "am", hour, video)
        return vid, model, name

    elif (get_timestamp(time) == "pm"):
        model = os.path.join(data_dir, "models/night_hrnet.pth")
#        model = os.path.join(data_dir, "models/mix_hrnet.pth")
        vid = os.path.join(data_dir, "data/videos", "pm", hour, video)
        return vid, model, name

def demo():
    video, model, name = get_input(data_dir, args.time)
    output_dir = os.path.join(data_dir, "results")
    print("Processing video " + name)
    print("Loading model...")
    process = subprocess.run(['python', 'demo.py', 'mot', '--load_model', str(model), '--input-video', str(video), '--conf_thres', str(conf_thres), '--output-root', str(output_dir), '--output-format', 'text'])
    result = [name] + count.get_result()[0]   
    count.save_result([result])
    print("Saved counting result to src/count.csv")

if __name__ == "__main__":
    demo()
