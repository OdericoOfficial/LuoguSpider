# 导入selenium
import tkinter
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# 导入线程池
from concurrent.futures import ThreadPoolExecutor
import threading
import concurrent.futures as concurrent
# 导入工具库
import time
import random
import sqlite3
import os
from html2text import HTML2Text
# 导入ocr
import ddddocr
import numpy as np

__luoguProblemPath = 'https://www.luogu.com.cn/problem/'
__luoguSolutionPath = 'https://www.luogu.com.cn/problem/solution/'
__luoguListPath = 'https://www.luogu.com.cn/problem/list?page='
__luoguAuthPath = 'https://www.luogu.com.cn/auth/login'

OnSpiderCompleting = []
OnSpiderCompleted = []

def ProblemSpider(account, password, savePath, edgePath, gpu, threads, cookies = None):
    # 创建锁
    lock = threading.Lock()
    
    # 获取cookies
    if cookies == None:
        cookies = __getCookiesByOcr(account, password, edgePath, gpu)
    tkinter.messagebox.showinfo(message='登录完成')
    
    # 创建数据库
    dbPath = os.path.join(savePath, 'luogu.db')
    __createTable(dbPath)
    
    start = 1000
    adder = int(50 / threads)
    distance = 50 - adder * threads
    # 启动线程池
    with ThreadPoolExecutor() as task:
        for i in range(0, threads):
            task.submit(__spiderTask, start, adder, savePath, edgePath, dbPath, cookies, lock)
            start += adder
        if distance > 0:
            task.submit(__spiderTask, start, distance, savePath, edgePath, dbPath, cookies, lock);
            
def __createTable(dbPath):
    connect = sqlite3.connect(dbPath)
    connect.execute(
        """CREATE TABLE LuoguProblem (
        Id TEXT PRIMARY KEY,
        Title TEXT,
        Difficulty TEXT,
        Keywords TEXT,
        ProblemHtml TEXT,
        SolutionHtml TEXT)""")
    connect.commit()
    connect.close()
    
def __insertLine(problemDict, dbPath):
    connect = sqlite3.connect(dbPath)
    connect.execute("INSERT INTO LuoguProblem (Id, Title, Difficulty, Keywords, ProblemHtml, SolutionHtml) VALUES (?, ?, ?, ?, ?, ?)",
                    (problemDict.get('Id'), problemDict.get('Title'), problemDict.get('Difficulty'),
                        problemDict.get('Keywords'), problemDict.get('ProblemHtml'), problemDict.get('SolutionHtml')))
    connect.commit()
    connect.close()
    
def __getCookiesByOcr(account, password, edgePath, gpu):
    # 打开登录网站并等待加载
    driver = __getHeadLessDriver(edgePath)
    driver.get(__luoguAuthPath)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[3]/div/div[2]/img')))
    time.sleep(random.uniform(3, 5))

    # 获取元素
    accountInput = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[1]/div/input')
    passwordInput = driver.find_element(By.XPATH, '/html/body/div/div[2]/main/div/div/div/div/div/div/div[2]/div/input')
    captureInput = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[3]/div/div[1]/input')
    captureImage = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[3]/div/div[2]/img')

    # 截图保存验证码
    if os.path.exists('temp.png'):
        os.remove('temp.png')
    captureImage.screenshot('temp.png')
    
    ocr = ddddocr.DdddOcr(gpu)
    with open("temp.png", 'rb') as fs:
        capture = fs.read()
        
    # 将识别后的验证码4位数存储进result变量
    result = ocr.classification(np.resize(capture, (1, 19)))
 
    # 输入账号、密码、验证码
    accountInput.click()
    accountInput.send_keys(account)
    passwordInput.click()
    passwordInput.send_keys(password)
    captureInput.click()
    captureInput.send_keys(result)
    
    # 登录并等待登录
    captureInput.send_keys(Keys.ENTER)
    time.sleep(random.uniform(2, 3))

    count = 0    
    okBtn = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[3]/button[1]')
    while len(okBtn) != 0 and count < 10:
        okBtn[0].click()
        captureImage.click()
        
        # 截图保存验证码
        if os.path.exists('temp.png'):
            os.remove('temp.png')
        captureImage.screenshot('temp.png')

        with open("temp.png", 'rb') as fs:
            capture = fs.read()
        
        # 将识别后的验证码4位数存储进result变量
        result = ocr.classification(np.resize(capture, (1, 19)))
        
        captureInput.click()
        captureInput.send_keys(result)
        
        # 登录并等待登录
        captureInput.send_keys(Keys.ENTER)
        time.sleep(random.uniform(2, 3))

        okBtn = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[3]/button[1]')    
        count += 1

    if count >= 10:
        raise ValueError('登录失败,如果确定账号密码无误,那么就是验证码错误了,\n这个ocr包比较简单,可以多尝试几次QAQ')

   # 返回cookies
    cookies = []
    for cookie in driver.get_cookies():
        cookies.append(cookie)
    driver.quit()
    return cookies;

def __getHeadLessDriver(edgePath):
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"')
    options.binary_location = edgePath
    driver = webdriver.Edge(options = options)
    return driver

def __internalTask(problemId, savePath, driver, dbPath, cookies, lock):
    # 获取两个页面的soup,早关闭driver省一些http次数占用
    problemSoup = __problemTask(driver, problemId)
    solutionSoup = __solutionTask(driver, problemId, cookies)

    # 获取两个页面的信息
    problemDict = __solveProblemTask(problemSoup)
    problemDict['SolutionHtml'] = __solveSolutionTask(solutionSoup)

    # 拼接文件名
    problemDict['Id'] = problemId
    problemFileName = f"{problemId}-{problemDict['Title']}.md"
    solutionFileName = f"{problemId}-{problemDict['Title']}-题解.md"
    problemDirName = f"{problemId}-{problemDict['Title']}"
    difficultDirName = f"{problemDict['Difficulty']}-{problemDict['Keywords']}"

    # 创建位置
    difficultDir = os.path.join(savePath, difficultDirName)
    if not os.path.exists(difficultDir):
        os.mkdir(difficultDir)
        
    problemDir = os.path.join(difficultDir, problemDirName)
    if not os.path.exists(problemDir):
        os.mkdir(problemDir)
    
    h2t = HTML2Text()

    # 写入文件
    problemFile = os.path.join(problemDir, problemFileName)
    if not os.path.exists(problemFile):
        with open(problemFile, 'w', encoding='utf-8') as fs:
            fs.write(h2t.handle(problemDict['ProblemHtml']))

    solutionFile = os.path.join(problemDir, solutionFileName)
    if not os.path.exists(solutionFile):
        with open(solutionFile, 'w', encoding='utf-8') as fs:
            fs.write(h2t.handle(problemDict['SolutionHtml']))
    
    with lock:
        __insertLine(problemDict, dbPath)
        for event in OnSpiderCompleted:
            event(problemId)
            
    time.sleep(random.uniform(2, 3))

def __solutionTask(driver, problemId, cookies):
    # 打开题解页面
    driver.get(__luoguSolutionPath + problemId)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/main/div/section[2]/div/div[2]/div/div[1]')))
    time.sleep(random.uniform(2, 3))
    
    # 获取html文本
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    return soup

def __solveSolutionTask(soup):
    # 获取题解
    mainContainer = soup.find('section', class_ = 'main').find('div', 'block')
    fristSolution = mainContainer.find('div', class_ = 'row-wrap').find_all('div', class_ = 'item-row')[0]
    solution = fristSolution.find('div', class_ = 'main')
    return str(solution)

def __problemTask(driver, problemId):
    # 打开题目页面
    driver.get(__luoguProblemPath + problemId)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/main/div/section[1]/div[1]/div/div[2]/span[2]')))
    time.sleep(random.uniform(2, 3))
    
    # 点击'查看算法标签'
    findKeywords = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/section[1]/div[2]/div[2]')
    ActionChains(driver).move_to_element(findKeywords).click().perform()
    
    # 获取html文本
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    return soup    

def __solveProblemTask(soup):
    # 获取难度，把'/'换成' '防止路径问题
    row = soup.find('div', class_ = 'info-rows').find_all('div')[1]
    difficulties = row.find('a', class_ = 'color-none').find('span').text.strip().split('/')
    difficulty = ' '.join(difficulties)
    
    # 获取问题
    mainContainer = soup.find('section', class_ = 'main').find('div', class_ = 'card problem-card padding-default').find_all('div')[1]
    problem = str(mainContainer)
    
    # 获取标题
    title = soup.find('h1', class_ = 'lfe-h1').find('span')['title']
    
    # 获取标签
    keywords = []
    sideCard = soup.find('section', class_ = 'side').find_all('div', class_ = 'card padding-default')[1]
    keyContainer = sideCard.find('div', class_ = 'tags-wrap multiline')
    for item in keyContainer.find_all('span'):
        keywords.append(item.text.strip())
    
    return { 'Id': '',
             'Title': title,
             'Difficulty': difficulty,
             'Keywords': ' '.join(keywords),
             'ProblemHtml': problem,
             'SolutionHtml': ''}
    
def __spiderTask(start, adder, savePath, edgePath, dbPath, cookies, lock):
    try:
        path = 'https://www.luogu.com.cn/'
        driver = __getHeadLessDriver(edgePath)
        driver.get(path)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(path)
    
        for i in range(start, start + adder):
            for event in OnSpiderCompleting:
                event(f'P{str(i)}')
            __internalTask(f'P{str(i)}', savePath, driver, dbPath, cookies, lock)
        driver.quit()
    except Exception as e:
        tkinter.messagebox.showinfo(message=e)