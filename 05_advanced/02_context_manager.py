"""
    with문 (컨텍스트 매니저)
    - 자원의 획득과 반납을 자동으로 처리하는 제어 구조
    - 블록을 벗어날 때 자동으로 close 처리를 해줌 (직접 f.close() 처리할 필요 X)
"""
# os: 운영체제와 상호작용 하는 모듈
#     파일 경로 탐색, 폴더 생성/삭제, 환경 변수 조회 등을 지원
import os
# json 관련 변환 기능을 제공하는 모듈 (json <--> dict/list)
import json

print("-" * 60)
print(__file__) # C:\workspace\6_Python\05_advanced\02_context_manager.py
# 현재 실행 중인 파이썬 파일의 경로
print("-" * 60)

# os.path.dirname(): 디렉토리(폴더) 경로를 반환
# os.path.abspath(): 절대경로 반환
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)     # C:\workspace\6_Python\05_advanced
print()

# join(): 파이썬의 내장 함수 중 하나
#         여러 개의 경로(폴더, 파일 이름 등)를 운영체제에 맞게 안전하게 이어 붙여줌.
TXT_PATH = os.path.join(BASE_DIR, "_sample.txt")
JSON_PATH = os.path.join(BASE_DIR, "_sameple.json")

"""
# 직접 파일을 처리 (with문 x)
f = open(TXT_PATH, "w", encoding="utf-8")
f.write("금요일, 20260911, 기분이 안 좋다...\n")
f.close()
"""

# with문을 사용하여 파일 처리
print("=" * 60)
print(f"{'with문을 사용하여 파일 처리':^50}")
print("=" * 60)

# mode = "w" --> 파일 쓰기
with open(TXT_PATH, "w", encoding="utf-8") as f:    # f는 지금 열린 파일의 별칭
    f.write("금요일, 20260911, 기분 별로\n")
    f.write("토요일, 20260912, 우울...\n")

# basename(): 전체 경로(Path) 중 마지막에 있는 파일이름만 뽑아주는 함수
print(f"저장 완료: {os.path.basename(TXT_PATH)}")
print()

# mode = "r"  --> 파일 읽기
with open(TXT_PATH,"r", encoding="utf-8") as f:
    contents = f.read()

print(f"{'-------- 파일 내용 --------'}")
print(contents)
print()

print(f"-------- 한 줄씩 읽기 --------")
for line in contents.strip().split("\n"):
    print(line)
    print("-" * 40)


products = [
    {"code": "001123", "name": "iPad (아이패드)", "price": 2000000},
    {"code": "001124", "name": "Galaxy Tab (갤럭시탭)", "price": 1000000},
]

# JSON으로 저장 (파일 쓰기)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    # dump() : 딕셔너리나 리스트 같은 자료구조를 JSON 형식의 문자열로 변환한 뒤,
    #          파일 f에 곧바로 써서 저장해주는 함수
    # ensure_ascii=False : 기본값이 True인데 False로 바꿔야 한글이 유지됨
    # indent=2 : 2칸씩 들여쓰기 해주는 옵션
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"저장 완료 {os.path.basename(JSON_PATH)}")

# # dumps() : 파이썬 데이터를 str로 바꿔주는 함수
# print(f"ensure_ascii=True -> {json.dumps(products, ensure_ascii=True)}")
# print(f"ensure_ascii=False -> {json.dumps(products, ensure_ascii=False)}")
# print()

# JSON 읽기 (파일 읽기)
with open(JSON_PATH, "r", encoding="utf-8") as f:
    json_contents = json.load(f)

print(f"type -> {type(json_contents)}")             # list
for c in json_contents:     
    print(f"data type -> {type(c)}")                # dict => key값으로 접근 가능
    print(f"{c['name']} : {c['price']:,}원")
