import cv2 as cv
import time
import lib.find as f
import lib.adb_command as adb
import lib.api as api

template_imgs = {
    'title': {'img': 'imgs/title.png', 'pos': (462,285,1129,525)},#html坐标格式(以下简称html);标题界面
    #'policy': {'img': 'imgs/agree.png', 'pos': (600, 430, 200, 100)},#TODO:html;隐私政策界面
    'update': {'img': 'imgs/download.png', 'pos': (821,542,1193,618)},#html;更新界面
    'alert': {'img': 'imgs/alert_close.png', 'pos': (1215,1,1600,269)},#html;公告界面的关闭
    'got':{'img': 'imgs/got.png', 'pos': (757,38,847,131)},#html;获得物品界面
    'checkin':{'img': 'imgs/checkin.png', 'pos': (995,124,903,45)},#html;每日初次登录的签到界面
    'login': {'img': 'imgs/login.png', 'pos': (175,0,1077,667)},#html
    'menu': {'img': 'imgs/main_menu_checker.png', 'pos': (157,560,1501,696)},#html;主界面
    'notmenu': {'img': 'imgs/go_back_1.png', 'pos': (0,0,225,94)},#html;白色的返回键
    'notmenu2': {'img': 'imgs/go_back_2.png', 'pos': (0,0,225,94)},#html;黑色的返回键
    'win':{'img': 'imgs/VICTOR.png', 'pos': (927,33,1364,293)},#html;作战胜利界面
    'confirm':{'img': 'imgs/confirm.png', 'pos': (612,458,1596,724)},#html;管他是啥呢，确认就完了！
}

def where_am_i():
    adb.is_game_on()
    max_val = 0
    max_template_name = ''
    screen = cv.imread(api.get_screen_shot())
    screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    t=0
    for template_name, template_info in template_imgs.items():
        #用于处理从 https://www.image-map.net 框出来的坐标
        x1,y1,x2,y2 = template_info['pos']
        if x2<x1:
            a=x2
            x2=x1
            x1=a
        if y2<y1:
            a=y2
            y2=y1
            y1=a
        w=x2-x1
        h=y2-y1
        img = cv.imread(template_info['img'])
        template_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        screen_gray_cropped = screen_gray[y1:y1+h, x1:x1+w]
        result = cv.matchTemplate(screen_gray_cropped, template_img, cv.TM_CCOEFF_NORMED)
        if cv.minMaxLoc(result)[1] > max_val:
            max_val = cv.minMaxLoc(result)[1]
            max_template_name = template_name
            # 获取匹配结果矩阵中最大值的位置
            _, max_val, _, max_loc = cv.minMaxLoc(result)
            # 获取模板图像的宽度和高度
            tw, th = template_img.shape[::-1]
            # 在匹配到的目标上画一个矩形框
            cv.rectangle(screen, (x1 + max_loc[0], y1 + max_loc[1]), (x1 + max_loc[0] + tw, y1 + max_loc[1] + th), (0, 0, 255), 2)
    if max_val < 0.6:
        print('未匹配到任何模板图像')
        print(max_val,max_template_name)
        return None
    else:
        print(f'匹配到了{max_template_name}')
        # 将结果保存到cache/result.png文件中
        cv.imwrite('cache/result.png', screen)
        return max_template_name

def to_menu():
    start_time = time.time()
    while True:
        status = where_am_i()
        if status is None:
            if time.time() - start_time > 180: #这样写不好，万一出下载时间过久就会直接退出应该检验一下是不是在loading或者应用在更新
                print('启动超时')
                time.sleep(1)
                break
            else:
                #print('似乎正在启动')
                time.sleep(1)
        elif status == 'login':
            print('登陆界面还没写')
            break
        elif status == 'title':
            #等待,开始键应该能出现了
            time.sleep(1.5)
            #标题界面点开始
            adb.touch([791,670])
            time.sleep(1)
        elif status == 'got':
            #获得界面瞎点一下(不点到物品就行)
            adb.touch([799,247])
            time.sleep(1)
        elif status == 'checkin':
            #签到界面瞎点一下
            adb.touch([103,73])
            time.sleep(1)
        elif status == 'alert':
            #能关的界面点关闭
            xy=f.cut_find_html('imgs/alert_close',1215,1,1600,269,False)
            adb.touch(xy)
            time.sleep(1)
        elif status == 'update':
            print('开始更新！重新计时')
            start_time = time.time()
            #更新界面点下载(切换到1600*900以来还没用过)
            adb.touch([1007,576])
            time.sleep(1)
        elif status == 'notmenu2': #在签到界面点返回键竟然能给到签了，神奇
            print('action:notmenu2')
            #返回
            adb.touch([60,58])
            time.sleep(1)
        elif status == 'notmenu':
            print('action:notmenu')
            #返回
            adb.touch([60,57])
            time.sleep(1)
        elif status == 'nothome':
            print('action:nothome')
            #返回菜单
            adb.touch([177,58])
            time.sleep(1)
        elif status == 'confirm':
            print('action:confirm')
            #管他是啥呢，确认就完了！
            adb.touch(f.cut_find_html('imgs/confirm',612,458,1596,724,False))
            cv.imwrite('cache/confirm.png', cv.imread('cache/screenshot.png'))
            print('已将确认内容保存至cache/confirm.png')
            time.sleep(1)

        elif status == 'menu':
            print('已在主菜单')
            break    

def to_title(autologin=True):
    start_time = time.time()
    while True:
        status = where_am_i()
        if status is None:
            if time.time() - start_time > 180: #这样写不好，万一出下载时间过久就会直接退出应该检验一下是不是在loading或者应用在更新
                print('启动超时')
                time.sleep(1)
                break
            else:
                #print('似乎正在启动')
                time.sleep(1)
        elif status == 'title':
            #标题界面
            print('到达标题界面，本次导航结束')
            break
        elif status == 'login':
            if autologin:
                print('尝试自动登录')
                out=f.cut_find_html('imgs/login_back',572,234,654,295,False)
                if out is not None:
                    adb.touch(out)
                    time.sleep(1)
                adb.touch([804,525])
                time.sleep(1)
            else:
                print('到达登陆界面')
            break
        elif status == 'got':
            #获得界面瞎点一下(不点到物品就行)
            adb.touch([799,247])
            time.sleep(1)
        elif status == 'checkin':
            #签到界面瞎点一下
            adb.touch([103,73])
            time.sleep(1)
        elif status == 'alert':
            #能关的界面点关闭
            xy=f.cut_find_html('imgs/alert_close',1215,1,1600,269,False)
            adb.touch(xy)
            time.sleep(1)
        elif status == 'update':
            print('开始更新！重新计时')
            start_time = time.time()
            #更新界面点下载(切换到1600*900以来还没用过)
            adb.touch([1007,576])
            time.sleep(1)
        elif status == 'notmenu2': #在签到界面点返回键竟然能给到签了，神奇
            print('action:notmenu2')
            #返回
            adb.touch([60,58])
            time.sleep(1)
        elif status == 'notmenu':
            print('action:notmenu')
            #返回
            adb.touch([60,57])
            time.sleep(1)
        elif status == 'nothome':
            print('action:nothome')
            #返回菜单
            adb.touch([177,58])
            time.sleep(1)
        elif status == 'confirm':
            print('action:confirm')
            #管他是啥呢，确认就完了！
            adb.touch(f.cut_find_html('imgs/confirm',612,458,1596,724,False))
            cv.imwrite('cache/confirm.png', cv.imread('cache/screenshot.png'))
            print('已将确认内容保存至cache/confirm.png')
            time.sleep(1)
        elif status == 'menu':
            adb.touch(f.cut_find_html('imgs/menu',44,616,157,730,False))
            time.sleep(1.5)
            adb.touch(f.cut_find_html('imgs/setting',82,565,520,794))
            time.sleep(1.5)
            adb.touch((1096,656))
            time.sleep(1.5)
            adb.touch((1011,532))
            break

def to_login():
    to_title()
    time.sleep(1.5)
    adb.touch(f.cut_find_html('imgs/title_exit',1502,778,1573,867))
    time.sleep(1)
    adb.touch(f.cut_find_html('imgs/confirm',612,458,1596,724))   

def to_fight():
    to_menu()
    adb.touch(f.find('imgs/enter_the_show'))
    print("正在进入主会场")
