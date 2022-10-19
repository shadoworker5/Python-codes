"""
 * @author Kassoum TRAORE
 * @email shadoworker5.dev@gmail.com
 * @create date 2022-06-20 23:34:42
 * @modify date 2022-08-02 01:03:17
 * @desc [description]
"""
import os
import sys
from PIL import Image
# import art
from PIL.ExifTags import TAGS, GPSTAGS

all_files = list()
all_gps = list()
list_menu = ['Read images data', 'Read videos data', 'Draw road', 'Exit']

all_gps = []

def draw_position():
    if all_gps:
        longitude = convert_coord(float(all_gps[0]['GPSLongitude'][0]), float(all_gps[0]['GPSLongitude'][1]), float(all_gps[0]['GPSLongitude'][2]), all_gps[0]['GPSLongitudeRef'])
        latitude = convert_coord(float(all_gps[0]['GPSLatitude'][0]), float(all_gps[0]['GPSLatitude'][1]), float(all_gps[0]['GPSLatitude'][2]), all_gps[0]['GPSLatitudeRef'])
        url = f'https://maps.google.com/?q={latitude},{longitude}'
        print(url)
        try_again()
    else:
        print(f'Data not found')
        try_again()

def draw_map_road():

    coords = list()
    for i, item in enumerate(all_gps):
        longitude = convert_coord(float(all_gps[i]['GPSLongitude'][0]), float(all_gps[i]['GPSLongitude'][1]), float(all_gps[i]['GPSLongitude'][2]), all_gps[i]['GPSLongitudeRef'])
        latitude = convert_coord(float(all_gps[i]['GPSLatitude'][0]), float(all_gps[i]['GPSLatitude'][1]), float(all_gps[i]['GPSLatitude'][2]), all_gps[i]['GPSLatitudeRef'])
        coords.append(str(latitude)+','+str(longitude))
    
    # print(all_gps)
    # try_again()
    # url = f'https://www.google.com/maps/dir/?api=1&origin=Space+Needle+Seattle+WA&destination=Pike+Place+Market+Seattle+WA'
    # # url = f'https://maps.google.com/?q={coords}'
    # url = f'https://www.google.com/maps/dir/?api=1&origin={coords[0]}&destination={coords[2]}&travelmode=driving&waypoints={coords[1]}'
    # print(url)
    import webbrowser as browser
    url = f'https://www.google.com/maps/place/{coords[0]}/{coords[1]}'
    browser.open_new_tab(url)
    
def convert_coord(degree, minutes, seconds, direction):
    result = degree + (minutes / 60) + (seconds / 3600)
    return result

def video_metadata(files):
    pass

def write_result_in_file(message):
    with open('result.txt', 'w') as content:
        for item in message:
            content.write(item+'\n')

def read_data():
    exif_data = list()
    for it in all_files:
        item = Image.open(it)
        exif_data.append(f"-------------------------------------File {all_files.index(it) + 1} => {it}------------------------------------------")
        if item._getexif() != None:

            for key, values in item._getexif().items():
                tags = TAGS.get(key, key)
                if tags == 'GPSInfo':
                    gps_data = {}
                    for it, result in values.items():
                        if GPSTAGS.get(it, it) in ['GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude']:
                            gps_data[GPSTAGS.get(it, it)] = result
                        msg = f'{GPSTAGS.get(it, it)} => {result}'
                        exif_data.append(msg)
                    all_gps.append(gps_data)
                else:
                    msg = f'{tags} => {values}'
                    exif_data.append(msg)
        else:
            print("Data not found")

    print(exif_data)
    write_result_in_file(exif_data)
    try_again()

def get_files(*arg):
    extensions = [ext.lower() for ext in arg]

    with os.scandir() as files:
        for item in files:
            if item.is_file():
                for ext in extensions:
                    if item.name.endswith(ext):
                        all_files.append(item.name)
            else:
                print('Files not found')
    
def change_directorie():
    if os.getcwd() != 'images':
        os.chdir('images')

def get_input(msg, format):
    while True:
        try:
            response = format(input(msg))
            if isinstance(response, format):
                break
            else:
                print('Error type. please try again')
        except ValueError:
            print(f'Ooops!!! you must enter {format} type ')
            
    return response

def try_again():
    while True:
        response = get_input('\nDo you want to try again [Y/n] default [n]: ', str)
        if response == 'Y':
            main()
            break
        else:
            print('Good bye user')
            break

def choose_menu():
    while True:
        item = get_input('=> ', int)
        if item in range(len(list_menu) + 1):
            break
        else:
            item = get_input('=> ', int)
            print(f'Yous must choose between 1 and {len(list_menu)}')
    
    if item == 1:
        read_data()
    elif item == 2:
        print('Method not yet implemented')
        try_again()
    elif item == 3:
        draw_map_road()
    # elif item == 4:
    #     print(all_gps)
    #     print('Method not yet implemented')
    #     try_again()
    else:
        print('Good bye user')
        exit()

def main():
    get_files('jpg', 'png')

    for i, j in enumerate(list_menu):
        print(f'[{i+1}] {j}')

    print('\nChoise  one')
    choose_menu()

if __name__ == '__main__':
    # art.tprint('Shadoworker5')
    change_directorie()
    main()