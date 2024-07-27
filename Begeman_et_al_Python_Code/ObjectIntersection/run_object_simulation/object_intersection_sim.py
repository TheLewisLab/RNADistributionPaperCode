import random
from statistics import mean
from statistics import stdev
from tqdm import tqdm
'''
total_v = 672.4752740799601
obj1_count = 890
obj1_v = 0.06904345149799568
obj2_count = 1085
obj2_v = 0.03822091586886189
percent_overlap_required = 80.0
'''
def colide(position, list_of_positions, object_size):
    for pos in list_of_positions:
        if abs(position - pos) < object_size:
            return True
    return False

def place_positions(object_count, object_size, total_area_size):
    obj_postions = []
    if (object_count * object_size) < total_area_size:
        while(len(obj_postions) < object_count):
            temp_pos = random.random() * total_area_size
            if not colide(temp_pos, obj_postions, object_size):
                obj_postions.append(temp_pos)
    return obj_postions

def overlap_percentage(obj1_position, obj1_size, obj2_position, obj2_size):
    obj1_lb = obj1_position - (obj1_size / 2.0)
    obj1_rb = obj1_position + (obj1_size / 2.0)
    obj2_lb = obj2_position - (obj2_size / 2.0)
    obj2_rb = obj2_position + (obj2_size / 2.0)
    if obj1_lb > obj2_rb or obj1_rb < obj2_lb:
        overlap = 0
    else:
        if obj1_lb >= obj2_lb and obj1_rb >= obj2_rb:
            overlap = obj2_rb - obj1_lb
        elif obj1_lb <= obj2_lb and obj1_rb <= obj2_rb:
            overlap = obj1_rb - obj2_lb
        elif obj1_lb < obj2_lb and obj1_rb > obj2_rb:
            overlap = obj2_size
        elif obj1_lb > obj2_lb and obj1_rb < obj2_rb:
            overlap = obj1_size
        else:
            print('you fucked up')
            print(obj1_lb)
            print(obj1_rb)
            print(obj1_size)
            print(obj2_lb)
            print(obj2_rb)
            print(obj2_size)

    return (overlap / min(obj1_size, obj2_size)) * 100.0

def calculate_overlap(obj1_positions, obj1_size, obj2_positions, obj2_size, overlap_percentage_required):
    overlap_number = 0
    obj1_positions = sorted(obj1_positions)
    obj2_positions = sorted(obj2_positions)
    for obj1 in obj1_positions:
        for obj2 in obj2_positions:
            if overlap_percentage(obj1, obj1_size, obj2, obj2_size) > overlap_percentage_required:
                overlap_number += 1
                break
            elif (obj1 < (obj2 - obj2_size - obj1_size)):
                break

    return (overlap_number / len(obj1_positions)) * 100.0

def simulation(obj1_count, obj1_size, obj2_count, obj2_size, total_area_size, percent_overlap_required, n_to_run):
    running_overlap_percentages = []
    for n in tqdm(range(n_to_run)):
        obj1_positions = place_positions(obj1_count, obj1_size, total_area_size)
        obj2_positions = place_positions(obj2_count, obj2_size, total_area_size)
        running_overlap_percentages.append(calculate_overlap(obj1_positions, obj1_size, obj2_positions, obj2_size, percent_overlap_required))
    return mean(running_overlap_percentages), stdev(running_overlap_percentages)

#print(simulation(obj1_count, obj1_v, obj2_count, obj2_v, total_v, 80.0, 100))





