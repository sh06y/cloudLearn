# -*- coding: UTF-8 -*-
import json
import os
import requests
import re
import time
from subprocess import call
import easygui

# 弹出文件夹选择框
downloadPath = easygui.diropenbox()


gradeList = """
对照表：

初二：1308
初一：1307

"""

# 不用这个了，太慢
# def download(download_url, filepath, filename):
#     r = requests.get(download_url, stream=True)
#     p = filepath + '/' + filename
#     print("downloading...")
#     f = open(p, "wb")
#     for chunk in r.iter_content(chunk_size=2048):
#         if chunk:
#             f.write(chunk)
#     f.close()


def mkdir(p):
    folder = os.path.exists(p)
    if not folder:
        os.makedirs(p)
        print("---  new folder...  ---:")
    else:
        print("---  There is this folder!  ---")


# 调用IDM下载
# def callIDM(downloadUrl, filepath, filename):
#     print("下载链接：", downloadUrl, "下载目录：", filepath, "文件名称：", filename)
#     IDMpath = r".\idm\idm.exe"
#     a = call([IDMpath, '/d', downloadUrl, '/f', filename, '/p', filepath])
#     print(a)
#     print("IDM downloading...\n")
#     # 最好加上这个
#     time.sleep(5)

def callAria2(path,url,name):
    aria2 = os.getcwd() + r"\aria2\aria2.exe "
    p=open(os.getcwd()+'/aria2/aria2.conf','r',encoding='utf-8')
    q=open(os.getcwd()+'/aria2/aria2.conf','w',encoding='utf-8')
    number=0
    for i in p:   #循环打印poems的内容
        number += 1
        if number == 1:
            i = 'dir=' + path + '\n'
            q.write(i)  #把在poems中读取的内容写在poems1中
            q.close()
            break

    order = aria2 + "--conf-path=" + os.getcwd() + r"\aria2\aria2.conf -o " + name + ' ' + url
    os.system(order)


# 文件名修改
def reFilename(name):
    name = name.replace('?', '？')
    name = name.replace('<', '[')
    name = name.replace('>', ']')
    return name


def downloadCourseFiles(data,weekNum):
    # subjectName：科目
    # courseName：课程名称
    subjectName = data['data']['subjectName']
    courseName = data['data']['courseName']
    # if subjectName != "数学":
    #     return 0
    # 建立文件夹
    newdirPath = downloadPath + r"\\第" + str(weekNum) + r"周\\"
    # mkdir(newdirPath)
    newdirPath = newdirPath + subjectName + "\\"
    # mkdir(newdirPath)
    newdirPath = newdirPath + courseName + "\\"
    newdirPath = reFilename(newdirPath)
    mkdir(newdirPath)
    # 课程中文件列表
    videoList = data['data']['courseResourceVOList']

    for i in range(0, len(videoList)):
        idata = videoList[i]
        downloadFileName = reFilename(idata['resourceName'])
        downloadUrl = idata['resourceUrl']

        # 判断文件是否存在,不存在就下载
        if os.access(newdirPath + downloadFileName, os.F_OK):
            print(downloadFileName, "已经有了")
        else:
            # 调用IDM下载
            callAria2(newdirPath,downloadUrl,downloadFileName)
        


def getCourseDetail(course):
    corseDetailGetHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Action-Type': 'json',
        'Authorization': 'Basic c2FucmVuLXN0dWRlbnQtcGM6TWJuMjJ1eEduWXkxR3B2VWRw',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Host': 'class-api.3ren.cn',
        'Origin': 'https://class.3ren.cn',
        'Referer': 'https://class.3ren.cn/um/class/course/4071855977039847429/view.do?ynXicheng=1',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': "same-site",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.130 Safari/537.36',
        'X-DT-accessToken': cookie,
        'X-DT-clientId': 'sanren-student-pc',
        'X-DT-Passport': '',
        'X-DT-version': '1.7.0'
    }
    url = "https://class-api.3ren.cn/toolkits-center/course/detail?courseId="
    data = requests.get(url + course, headers=corseDetailGetHeaders)
    data = json.loads(data.text)
    return data


def getCourseList(weekNum,gradeCode):
    classListPostHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Action-Type': 'json',
        'Authorization': 'Basic c2FucmVuLXN0dWRlbnQtcGM6TWJuMjJ1eEduWXkxR3B2VWRw',
        'Connection': 'keep-alive',
        'Content-Length': '30',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Host': 'class-api.3ren.cn',
        'Origin': 'https://class.3ren.cn',
        'Referer': 'https://class.3ren.cn/um/xicheng-schedule.do?ynXicheng=1',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53'
                      '7.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'X-DT-accessToken': cookie,
        'X-DT-clientId': 'sanren-student-pc',
        'X-DT-Passport': '',
        'X-DT-version': '1.7.0'
    }
    postdata = {'weekNum': weekNum, 'gradeCode': gradeCode}

    classList_url = "https://class-api.3ren.cn/cms-center/xicheng/kebiao/list"

    # 获取课程列表，转换成json格式
    classList_Data = requests.post(classList_url, data=json.dumps(postdata), headers=classListPostHeaders)
    classList_Data = json.loads(classList_Data.text)
    # courseList为列表格式
    courseList = classList_Data['data']
    for i in range(0, len(courseList)):
        iCourseData = courseList[i]
        coursePageUrl = iCourseData['courseUrl']

        # 正则提出链接中的课程ID
        pattern = re.compile(r"(?<=course/)\d+\.?\d*")
        courseID = pattern.findall(coursePageUrl)
        courseID = courseID[0]
        courseDetailData = getCourseDetail(courseID)
        # print(courseDetailData)
        downloadCourseFiles(courseDetailData,weekNum)


if __name__ == "__main__":
    cookie = input("please enter your cookie (X-DT-accessToken): ")
    print(gradeList)
    chooseGrade = input("请输入年级编号: ")
    chooseWeek = input("请输入周数：")

    # for grade in chooseGrade:
    #     for week in chooseWeek:
    #         print(week,grade)
    #         getCourseList(week, grade)

    getCourseList(chooseWeek, chooseGrade)