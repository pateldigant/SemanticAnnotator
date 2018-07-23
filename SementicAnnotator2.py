import pandas as pd
import cv2
import numpy as np
import argparse
import os
import time

parser = argparse.ArgumentParser(description='Sementic Annotator')
parser.add_argument('csv_file', metavar='csv_file', type=str,
                    help='Path to the image and csv file. Write ./filename for current dir')
parser.add_argument('output_images_dir', metavar='output_images_dir', type=str,
                    help='Directory where the output masked images will be stored. Write ./ for cuurent dir')
start_time = time.time()
args = parser.parse_args()
output_path = args.output_images_dir

input_path = args.csv_file[:args.csv_file.rfind('/')+1]
if not os.path.exists(output_path):
    os.makedirs(output_path)

df = pd.read_csv(args.csv_file)
filenames = df.filename.unique()

for filename in filenames:
    
    temp_df = df.loc[df['filename'] == filename]
    
    data = {}
    colors = [(0,0,255),(0,255,0),(255,0,0),(0,255,255)]
    
    for index, row in temp_df.iterrows():
        polygon_string = row["region_shape_attributes"]
        label_string = row["region_attributes"]
        xy_points_string = polygon_string[polygon_string.find('"all_points_x"'):polygon_string.find('}')]
        xy_points_string = xy_points_string.split('],')
        x_points = xy_points_string[0]
        ##print(x_points)
        x_points = x_points[x_points.find('[')+1:]
        y_points = xy_points_string[1]
        y_points = y_points[y_points.find('[')+1:y_points.find(']')]
        ##print(x_points)
        x_points_int = [int(x) for x in x_points.split(',')]
        y_points_int = [int(x) for x in y_points.split(',')]
        class_label = label_string.split(':')[1][1:-2]
        #print(x_points_int,y_points_int,class_label)
        xy_pairs = []
        for xy in zip(x_points_int,y_points_int):
            xy_pairs.append(xy)
        #print(xy_pairs)
        if class_label not in data:
            data[class_label] = []
        data[class_label].append(xy_pairs)
        
    image = cv2.imread(""+ input_path +filename)
    mask = np.zeros((image.shape[0], image.shape[1],image.shape[2]))
    index = -1
    for key in data.keys():
        index += 1
        list_of_points = data[key]
        for points in list_of_points:
            pts = np.array(points)
            cv2.fillConvexPoly(mask, pts, color=colors[index])
    cv2.imwrite(""+ output_path + '/' + filename.split('.')[0] +'_mask'+'.jpg', mask)
    
    df = df[df['filename']!=filename]
end_time = time.time()
print('Processed {} files in {:.3f} seconds'.format(len(filenames) , end_time-start_time))