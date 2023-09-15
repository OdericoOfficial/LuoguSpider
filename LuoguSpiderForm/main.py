# 导入GUI
from LuoguForm import LuoguForm
# 导入json
import json

if __name__ == '__main__':
    with open('appsettings.json', 'r', encoding='UTF-8') as fs:
        appsettings = json.load(fs)
    LuoguForm(appsettings).mainloop()