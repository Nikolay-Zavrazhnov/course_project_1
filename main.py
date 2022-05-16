def importing_photos_from_VK_to_YaDisk():
    import time
    import requests
    from pprint import pprint
    from yandex import YaUploader
    from tqdm import tqdm
    import json

    data_json =[]
    def dict_create(**structure):

        data_json.append(structure)

    def creating_json_file(data):
        with open('file.json', 'w') as json_file:
            json.dump(data, json_file)

    user_ids = input('enter the VK user ID:')
    ya_token = input('enter token YandexDisk:')
    new_path = input('введите имя папки на YaDisk')

    def creating_uploading_path():

        new_folder = YaUploader(ya_token)
        new_folder.creating_a_folder(new_path)


    def seved_photos(count=5):
        list_name = []
        upload_file_yadisk = YaUploader(ya_token)

        with open('token_vk.txt', 'r') as file_token: # файл token_vk.txt должен содержать ключ пользователя VK
            token_vk = file_token.read().strip()
            print(token_vk)
            URl = 'https://api.vk.com/method/photos.get'
            params = {'album_id': 'profile', 'access_token': token_vk, 'extended': 1, 'rev': 0, 'count': count,
                      'owner_id': user_ids, 'v': '5.131'}
            res = requests.get(URl, params=params)
            # pprint(res.json()['response'])

            for id_photo, size in enumerate(res.json()['response']['items']):
                pprint(res.json()['response']['items'][id_photo]['sizes'][-1]['url'])
                size = res.json()['response']['items'][id_photo]['sizes'][-1]['type']
                url_photos = res.json()['response']['items'][id_photo]['sizes'][-1]['url']
                like_photo = res.json()['response']['items'][id_photo]['likes']['count']
                date_photo = res.json()['response']['items'][id_photo]['date']

                if f"{like_photo}.jpg" not in list_name:
                    list_name.append(f"{like_photo}.jpg")
                    path = f"/{new_path}/{like_photo}.jpg"
                    upload_file_yadisk.upload_from_url(path=path, file_url=url_photos)
                    dict_create(file_name=f"{like_photo}.jpg", size=size)
                else:
                    list_name.append(f"{like_photo}_{date_photo}.jpg")
                    path = f"/{new_path}/{like_photo}_{date_photo}.jpg"
                    upload_file_yadisk.upload_from_url(path=path, file_url=url_photos)
                    dict_create(file_name=f"{like_photo}_{date_photo}.jpg", size=size)

        for i in tqdm(list_name):
            time.sleep(0.7)

        # pprint(list_name)
        creating_json_file(data_json)

    creating_uploading_path()
    seved_photos()
    # pprint(data_json)
importing_photos_from_VK_to_YaDisk()


