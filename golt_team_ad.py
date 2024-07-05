from PIL import Image, ImageDraw, ImageFont

# 이미지 크기 설정
width, height = 800, 600
image = Image.new('RGB', (width, height))

# 배경 설정
draw = ImageDraw.Draw(image)
draw.rectangle([0, 0, width // 2, height], fill=(255, 0, 0))  # 왼쪽 빨강
draw.rectangle([width // 2, 0, width, height], fill=(0, 255, 0))  # 오른쪽 초록

# 플레이어 사진 자리 표시
player_a_photo_area = [(50, 50), (350, 350)]
player_b_photo_area = [(450, 50), (750, 350)]
draw.rectangle(player_a_photo_area, outline='black', width=5)
draw.rectangle(player_b_photo_area, outline='black', width=5)

# 한글 폰트 설정
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 18)
except IOError:
    font = ImageFont.load_default()

# 플레이어 텍스트
player_a_text = "김철수\n- 2020년 PGA 챔피언십 우승\n- 2019년 US 오픈 준우승\n- 2018년 마스터즈 토너먼트 톱 10\n- 2017년 아시안 투어 챔피언\n- 세계 랭킹 5위"
player_b_text = "박영희\n- 2021년 LPGA 챔피언십 우승\n- 2020년 브리티시 오픈 준우승\n- 2019년 US 오픈 톱 5\n- 2018년 KLPGA 대상 수상\n- 세계 랭킹 3위"

# 텍스트 위치 설정
player_a_text_position = (50, 370)
player_b_text_position = (450, 370)

# 텍스트 그리기
draw.text(player_a_text_position, player_a_text, fill='white', font=font)
draw.text(player_b_text_position, player_b_text, fill='white', font=font)

# 결과 이미지 저장
image_path = "D:/golf_promo_sample_colored_v2.png"
image.save(image_path)
image.show()

image_path
