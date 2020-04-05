# -*- coding: UTF-8 -*-
import json
import os
import requests
import time
import re
from subprocess import call

downloadPath = "Z:/学习/学校/初中/知行云课堂/初三/数学/"

subjectNum = {
    2: '数学',
    3: '英语',
    4: '物理'

}




# 调用IDM下载
def callIDM(downloadUrl, filepath, filename):
    print("下载链接：", downloadUrl, "下载目录：", filepath, "文件名称：", filename)
    IDMpath = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
    call([IDMpath, '/d', downloadUrl, '/f', filename, '/p', filepath, '/n'])
    print("IDM downloading...\n")


# 文件名修改
def reFilename(name):
    name = name.replace('?', '？')
    return name


def getCourseDetail(courseID):
    url = 'https://school.etiantian.com/api-resource-service/api/resources/xicheng/'
    requestUrl = url + str(courseID)
    requestData = {'r': 0.26856862694411543}
    requestHeaders = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Authorization': cookie,
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'school.etiantian.com',
        'Origin': 'https://xicheng.etiantian.com',
        'Referer': 'https://xicheng.etiantian.com/video.html?rid=705150',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    data = requests.get(requestUrl, params=requestData, headers=requestHeaders)
    data = json.loads(data.text)['data']
    name = data['resourceName']+'.mp4'
    # introduction = data['introduction']
    videoUrl = data['mp4URL']
    # print(videoUrl)

    # 判断文件是否存在,不存在就下载
    if os.access(downloadPath + name, os.F_OK):
        print(name,"已经有了")
    else:
        # 调用IDM下载
        callIDM(videoUrl, downloadPath, name)
    
    # time.sleep(2)


def getCourseList(gradeID, subjectID):
    requestData = {
        'subjectId': subjectID,
        'gradeId': gradeID,
        'r': 0.002752869871963881
    }
    requestHeaders = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Authorization': cookie,
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'school.etiantian.com',
        'Origin': 'https://xicheng.etiantian.com',
        'Referer': 'https://xicheng.etiantian.com/list.html?sid=2',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    url = 'https://school.etiantian.com/api-study-service/api/xicheng/subject/grade/res'
    courseList = requests.get(url, params=requestData, headers=requestHeaders)

    courseList = json.loads(courseList.text)
    courseList = courseList['data']
    # print(courseList)
    for i in courseList:
        getCourseDetail(i['resourceId'])



if __name__ == "__main__":
    cookie = input("cookie: ")
    
    chooseGrade = input("enter grade (default 4): ")
    print("""
2:数学
3:英语
4:物理
    """)
    
    chooseSubject = input("enter subject: ")

    getCourseList(chooseGrade,chooseSubject)