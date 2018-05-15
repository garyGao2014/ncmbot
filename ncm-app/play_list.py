#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import urllib2
import threading
import ncmbot
import time
phone = '15017315191'


# r = ncmbot.login(phone=phone, password=pwd)
# next = True;
# if r.json().get('code') == 200:
#     loginR = r.content
#     print("登录信息",loginR)
# else:
#     next = False
#     print("登录失败");

def all():
    play_list_r = ncmbot.user_play_list(289073091)
    print("用户歌单信息:" + play_list_r.content)
    play_list_json = play_list_r.json()
    play_list_dict = {}
    play_list_list = []
    for play_list in play_list_json['playlist']:
        print(str(play_list))
        id = str(play_list['id']);
        print("id:" + id)
        play_list_detail = ncmbot.play_list_detail(id, limit=20)
        print(str(play_list_detail.content))
        play_detail_json = play_list_detail.json()
        for tracks in play_detail_json['playlist']['trackIds']:
            play_list_list.append(tracks['id'])

    print("长度" + str(play_list_list.__len__()))
    song_detail_r = ncmbot.song_detail(play_list_list)
    song_detail_r_json = song_detail_r.json();
    print(song_detail_r.content)
    for song in song_detail_r_json['songs']:
        play_list_dict[song['id']] = song['name']

    music_url_r = ncmbot.music_url(ids=play_list_list)
    music_url_r_json = music_url_r.json();
    print(music_url_r.content)
    url_list = {}

    print(play_list_dict)
    for data in music_url_r_json['data']:
        name = play_list_dict.get(data['id'])
        print(name + "|" + str(data['url']))
        url_list[name] = data['url']

    return url_list
    # for name, url in url_list.items():
    #     download(name, url)


def download(name, url):
    if url is None:
        print("name...." + name + "....url is None,continue....")
        return
    name = name.replace("/", "-")
    path = "/Users/garygao/Music/pyfetch_music/"
    if os.path.isdir(path) is False:  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
        print 'dir not exists'
        os.mkdir(path)  ##只能创建单级目录，用这个命令创建级联的会报OSError错误         print 'mkdir ok
    print("ready download..." + name + "...." + url)
    file_name = path + name + '.mp3'
    f = urllib2.urlopen(url)
    if os.path.exists(file_name):
        local_size = os.stat(file_name).st_size
        remote_size = f.info()['Content-Length']
        if local_size >= remote_size:
            print(file_name + " is exist")
            return
        else:
            print("local_size:" + str(local_size))
            print("remote_size:" + str(remote_size))
            # os.remove(file_name)

    print("downloading..." + name + "...." + url)

    # with open(file_name, "wb") as code:
    #     code.write(f.read())


if __name__ == '__main__':
    url_lists = all()
    times = 0;
    for name,url in url_lists.items():
        times=times+1
        if times >=10:
            time.sleep(5)
            times=0

        down_thread = threading.Thread(target=download,args=(name,url))
        down_thread.setDaemon(True)
        down_thread.start()
