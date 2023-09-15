# 导入GUI
from LuoguForm import LuoguForm
# 导入json
import json
# 关闭cmd窗口
import win32console
import win32gui

if __name__ == '__main__':
    win32gui.ShowWindow(win32console.GetConsoleWindow(), 0)
    with open('appsettings.json', 'r', encoding='UTF-8') as fs:
        appsettings = json.load(fs)
    LuoguForm(appsettings).mainloop()