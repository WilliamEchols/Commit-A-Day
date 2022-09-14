# Goal: randomized layer-image generation

from tkinter import N
import yaml
import json
import random
import numpy as np
from PIL import Image

# dev config and file imports

gen_num = 1000
gen_name = 'Pinata #'
gen_desc = 'Your very own party pinata!'

config_file = './img/config.yaml'
save_folder = 'output/'
all_trait_objs = []
random.seed(7734)

# load data 

with open(config_file, 'r') as stream:
  try:
    configs = yaml.safe_load(stream)
  except yaml.YAMLError as exc:
    print(exc)

# functions
def probs_randomizer(values, probs):
  selected_trait_num = random.choices(population = list(range(0, len(values))), weights = probs, k = 1).pop()
  selected_trait = values[selected_trait_num]
  return (selected_trait, selected_trait_num)

def random_trait(trait):
  category = configs[trait]
  values = category['values']
  probs = category['probs'] 
  
  randomized_values = probs_randomizer(values, probs)
  selected_trait = randomized_values[0]
  selected_trait['chance'] = probs[randomized_values[1]]

  # generate sub properties
  sub_values = selected_trait['values']
  sub_names = selected_trait['sub_names']
  sub_probs = selected_trait['probs']
  sub_randomized_values = probs_randomizer(sub_values, sub_probs)
  selected_trait['sub_value'] = sub_randomized_values[0]
  selected_trait['sub_chance'] = sub_probs[sub_randomized_values[1]]
  selected_trait['sub_name'] = sub_names[sub_randomized_values[1]]


  return selected_trait

def gen_NFT_props():
  traits = []
  for i in range(len(configs)): # for each category
    category_name = configs[i]['category']
    trait_obj = random_trait(i)
 
    selected_trait = {
       'name' : trait_obj['name'],
       'category' : category_name,
       'id' : trait_obj['id'],
       'type' : configs[i]['type'],
       'chance': trait_obj['chance'],
       'src' : configs[i]['folder'] + trait_obj['src'],
       'sub_value' : trait_obj['sub_value'],
       'sub_name' : trait_obj['sub_name'],
       'sub_chance' : trait_obj['sub_chance'],
       'layer' : configs[i]['layer']
    }

    
    traits.append(selected_trait)

  common_layer = {
    'name' : 'Common Layer',
    'category' : 'common',
    'id' : 'common-layer',
    'type' : 'img',
    'chance' : 1.00,
    'src' : './img/common_layer.png',
    'sub_value' : 0,
    'sub_name' : 'N/A',
    'sub_chance' : 1.00,
    'layer' : 0
  }

  traits.append(common_layer)

  return sorted(traits, key=lambda x: x['layer'], reverse=True)

def layer_images(lower_img, upper_img):
  lower_img.paste(upper_img, (0, 0), mask = upper_img)
  return lower_img

def retrieve_frame(frame_obj):
  if frame_obj['type'] == 'value':
    retrieve_img = Image.open(frame_obj['src'])
    rgb_value = tuple(int(frame_obj['sub_value'][i:i+2], 16) for i in (0, 2, 4))
    retrieve_img = fill_blueprint(retrieve_img, (0, 0, 0), rgb_value)

    #print(frame_obj['src'])
  elif frame_obj['type'] == 'img':
    retrieve_img = Image.open(frame_obj['src'])
  return retrieve_img

def gen_NFT():
  traits = gen_NFT_props()
  props = []
  
  bgr_obj = traits.pop()
  props.append(bgr_obj)

  lower_img = retrieve_frame(bgr_obj)

  for i in range(len(traits)):
    upper_obj = traits.pop()
    props.append(upper_obj)

    upper_img = retrieve_frame(upper_obj)
    lower_img = layer_images(lower_img, upper_img)

  #NFT_img = lower_img.resize((320, 320),resample=Image.NEAREST)
  NFT_img = lower_img.resize((320, 320),resample=Image.Resampling.NEAREST)
  return {'img' : NFT_img, 'props' : props}

def fill_blueprint(blueprint_img, init_color, main_color):
  blueprint_img = blueprint_img.convert('RGBA')
  
  data = np.array(blueprint_img)

  full_data_array = data[..., :-1]
  for x in range(len(full_data_array)):
    row_data_array = full_data_array[x]
    for y in range(len(row_data_array)):
      pixel_data_array = row_data_array[y]
      for i in range(len(pixel_data_array)):
        # determine degree of shading
        previous_value = data[..., :-1][x][y][i]


        new_color = main_color[i] * (1 - (previous_value / 100))
        if pixel_data_array[0] == 233 and pixel_data_array[1] == 233 and pixel_data_array[2] == 233: # exception for off-white (233, 233, 233) pixels only
          new_color = pixel_data_array[0] 

        data[..., :-1][x][y][i] = new_color

  return Image.fromarray(data)

def main():
  for i in range(gen_num): # generate each image
    NFT_obj = gen_NFT()
    while NFT_obj['props'] in all_trait_objs:
      # failed uniqueness -> re-roll props
      NFT_obj = gen_NFT()
    all_trait_objs.append(NFT_obj['props'])

    # path and file name (not extension) for image and json - also need to change meta['name'] if this is manipulated
    NFT_name = str(i)


    # write image
    NFT_obj['img'].save(save_folder + NFT_name + '.png')

    # general metadata
    meta = {
      'name': gen_name + NFT_name,
      'description' : gen_desc,
      #'image' : 'ipfs://asset_cid',
      'attributes': []
    }

    # attributes and style formatting
    for p in range(len(NFT_obj['props'])):
      prop = NFT_obj['props'][p]
      if prop['category'] != 'common': # disregard properties of the common group
        attribute = { prop['category'] : prop['name'], 'rarity' : prop['chance'] }
        meta['attributes'].append(attribute)
        if prop['sub_chance'] != 1.00: # add another property for sub-properties if there are possibilities
          sub_attribute = { prop['category'] + ' Style' : prop['sub_name'], 'rarity' : prop['sub_chance'] }
          meta['attributes'].append(sub_attribute)
  
    # writting json metadata
    with open(save_folder + NFT_name + '.json', 'w', encoding='utf-8') as f:
      json.dump(meta, f, ensure_ascii=False, indent=2)

main()
