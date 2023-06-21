import pyautogui
import os
#출처 https://diplabs.tistory.com/15
pyautogui.position() # 현재 마우스의 포지션을 알려주는 함수
# 1초에 걸쳐 해당 좌료로 이동
pyautogui.move(6706,300,1)
# 마우스를 클릭한채 3초에 걸쳐 이동
pyautogui.dragTo(100,200,3, button='right')
# 즉시 클릭
pyautogui.click(button='right')
# 좌표 설정후 클릭
pyautogui.click(x=100, y=200)
# 더블클릭 간격 설정3
pyautogui.click(x=100, y=200, clicks=2, interval= .2) # double click
# mouse scroll
for i in range(10):
    pyautogui.scroll(100)
#천천히 타이핑 하는 효과
pyautogui.click(button='left')
pyautogui.write('Hello world!', interval= 0.1)

# 확대
pyautogui.keyDown('ctrl')
pyautogui.press('-')
pyautogui.press('-')
pyautogui.keyUp('ctrl')
#screen shot
cwd = os.getcwd()
down_path = cwd + '/'+  'result_file'
img2 = pyautogui.screenshot( os.path.join(down_path,'img2_screenshot.jpg'))
img1 = pyautogui.screenshot( os.path.join(down_path,'img1_region_screenshot.jpg'),
                             region=(100,100,300,400))
# 이렇게 하면 에러나서 아래와 같이 수정하였다, 이유는 RGBA mode 는 jpeg format으로 저장이 안되어  RGB mode로 변경해야

img3 = pyautogui.screenshot(region=(0,0,300,400))
img3 = img3.convert('RGB')
img3.save( os.path.join(down_path,'img3_region_screenshot.jpg'))
