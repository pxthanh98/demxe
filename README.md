# **Đếm xe**
Project sử dụng kiến trúc mạng [FairMOT](https://github.com/ifzhang/FairMOT) với backbone HRNetv2 cho bài toán nhận diện xe cộ dựa trên dữ liệu video từ các camera giám sát, kết hợp với thuật toán xác định hướng di chuyển của từng vật thể. 


## 1. Yêu cầu
* Folder tree:
```
folder_name/
├── data
├── demos
├── exp
├── models
└── src
```
trong đó
```
data        Chứa tất cả các video
demos       Video demo sau khi inference
exp         Checkpoint của quá trình training
models      Pretrained models
src         Các script hỗ trợ
```

* Môi trường:
Sử dụng python 3.7 và pytorch >= 1.2.0, ffmpeg.
```
conda create -n FairMOT
conda activate FairMOT
conda install pytorch torchvision cudatoolkit -c pytorch
cd ${FAIRMOT_ROOT}
pip install -r requirements.txt
```

* Ngoài ra nếu sử dụng backbone [DCNv2](https://github.com/CharlesShang/DCNv2):
```
git clone https://github.com/CharlesShang/DCNv2
cd DCNv2
./make.sh
```

## 2. Chuẩn bị dữ liệu
* Bước 1: Trích xuất frame từ các video cần thiết, chia thành các folder như sau:
```
video_name/
├── gt
├── img1
└── seqinfo.ini
```
trong đó
```
gt            Folder chứa file text gán nhãn của video
img1          Folder chứa các frame định dạng .jpg
seqinfo.ini   File chứa các thông tin metadata của video.
```
ví dụ 1 file seqinfo.ini hoàn chỉnh (tham khảo `src/gen_seq.sh`)
```
[Sequence]
name=video_name
imgDir=img1
frameRate=30
seqLength=1202
imWidth=1280
imHeight=720
imExt=.jpg
```
Sau đó chuyển vào folder `train`
```
data/
└── demxe
   ├── images
   │   └── train
   └── labels_with_ids
       └── train
```
* Bước 2: Sinh nhãn tương ứng cho từng video với định dạng sau (mỗi giá trị là 1 cột):
```
Frame                Frame mà dữ liệu này biểu diễn. 
Object Id            Id của vật thế.
xmin                 Tọa độ x của điểm trái trên.
ymin                 Tọa độ y của điểm trái trên.
width                Chiều rộng của bounding box.
height               Chiều cao của bounding box.
Confidence Score     Mặc định bằng 1 cho task tracking.
-1
-1
-1
```
ví dụ đầy đủ cho 1 file định dạng đúng
```
1,1,755,211,22,31,1,-1,-1,-1
1,7,117,207,53,58,1,-1,-1,-1
2,1,754,211,22,31,1,-1,-1,-1
2,7,117,207,53,58,1,-1,-1,-1
```
* Bước 3: Chia file nhãn cho từng frame:
Sử dụng script `src/gen_labels.py` để sinh nhãn của từng frame trong mỗi video. Kết quả sẽ được lưu tại `data/demxe/labels_with_ids/train`.

## 2. Training
* Bước 1: Download các pretrained model cần thiết:
```
models/
├── day_hrnet.pth
├── night_hrnet.pth
├── mix_hrnet.pth
├── hrnetv2_w18_imagenet_pretrained.pth
└── hrnetv2_w32_imagenet_pretrained.pth
```
Link download: https://drive.google.com/drive/folders/1XFW5PQz2NevRo7jQCBlgmbN8YhRvNRTN?usp=sharing
trong đó
```
day_hrnet.pth       Training trên những video ban ngày (6:00am to 17:59pm)
night_hrnet.pth     Training trên những video buổi tối (18:00pm to 5:59am)
mix_hrnet.pth       Training trên những video trên cả 2 khung giờ
```

* Bước 2: Tạo file training:
Sử dụng script `scr/gen_dot_train.py`, thay `label_root=$HOME/data/demxe/labels_with_ids/train`. Kết quả cho ra file `demxe.train` chứa đường dẫn đến các frame tại `$HOME/src/data/`.

* Bước 3: Tạo file config đường dẫn đến dữ liệu training `src/lib/cfg/data.json`.
```
{
    "root":"${FAIRMOT_ROOT}",
    "train":
    {
        "demxe":"/data/FairMOT/src/data/demxe.train"
    }
}
```

* Bước 4: Training:
Sử dụng script `scr/all_hrnet.sh`.


## 3. Inference
* Tracking raw video:
```
cd src
python demo.py mot --load_model ../models/mix_hrnet.pth --input-video video_name --conf_thres 0.4
```
* Kết quả cho ra video tracking vật thể, folder chứa các frame và file text chứa bounding box.
* Trong trường hợp không muốn lưu video, có thể thêm option `--output-format text` ở cuối.


## 4. Evaluation
* Đánh giá dựa trên các độ đo MOTA, IDF1, IDS.
```
cd src
python track.py mot --test_demxe True --load_model mix_hrnet.pth --conf_thres 0.3
```
* Đếm hướng xe: Tham khảo script `src/vehicle_count.py` và `src/count.py`.

## Citation
```
@article{zhang2020fair,
  title={FairMOT: On the Fairness of Detection and Re-Identification in Multiple Object Tracking},
  author={Zhang, Yifu and Wang, Chunyu and Wang, Xinggang and Zeng, Wenjun and Liu, Wenyu},
  journal={arXiv preprint arXiv:2004.01888},
  year={2020}
}
```
