# -*- coding: UTF-8 -*-
import json
import os
import requests
import time
import re
from subprocess import call

# Authorization
cookie = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXRhaWwiOnsidXNlcklkIjoxMDA3MTI1NDE5LCJ1c2VyTmFtZSI6IjAxOGN6dDAwNyIsInBhc3N3b3JkIjoiIiwidXNlcklkZW50aXR5IjozLCJlbmFibGUiOjEsInNjaG9vbFVzZXJJZCI6MCwic2Nob29sSWQiOjAsInNjaG9vbFVzZXJSZWYiOm51bGwsInNjaG9vbEdyb3VwSWQiOm51bGwsInJvbGVzIjpbNV0sInVybExpc3QiOm51bGx9LCJleHAiOjE1ODQ4MDQ0MDcsInVzZXJfbmFtZSI6IjAxOGN6dDAwNyIsImp0aSI6IjNkMDBiYTk0LWVkYWEtNDdhNS1hZDNhLTk3NTI1YzE5MzA2MyIsImNsaWVudF9pZCI6IkQ2QzU3OEVERkVBNzBBNzc0MDlERjE4MDI0NEQxRUI3Iiwic2NvcGUiOlsiYWxsIiwid2ViIiwibW9iaWxlIl19.IlBIG7k4T5sp8jIu5_qG-ibywDRnN1NKRbNmZIj67pk'

downloadPath = 'C:/Users/sy/Desktop/云学习'

subjectNum = {
    '数学': 2
}

chooseGrade = 4
chooseSubject = 2

courseListGet = {
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

courseDetailGet = {
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


# 调用IDM下载
def callIDM(downloadUrl, filepath, filename):
    print("下载链接：", downloadUrl, "下载目录：", filepath, "文件名称：", filename)
    IDMpath = "D:/Internet Download Manager/IDMan.exe"
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
    data = requests.get(requestUrl, params=requestData, headers=courseDetailGet)
    data = json.loads(data.text)['data']
    name = data['resourceName']+'.mp4'
    introduction = data['introduction']
    videoUrl = data['mp4URL']
    # print(videoUrl)
    callIDM(videoUrl, downloadPath, name)
    time.sleep(5)


def getCourseList(gradeID, subjectID):
    requestData = {
        'subjectId': subjectID,
        'gradeId': gradeID,
        'r': 0.002752869871963881
    }
    url = 'https://school.etiantian.com/api-study-service/api/xicheng/subject/grade/res'
    courseList = requests.get(url, params=requestData, headers=courseListGet)

    courseList = json.loads(courseList.text)
    courseList = courseList['data']
    print(courseList)
    for i in courseList:
        getCourseDetail(i['resourceId'])


getCourseList(chooseGrade, chooseSubject)
