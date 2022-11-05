from os import listdir
from os.path import isfile, join
import json
import re
from sklearn.model_selection import train_test_split
import pickle
import torch
import gzip
import random

irrelevant_const = "IRRELEVANT"

sign_subtitle_json_file_root = "../extractedbdhandspeakskeletons/skeleton_subtitle_jsons"

onlyfiles = [f for f in listdir(sign_subtitle_json_file_root) if isfile(join(sign_subtitle_json_file_root, f))]

def generate_sequence_id(line):
    p = re.compile('[a-zA-Z0-9\-]')
    return "".join(p.findall(line))


final_array = []

keys_of_skeleton = []
properties_of_consideration = [{
    'name': 'pose_keypoints_2d', 'count': 25
}, {
    'name': 'face_keypoints_2d', 'count': 70
}, {
    'name': 'hand_left_keypoints_2d', 'count': 21
}, {
    'name': 'hand_right_keypoints_2d', 'count': 21
}]

total_body_keypoint_count = 0
for property in properties_of_consideration:
    property_name = "_".join(property['name'].split('_')[:-2])
    for i in range(property['count']):
        keys_of_skeleton.append(f"{ property_name }_{i}_x")
        keys_of_skeleton.append(f"{ property_name }_{i}_y")

for json_file_name in onlyfiles:
    print(json_file_name)
    json_file_object = open(f"{sign_subtitle_json_file_root}/{json_file_name}", encoding='utf-8')
  
    json_dict = json.load(json_file_object)
    
    for single_sentence_data in json_dict['skeleton_data']:
        sequence_id = generate_sequence_id(f"{json_dict['video_name']}-{single_sentence_data['english']}-{single_sentence_data['start_time']}-{single_sentence_data['end_time']}")
        
        sign_array_of_single_sentence = []

        skeletons_of_single_sentence = single_sentence_data['skeletons']

        for single_skeleton in skeletons_of_single_sentence:
            single_skeleton_numbers = []
            for key_of_skeleton in keys_of_skeleton:
                single_skeleton_numbers.append(single_skeleton[key_of_skeleton])
            sign_array_of_single_sentence.append(single_skeleton_numbers)

        final_array.append({
            "name": sequence_id,
            "signer": irrelevant_const,
            "gloss": irrelevant_const,
            "sign": torch.Tensor(sign_array_of_single_sentence),
            "text": single_sentence_data['bengali']
        })

    json_file_object.close()

random.shuffle(final_array)

train_set, not_train_set = train_test_split(final_array, test_size=0.1, random_state=42)
test_set, validation_set = train_test_split(not_train_set, test_size=0.5, random_state=42)

train_array_pickle_handler = gzip.open("data_for_stochastic/phoenix14t.pami0.train","wb")
validation_array_pickle_handler = gzip.open("data_for_stochastic/phoenix14t.pami0.dev","wb")
test_array_pickle_handler = gzip.open("data_for_stochastic/phoenix14t.pami0.test","wb")

pickle.dump(train_set, train_array_pickle_handler)
pickle.dump(test_set, test_array_pickle_handler)
pickle.dump(validation_set, validation_array_pickle_handler)

train_array_pickle_handler.close()
validation_array_pickle_handler.close()
test_array_pickle_handler.close()

# sample_from_train = train_set[0]

# sample_dict = {
#     'name': sample_from_train['name'],
#     'signer': sample_from_train['signer'],
#     'gloss': sample_from_train['gloss'],
#     'text': sample_from_train['text'],
#     'sign': sample_from_train['sign'],
# }
# print(sample_dict)
# print(sample_dict['sign'].size())

