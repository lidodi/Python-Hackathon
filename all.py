import csv
import os
import yaml


params={"iti" : 1,
        "stim_time" : 1,
        "itis": 0.3,
        "stim Position":(0,0),
        "stim_size":[400,400],
        "key_to_press": 'k',
        "cue_time":0.1,
        "pre_cue":0.7,
        "cue_size":[400,400],
        "cue_type": 'sound',
        "cue_position":(0,0),
        "cue_image_name": 'astriks_gabor.jpg',
        "cue_sound_value":"G",
        "images_folder_path": "Images/",
        "break_image": "break_image.jpg",
        "end_exp_img": "end_exp_img"}

with open('data.yml', 'w') as outfile:
    yaml.dump(params, outfile, default_flow_style=False)
sir=yaml.dump(params)
with open("data.yml", 'r') as stream:
    try:
        new_param=(yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)
print('hi')
#params={"iti" : 1,
#         "stim_time" : 1,
#         "itis": 0.3,
#         "stim Position":(0,0),
#         "stim_size":[400,400],
#         "key_to_press": 'k',
#         "cue_time":0.1,
#         "pre_cue":0.7,
#         "cue_size":[400,400],
#         "cue_type": 'sound',
#         "cue_position":(0,0),
#         "cue_image_name": 'astriks_gabor.jpg',
#         "cue_sound_value":"G",
#         "images_folder_path": "Images/"}
#
# csv_colums=['keys','values']
# currentPath = os.getcwd()
# csv_file = os.path.abspath('gigi.csv')
#
# def WriteDictToCSV(csv_file,csv_colums,params):
#
#         with open(csv_file, 'w') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=csv_colums)
#             writer.writeheader()
#             for data in params:
#                 writer.writerow(data)
#         return
#
#
# WriteDictToCSV(csv_file,csv_colums,params)
