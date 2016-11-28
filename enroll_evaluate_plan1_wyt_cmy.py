# @file evaluate.py
# @brief enroll & evaluate
# @author scusjs@foxmail.com, my@imcmy.me
# @version 0.2.00
# @date 2016-9-3

import requests
from configparser import RawConfigParser
from bs4 import BeautifulSoup

debug = False


class UCASEvaluate:
    def __init__(self):
        self.__readCoursesId()

        cf = RawConfigParser()
        cf.read('config')
        self.username = cf.get('info', 'username')
        self.password = cf.get('info', 'password')
        self.enroll = cf.getboolean('action', 'enroll')
        self.evaluate = cf.getboolean('action', 'evaluate')

        self.loginPage = 'http://sep.ucas.ac.cn'
        self.loginUrl = self.loginPage + '/slogin'
        self.courseSystem = self.loginPage + '/portal/site/226/821'
        self.courseBase = 'http://jwxk.ucas.ac.cn'
        self.courseIdentify = self.courseBase + '/login?Identity='
        self.courseSelected = self.courseBase + '/courseManage/selectedCourse'
        self.courseSelectionBase = self.courseBase + '/courseManage/main'
        self.courseCategory = self.courseBase + '/courseManage/selectCourse?s='
        self.courseSave = self.courseBase + '/courseManage/saveCourse?s='

        self.studentCourseEvaluateUrl = 'http://jwjz.ucas.ac.cn/Student/DeskTopModules/'
        self.selectCourseUrl = 'http://jwjz.ucas.ac.cn/Student/DesktopModules/Course/SelectCourse.aspx'

        self.enrollCount = {}
        self.headers = {
            'Host': 'sep.ucas.ac.cn',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }

        self.s = requests.Session()
        loginPage = self.s.get(self.loginPage, headers=self.headers)
        self.cookies = loginPage.cookies

    def login(self):
        postdata = {
            'userName': self.username,
            'pwd': self.password,
            'sb': 'sb'
        }
        self.s.post(self.loginUrl, data=postdata, headers=self.headers)
        if 'sepuser' in self.s.cookies.get_dict():
            return True
        return False

    def __readCoursesId(self):
        coursesFile = open('./courseid', 'r')
        self.coursesId = {}
        for line in coursesFile.readlines():
            line = line.strip().replace(' ', '').split(':')
            courseId = line[0]
            isDegree = False
            if len(line) == 2 and line[1] == 'on':
                isDegree = True
            self.coursesId[courseId] = isDegree

    def enrollCourses(self):
        response = self.s.get(self.courseSystem, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        if debug:
            print(response.text)
            exit()
        try:
            identity = str(soup).split('Identity=')[1].split('"'[0])[0]
            coursePage = self.courseIdentify + identity
            response = self.s.get(coursePage)
            response = self.s.get(self.courseSelected)
            if debug:
                print(response.text)
                exit()

            for eachCourse in self.coursesId:
                if eachCourse in response.text:
                    print("Course " + eachCourse + " has been selected.")
                    continue
                if (eachCourse in self.enrollCount and
                        self.enrollCount[eachCourse] == 1):
                    continue
                self.enrollCount[eachCourse] = 1
                result = self.__enrollCourse(eachCourse,
                                             self.coursesId[eachCourse])
                if result:
                    self.enrollCount[eachCourse] = 0
        except Exception as exception:
            print("System error")
            print(exception)
            exit()
        except KeyboardInterrupt:
            print("Bye")

    def __enrollCourse(self, courseId, isDegree):
        response = self.s.get(self.courseSelectionBase)
        if debug:
            print(response.text)
            exit()

        soup = BeautifulSoup(response.text, 'html.parser')
        categories = dict([(label.contents[0][:2], label['for'][3:])
                          for label in soup.find_all('label')[2:]])
        categoryId = categories[courseId[:2]]
        identity = soup.form['action'].split('=')[1]

        postdata = {
            'deptIds': categoryId,
            'sb': 0
        }
        categoryUrl = self.courseCategory + identity
        response = self.s.post(categoryUrl, data=postdata)
        if debug:
            print(response.text)
            exit()

        soup = BeautifulSoup(response.text, 'html.parser')
        courseTable = soup.body.form.table.find_all('tr')[1:]
        courseDict = dict([(c.span.contents[0], c.span['id'].split('_')[1])
                           for c in courseTable])

        if courseId in courseDict:
            postdata = {
                'deptIds': categoryId,
                'sids': courseDict[courseId]
            }
            if isDegree:
                postdata['did_' + courseDict[courseId]] = courseDict[courseId]

            courseSaveUrl = self.courseSave + identity
            response = self.s.post(courseSaveUrl, data=postdata)
            if debug:
                print(response.text)
                exit()
            if 'class="error' not in response.text:
                print('[Success] ' + courseId)
                return True
            else:
                print('[Fail] ' + courseId)
                return False
        else:
            print("No such course")
            return True

    # def getCourse(self):
    #     response = self.s.get(self.courseSystem, headers=self.headers)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     if debug:
    #         print(response.text.encode('utf8'))
    #     indentity = str(soup.noscript).split('Identity=')[1].split('"'[0])[0]
    #     coursePage = self.courseIdentify + indentity
    #     response = self.s.get(coursePage)
    #     response = self.s.get(self.courseSelected)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     listLi = (str)(soup.select('div[class="Menubox"]')[0]).split('SwichClass(this,"MainFrame",')
    #     evaluateCouse = self.studentCourseEvaluateUrl + listLi[3].split('"')[1]
    #     response = self.s.get(evaluateCouse)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     courseListResource = soup.body.table.tbody.find_all('tr')[3:-2]
    #     courseDict = {}
    #     if len(courseListResource) == 0:
    #         self.courseDict = courseDict
    #     for course in courseListResource:
    #         tdList = course.find_all('td')
    #         if tdList[-1].a is None:
    #             continue
    #         courseUrl = tdList[-1].a['href']
    #         courseName = tdList[1].a.string.strip()
    #         evaluateFlag = tdList[-1].a.string.encode('utf-8')
    #         if evaluateFlag == '评估':
    #             courseDict[courseName] = courseUrl
    #     self.courseDict = courseDict

    # def evaluateCourse(self):
    #     if len(self.courseDict) == 0:
    #         print('there is no course need to be evaluated')
    #         return
    #     for course in self.courseDict:
    #         print('start evaluate ' + course + '...')
    #         evaluateUrl = self.studentCourseEvaluateUrl + 'Evaluate/' + self.courseDict[course]
    #         self.__evaluate(evaluateUrl)

    # def __evaluate(self, evaluateUrl):
    #     postData = {}
    #     response = self.s.get(evaluateUrl)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     formResource = soup.body.form
    #     formList = formResource.contents

    #     for inputResource in formResource.contents:
    #         if (str)(inputResource).strip() != '':
    #             if inputResource.name == 'input':
    #                 postData[inputResource['name']] = inputResource['value']
    #             elif inputResource.name == 'table':
    #                 subTable = inputResource.contents[1].contents[2].td.table.find_all(attrs={'class': 'GbText'})
    #                 for eachTable in subTable:
    #                     for eachInput in eachTable.find_all('input'):
    #                         label = eachInput.next_sibling.string.encode('utf-8')
    #                         if label == '优' or label.find('优') != -1:
    #                             postData[eachInput['name']] = eachInput['value']
    #                 # subText = inputResource.contents[1].contents[4]
    #                 postData['rbtnList'] = 5
    #             postData['tbMerit'] = "本课程老师非常优秀，讲的知识也非常有用。"
    #             postData['tbSuggest'] = ''
    #             postData['tbFlaw'] = ''
    #             postData['btnSave'] = "保存我的评论"

    #     response = self.s.post(evaluateUrl, data=postData)
    #     if (response
    #             .text.encode('utf-8')
    #             .find("<script>alert('恭喜您，提交对该课程的评论成功……')</script>") != -1):
    #         print('evaluate success...')
    #     else:
    #         if debug:
    #             print(response.text)
    #         print('evaluate error!')


if __name__ == "__main__":
    ucasEvaluate = UCASEvaluate()

    if not ucasEvaluate.login():
        print('Login error. Please check your username and password.')
        exit()
    print('Login success')

    if ucasEvaluate.enroll:
        print('Enrolling start')
        ucasEvaluate.enrollCourses()
        print('Enrolling finish')

    # if ucasEvaluate.evaluate:
    #     print('Evaluating course...')
    #     ucasEvaluate.getCourse()
    #     if len(ucasEvaluate.courseDict) == 0:
    #         print('There is no course need to be evaluated')
    #         exit()
    #     print(str(len(ucasEvaluate.courseDict)) + ' courses need to be evaluated.')
    #     ucasEvaluate.evaluateCourse()
