import os
import requests
import shutil


def get_save_image_directory_path(directory_name):
    current_directory_path = os.getcwd()
    save_image_directory_path = f'{current_directory_path}{os.sep}{directory_name}'

    return save_image_directory_path


def make_image_directory(path_name):
    if not os.path.isdir(path_name):
        os.mkdir(path_name)


def get_child_save_image_directory_path(parent_path, directory_number):
    child_save_image_directory_path = f'{parent_path}{os.sep}{directory_number}'

    return child_save_image_directory_path


def get_image_id_url(file_name):
    with open(file_name, "r") as files:
        lines = files.readlines()
        image_id_url_dict = {}

        for idx, line in enumerate(lines):
            if idx == 0:
                continue
            components = line.strip().split()

            image_id_url_dict[components[0]] = components[2]

    return image_id_url_dict


def main():
    photo_file_name = "photos.tsv000"
    save_image_directory_name = "unsplash_images"

    photo_info_dict = get_image_id_url(photo_file_name)
    save_image_directory_path_string = get_save_image_directory_path(save_image_directory_name)

    make_image_directory(save_image_directory_path_string)

    for child_directory_number in range(len(photo_info_dict) // 5000):
        child_directory_path = get_child_save_image_directory_path(save_image_directory_path_string, child_directory_number)
        make_image_directory(child_directory_path)

    for idx, id_url in enumerate(photo_info_dict.items()):
        image_id, image_url = id_url[0], id_url[1]
        directory_number = (idx + 1) // 5000
        print(image_id, image_url, directory_number)

        save_file_path = f'{save_image_directory_path_string}{os.sep}{directory_number}{os.sep}{image_id}.jpg'

        response = requests.get(image_url, stream=True)
        with open(save_file_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


if __name__ == "__main__":
    main()




"""

# url = "http://craphound.com/images/1006884_2adf8fc7.jpg"
# response = requests.get(url)
# if response.status_code == 200:
#     with open("/Users/apple/Desktop/sample.jpg", 'wb') as f:
#         f.write(response.content)


#
# import requests
#
# url = 'http://example.com/img.png'
# response = requests.get(url, stream=True)
# with open('img.png', 'wb') as out_file:
#     shutil.copyfileobj(response.raw, out_file)
# del response

"""
