# -*- coding: UTF-8 -*-
import json
import os
import requests
import re
import time
from subprocess import call

# downloadPath = os.getcwd()

# ===============
# X-DT-accessToken
# cookie = ""

# weekNum第几周
# chooseWeek = [7]

# 1308 初二
# 1307 初一
# chooseGrade = [1307]

downloadPath = "C:/Users/sy/Downloads/cloud/"
# ===============

gradeList = """
对照表：

初二：1308
初一：1307

"""



# 传统下载，太慢了，已经废弃
def download(download_url, filepath, filename):
    r = requests.get(download_url, stream=True)
    p = filepath + '/' + filename
    print("downloading...")
    f = open(p, "wb")
    for chunk in r.iter_content(chunk_size=2048):
        if chunk:
            f.write(chunk)
    f.close()


def mkdir(p):
    folder = os.path.exists(p)
    if not folder:
        os.makedirs(p)
        print("---  new folder...  ---:")
    else:
        print("---  There is this folder!  ---")


# 调用IDM下载
def callIDM(downloadUrl, filepath, filename):
    print("下载链接：", downloadUrl, "下载目录：", filepath, "文件名称：", filename)
    IDMpath = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
    call([IDMpath, '/d', downloadUrl, '/f', filename, '/p', filepath, '/n'])
    print("IDM downloading...\n")
    # 最好加上这个
    time.sleep(10)


# 文件名修改
def reFilename(name):
    name = name.replace('?', '？')
    return name


def downloadCourseFiles(data,weekNum):
    # subjectName：科目
    # courseName：课程名称
    subjectName = data['data']['subjectName']
    courseName = data['data']['courseName']
    # if subjectName != "数学":
    #     return 0
    # 建立文件夹结
    newdirPath = downloadPath + '第' + str(weekNum) + '周/'
    newdirPath = newdirPath + subjectName + '/'
    mkdir(newdirPath)
    newdirPath = newdirPath + courseName + '/'
    mkdir(newdirPath)
    # 课程中文件列表
    videoList = data['data']['courseResourceVOList']

    for i in range(0, len(videoList)):
        idata = videoList[i]
        downloadFileName = reFilename(idata['resourceName'])
        downloadUrl = idata['resourceUrl']

        # 判断文件是否存在,不存在就下载
        if not os.access(newdirPath + downloadFileName, os.F_OK):
            # 调用IDM下载
            # download(downloadUrl, newdirPath, downloadFileName)
            callIDM(downloadUrl, newdirPath, downloadFileName)
        


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
    # chooseGrade = chooseGrade
    chooseWeek = input("请输入周数：")
    # chooseWeek = chooseWeek

    # for grade in chooseGrade:
    #     for week in chooseWeek:
    #         print(week,grade)
    #         getCourseList(week, grade)

    getCourseList(chooseWeek, chooseGrade)