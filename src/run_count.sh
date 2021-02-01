python index.py

# 06:00 to 18:00 - am
# 18:01 to 05:59 - pm

#for i in $(seq -w 0700 0759)
for i in $(seq 2200 2259)
do
	python vehicle_count.py --model_dir ../models/ --data_dir ../data/videos --time $i
done
