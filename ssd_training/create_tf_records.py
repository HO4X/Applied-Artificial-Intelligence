## This uses the data generated previously and creates tf_records
import os
import tensorflow as tf 
# util - folder musst be in same directory
from object_detection.utils import dataset_util
# for visu
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

# reads the bounding box file
def getbboxcoordinates(path): 
    f= open(path,"r")
    line_str = f.read() # only use first line
    i = 0
    coordinates = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    numbers = line_str.split(' ')
    for number in numbers:
        coordinates[i] = (int(number))
        i = i + 1
    return coordinates

# Brief: creates tensorflow record
def create_cat_tf_example(filename, encoded_cat_image_data, image_width, image_height, bbox_tl_x, bbox_tl_y, bbox_br_x, bbox_br_y ):
  height = image_height
  width = image_width
  filename = bytes(filename, 'utf8') #the b makes it implicit to an byte
  image_format = b'jpg'
  # we want relative coordinates
  xmins = [bbox_tl_x / width]
  xmaxs = [bbox_br_x / width]
  ymins = [bbox_tl_y / height]
  ymaxs = [bbox_br_y / height]
  if(xmaxs[0] > 1):
    xmaxs[0] = 1; 
  if(ymaxs[0] > 1):
    ymaxs[0] = 1; 
  classes_text = [b'cat_face'] # we only have cats 
  classes = [1]
  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_cat_image_data),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  print(filename)
  return tf_example



def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    # TODO(user): Write code to read in your dataset to examples variable

    #for example in examples:
    #tf_example = create_tf_example(example)
    #writer.write(tf_example.SerializeToString())

    #writer.close()
  
    path = './'
    folders = []
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for folder in d:
            folders.append(os.path.join(r, folder))

    for folder in folders:
        if "CAT" in folder:
            print("Process folder -> " + folder)
            for rr, dd, ff in os.walk(folder):
                for file in ff:
                    if '.jpg.bound' in file:
                        files.append(os.path.join(rr, file))
            for ff in files:
                with open(ff.split('.bound')[0], "rb") as image:
                    pil_image = Image.open(ff.split('.bound')[0])
                    boundbox = getbboxcoordinates(ff)
                    width, height = pil_image.size
                    f = image.read()
                    encoded_image = bytes(bytearray(f))
                    # only jpg
                    tf_record = create_cat_tf_example(ff.split('.bound')[0].split('/')[2],encoded_image, width, height, boundbox[0], boundbox[1], boundbox[6], boundbox[7])
                    writer.write(tf_record.SerializeToString())
                    # check 
                    result = tf.train.Example.FromString(tf_record.SerializeToString())
    writer.close()

    

if __name__ == '__main__':
  tf.app.run()
