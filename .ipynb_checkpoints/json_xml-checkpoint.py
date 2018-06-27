import glob 
import json
import cv2
json_folder = 'AIMVAS_HAVC/vehicles/out/'
json_files = glob.glob(json_folder+"/*")


def make_annotations(data):
    zind = 0
    for z in data:
        filename = data[zind]["path"]
        basename, file_extension = os.path.splitext(filename)
        f = open(basename + '.xml','w') 
        line = "<annotation>" + '\n'
        f.write(line)
        line = '\t\t<folder>' + data[zind]['folder'] + '</folder>' + '\n'
        f.write(line)
        line = '\t\t<filename>' + data[zind]['filename'] + '</filename>' + '\n'
        f.write(line)
        line = '\t\t<path>' + data[zind]['path'] + '</path>' + '\n'
        f.write(line)
        line = '\t\t<source>\n\t\t\t<database>Unknown</database>\n\t\t</source>\n'
        f.write(line)
#         line = '\t<size>\n\t\t<width>'+ str(data[zind]['width']) + '</width>\n\t\t<height>' + str(data[zind]['height']) + '</height>\n\t'
#         line += '\t<depth>' + str(data[zind]['depth']) + '</depth>\n\t</size>'
#         f.write(line)
        line = '\n\t<segmented>0</segmented>'
        f.write(line)
        
        ind = 0
        for i in data[zind]["annotations"]:
            line = '\n\t<object>'
            line += '\n\t\t<name>' + i[0] + '</name>\n\t\t<pose>0</pose>'
            line += '\n\t\t<truncated>0</truncated>\n\t\t<difficult>0</difficult>'
            xmin = (i[1])
            line += '\n\t\t<bndbox>\n\t\t\t<xmin>' + str(xmin) + '</xmin>'
            xmax = (i[2])
            line += '\n\t\t\t<xmax>' + str(xmax) + '</xmax>'
            ymin = (i[3])
            line += '\n\t\t\t<ymin>' + str(ymin) + '</ymin>'
            ymax = (i[4])
            line += '\n\t\t\t<ymax>' + str(ymax) + '</ymax>'
            line += '\n\t\t</bndbox>'
            line += '\n\t</object>'     
            f.write(line)
            ind +=1
        line = "\n<annotation>" + '\n'
        f.write(line)
        f.close()
        zind +=1

        
new_data = []
for file in json_files:
    
    temp_dict = {}
    with open(file) as f:
        data = json.load(f)
        image_name = data[0]
        folder,_,filename = image_name.split("/")
        path = image_name
        #path = os.path.join("/bv/naveen/MobileNet_Keras/",image_name)
 
        temp_dict['folder'] = folder
        temp_dict['filename'] = filename
        temp_dict['path'] = path

        im = cv2.imread(image_name)
        h,w,d = im.shape
        temp_dict['height'] = h
        temp_dict['width'] = w
        temp_dict['depth'] = d
        
        temp_dict['annotations'] = []
        # if any annotations exist
        if(len(data)):
        
            for i in range(1,len(data)):

                temp_label = data[i]
                label = temp_label['label']
                xmin = temp_label['topleft']['x']
                ymin = temp_label['topleft']['y']
                xmax = temp_label['bottomright']['x']
                ymax = temp_label['bottomright']['y']

                temp_dict['annotations'].append([label,xmin,xmax,ymin,ymax])
            
    new_data.append(temp_dict)


make_annotations(new_data)

