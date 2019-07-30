import requests
import re, hashlib, time

MyID='201601441'
MyPW='fanrui926Jwc'
CUR_MAX_SEMID=89

VirtualHeader={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Content-Type':'application/x-www-form-urlencoded'
}

def GetSemesterID():
    Year=input('请输入年份: ')
    try:
        Year=int(Year)
    except ValueError:
        print('请输入数字')
        return False
    Sem=input('请输入学期: ')
    try:
        Sem=int(Sem)
    except ValueError:
        print('请输入数字')
        return False
    if (Year<=2017):
        SemesterID=(Year-1994)*2+Sem-1
    elif (Year<=1994):
        print('请输入大于1994的年份')
        return False
    else:
        SemesterID=49+(Year-2018)*40+(Sem-1)*20
    if (SemesterID>CUR_MAX_SEMID):
        print('请输入有效学期')
        return False
    print('Semester ID: %d'%SemesterID)
    return SemesterID

def main(UserName,PassWord):
    # Init sessino
    YZU_JWC = requests.Session()

    # Login Page
    LoginPage = YZU_JWC.get('http://jwc3.yangtzeu.edu.cn/eams/login.action',headers=VirtualHeader)
    # print(LoginPage.text)
    SHA1_SALT=re.search('\w{8}(-\w{4}){3}-\w{12}',LoginPage.text,re.M)
    if (None==SHA1_SALT): # 找不到登录界面的SHA1 UUID
        print('Cannot resolve SHA1-salt at login page.')
        return False
    SHA1_SALT=SHA1_SALT.span()
    SHA1_SALT=LoginPage.text[SHA1_SALT[0]:SHA1_SALT[1]]
    SHA1_Pass=hashlib.sha1((SHA1_SALT+'-'+PassWord).encode()).hexdigest()
    print('UUID: %s'%SHA1_SALT)

    # Login
    time.sleep(1) # 防止检测
    LoginData={
        'username':UserName,
        'password':SHA1_Pass,
        'encodedPassword':'',
        'session_locale':'zh_CN'
    }
    VirtualHeader['Origin']='http://jwc3.yangtzeu.edu.cn'
    VirtualHeader['Referer']= 'http://jwc3.yangtzeu.edu.cn/eams/login.action'
    VirtualHeader['Host']= 'jwc3.yangtzeu.edu.cn'
    IndexPage=YZU_JWC.post('http://jwc3.yangtzeu.edu.cn/eams/login.action',headers=VirtualHeader,data=LoginData)
    if (IndexPage.text.find('密码错误')!=-1):
        print('密码错误')
        return False
    if (IndexPage.text.find('账户不存在')!=-1):
        print('账户不存在')
        return False
    # HomePage=YZU_JWC.get('http://jwc3.yangtzeu.edu.cn/eams/home.action',headers=VirtualHeader)
    # print(IndexPage.text)

    # Print Information
    SemesterID=GetSemesterID()
    while(True):
        print('* 1. 修改当前学期')
        # print('* 2. 学籍信息')
        # print('* 3. 培养计划')
        print('* 4. 我的课表')
        print('* 5. 选课')
        print('* 6. 我的考试')
        print('* 7. 我的成绩')
        print('* 8. 校外考试')
        print('* 9. 信息核准及补录')
        print('* 0. Quit')
        Task=input('请输入执行序号: ')
        try:
            Task=int(Task)
        except ValueError:
            print('请输入数字')
            continue
        if (0==Task):
            break
        elif (1==Task):
            SemesterID=GetSemesterID()
            # if (not SemesterID):
            #     continue
            # Result=YZU_JWC.get('http://jwc3.yangtzeu.edu.cn/eams/postgraduate/midterm/stdExamine!content.action?semester.id='+str(SemesterID)).text
            # if (-1!=Result.find('当前无中期考核申请信息。')):
            #     print('当前无中期考核申请信息。')
            # else:
            #     print(Result)
        # elif (2==Task):
        #     Result=YZU_JWC.get('http://jwc3.yangtzeu.edu.cn/eams/stdDetail.action').text
        #     print(Result)
        # elif (3==Task):
        #     Result=YZU_JWC.get('http://jwc3.yangtzeu.edu.cn/eams/myPlan.action').text
        #     print(Result)
        elif (4==Task):
            if (not SemesterID):
                continue
            Result=YZU_JWC.get('http://jwc3.yangtzeu.edu.cn/eams/courseTableForStd.action').text
            r=re.compile('form,"ids","([0-9]+)"',re.M)
            ids=r.findall(Result)
            if (not ids):
                print('无法解析StudentID和ClassID')
                continue
            std_id=ids[0]
            class_id=ids[1]
            print('Student ID: %s'%std_id)
            print('Class ID: %s'%class_id)
            PostData={
                'ignoreHead':'1',
                'setting.kind':'std',
                'startWeek':'',
                'project.id':'1',
                'semester.id':str(SemesterID),
                'ids':std_id
            }
            Result=YZU_JWC.post('http://jwc3.yangtzeu.edu.cn/eams/courseTableForStd!courseTable.action',data=PostData).text
            print(Result[:-100])
            fp=open('D:\\test.txt','w+')
            fp.write(Result)
            fp.close()
            r=re.compile('<tr>([\n\t ]*<td>.*?</td>[\n\t ]*)+</tr>',re.M)
            Courses=r.findall(Result)
            if (not Courses):
                print('本学期无课程')
            else:
                print(Courses)

        else:
            print('Input invalid.')
            continue

if '__main__'==__name__:
    main(MyID,MyPW)
    # print(re.search('\w{8}','"28bd3496-d2a8-4731-8a17-278c170aca23-'))