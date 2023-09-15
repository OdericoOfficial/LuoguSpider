import unittest
from bs4 import BeautifulSoup
import os

class TestSpider(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        with open('TestProblem.txt', 'r', encoding='UTF-8') as fs:
            self.problemHtml = BeautifulSoup(''.join(fs.readlines()), features="lxml")
        with open('TestSolution.txt', 'r', encoding='UTF-8') as fs:
            self.solutionHtml = BeautifulSoup(''.join(fs.readlines()), features="lxml")
        super().__init__(methodName)
    
    def test_solve_soultion(self):
        b1 = self.solutionHtml.find('section', class_ = 'main')
        self.assertFalse(b1 == None)
        b2 = b1.find('div', 'block')
        self.assertFalse(b2 == None)
        b3 = b2.find('div', class_ = 'row-wrap')
        self.assertFalse(b3 == None)
        b4 = b3.find_all('div', class_ = 'item-row')
        self.assertFalse(len(b4) == 0)
        b5 = b4[0].find('div', class_ = 'main')
        self.assertFalse(b5 == None)
    
    def test_sovle_problem(self):
        b1 = self.problemHtml.find('div', class_ = 'info-rows')
        self.assertFalse(b1 == None)
        b2 = b1.find_all('div')
        self.assertFalse(len(b2) < 2)
        b3 = b2[1].find('a', class_ = 'color-none')
        self.assertFalse(b3 == None)
        b4 = b3.find('span')
        self.assertFalse(b4 == None)

        b5 = self.problemHtml.find('section', class_ = 'main')
        self.assertFalse(b5 == None)
        b6 = b5.find('div', class_ = 'card problem-card padding-default')
        self.assertFalse(b6 == None)
        b7 = b6.find_all('div')
        self.assertFalse(len(b7) < 2)

        b8 = self.problemHtml.find('h1', class_ = 'lfe-h1')
        self.assertFalse(b8 == None)
        b9 = b8.find('span')
        self.assertFalse(b9 == None)
        
        b10 = self.problemHtml.find('section', class_ = 'side')
        self.assertFalse(b10 == None)
        b11 = b10.find_all('div', class_ = 'card padding-default')
        self.assertFalse(len(b11) < 2)
        b12 = b11[1].find('div', class_ = 'tags-wrap multiline')
        self.assertFalse(b12 == None)