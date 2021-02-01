import os.path as osp
import os
from os.path import isfile, join

label_root = '/data/FairMOT/data/demxe/images/train'
seqs = [s for s in os.listdir(label_root)]
seqs = sorted(seqs)
result = []

def gen_dot():
	for seq in seqs:	
		images_root = join(label_root, seq, 'img1')
		labels_root = join(label_root, seq, 'gt', 'gt.txt')
#		label_files = [f for f in os.listdir(seq_label_root) if isfile(join(seq_label_root, f))]
#		images = [f.split('.')[0] for f in label_files]	
#		img_links = ["demxe/images/train/" + seq + "/img1" + "/" + f + ".jpg" for f in images]
#		result.append(sorted(img_links))
#	with open('/data/FairMOT/src/data/demxe.train', 'w') as f:
#		for i in result:
#			for j in i:	
#				if (os.path.isfile("/data/FairMOT/data/" + j)):
#					f.write(j + '\n')	
#		f.close()			
		with open(labels_root, 'r'):
			
gen_dot()
