import torch
import torch.nn as nn
import cv2
import numpy as np
from torchvision import transforms
from PIL import Image
from os import listdir
from os.path import isfile, join
import pickle

class Identity(nn.Module):
    def __init__(self):
        super(Identity, self).__init__()
            
    def forward(self, x):
        return x

model = torch.hub.load('pytorch/vision:v0.8.2', 'inception_v3', pretrained=True)
model.dropout = Identity()
model.fc = Identity()

device = torch.device("cuda")
model.to(device)

model.eval()
preprocess = transforms.Compose([
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def forward(image_array):
    with torch.no_grad():
        output = model(image_array)
    return output

def FrameCapture(path):
    cap = cv2.VideoCapture(path)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
    pil_array = []
    fc = 0
    ret = True
    while (fc < frameCount  and ret):
        ret, image = cap.read()
        buf[fc] = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_array.append(Image.fromarray(image))
        fc += 1

    cap.release()
    return pil_array

def preprocess_for_inception(input_video):
    batch_list = []
    for frame in input_video:
        input_tensor = preprocess(frame)
        batch_list.append(input_tensor.unsqueeze(0))

    return torch.cat(batch_list)

def extract_embedding_inception(path):
    pill_array = FrameCapture(path)
    whole_video_tensor = preprocess_for_inception(pill_array)
    count_of_frames = len(whole_video_tensor)
    batch_size = 100
    batch_count = count_of_frames // batch_size
    embedding = []
    for i in range(batch_count + 1):
        batch = whole_video_tensor[i*batch_size: min((i+1)*batch_size, count_of_frames)]
        if batch.shape[0] == 0:
            continue
        batch = torch.FloatTensor(batch).to(device)
        embedding.append(forward(batch).detach().cpu())

    final_embedding_tensor = torch.cat(embedding)
    return final_embedding_tensor

root_of_raw_videos = '../extractedbdhandspeakskeletons/cropped_videos'
root_of_video_embeddings = '../extractedbdhandspeakskeletons/video_embeddings_cropped'
raw_video_name_list = [f for f in listdir(root_of_raw_videos) if isfile(join(root_of_raw_videos, f))]

for single_video_path in raw_video_name_list:
    print(f"extracting {single_video_path}")
    if isfile(f"{root_of_video_embeddings}/{single_video_path}.pickle"):
        print(f"skipping video {single_video_path}")
        continue
    embeddings = extract_embedding_inception(root_of_raw_videos+'/'+single_video_path)
    filehandler = open(f"{root_of_video_embeddings}/{single_video_path}.pickle","wb")
    pickle.dump(embeddings, filehandler)
    filehandler.close()
