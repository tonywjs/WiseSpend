# 소비 유형 분석 및 캐릭터 생성 서비스

## 📝 프로젝트 개요

은행에서 다운로드한 소비 지출 내역 엑셀 또는 CSV 파일을 업로드하면,
- GPT가 소비 패턴을 분석하여 16가지 소비 유형 중 하나를 제안하고,
- 해당 유형에 맞는 캐릭터 이미지를 보여주는 서비스입니다.
- GPT는 소비 유형과 함께 상세한 분석 내용과 개선 조언을 제공합니다.

## ⚡ 주요 기능

- 엑셀 파일(.xlsx) 및 CSV 파일(.csv) 업로드
- GPT API를 활용한 심층 소비 패턴 분석
- 16가지 소비 유형 분류 (소비 정밀 검사자, 욜로 개척자, 할인 추적자 등)
- 소비 유형에 맞는 캐릭터 이미지 매칭 및 표시
- 맞춤형 소비 개선 조언 제공
- 지출 패턴 분석 결과 시각화

## 🛠️ 사용 기술

- Python
- Streamlit
- Pandas
- OpenAI API (GPT-4)
- Pillow (이미지 처리)

## 📂 프로젝트 구조

```
app.py                  # 메인 애플리케이션 파일
src/                    # 소스 코드 폴더
    LLM_interface.py    # GPT API 연동 및 분석 로직
/images/                # 캐릭터 이미지 폴더
    욜로 개척자.png      # 욜로 개척자 캐릭터
    할인 추적자.png      # 할인 추적자 캐릭터
    yolo.png            # YOLO 캐릭터 (영문버전)
    discount.png        # 할인 추적자 캐릭터 (영문버전)
    title.png           # 타이틀 이미지
requirements.txt        # 필요 패키지 목록
```

## 🚀 실행 방법

1. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

2. OpenAI API 키 설정
   - 애플리케이션 실행 후 '설정' 탭에서 API 키를 입력하거나
   - Streamlit 설정 파일(secrets.toml)에 `OPENAI_KEY` 설정

3. Streamlit 앱 실행

```bash
streamlit run app.py
```

4. 브라우저에서 localhost 링크로 접속합니다.

## ✨ 사용자 플로우

1. 첫 화면은 엑셀/CSV 파일 업로드 영역만 표시됩니다.
2. 파일을 업로드하고 '분석 시작' 버튼을 클릭하면 분석이 진행됩니다.
3. 분석 중 프로그레스 바가 표시되며, 완료 후 결과 화면으로 전환됩니다.
4. 결과 화면에서는 16가지 소비 유형 중 하나와 캐릭터, GPT의 상세 분석 내용을 확인할 수 있습니다.

## 🔧 설정

- '설정' 탭에서 OpenAI API 키를 입력할 수 있습니다.
- 시스템 프롬프트를 커스터마이징하여 분석 방향을 조정할 수 있습니다.

## 📊 소비 유형

분석 결과 다음 16가지 소비 유형 중 하나로 분류됩니다:

1. 소비 정밀 검사자 - #디테일장인 #계획소비 #진지소비
2. 욜로 개척자 - #YOLO #욜로러 #인생개척
3. 할인 추적자 - #할인헌터 #쿠폰수집가 #세일탐정
4. 충동 탐험가 - #충동구매 #탐험가 #질주러
5. 생존형 저축가 - #적금모드 #짠내러 #생존플랜
6. 무계획 방랑자 - #방랑러 #무계획 #즉흥삶
7. 안전 지향자 - #안전제일 #플렉스제한 #조심조심
8. 무심한 관리자 - #쿨한관리 #무심테크 #대충성공
9. 목표 달성자 - #목표달성 #미션성공 #계획소비러
10. 기분파 소비자 - #감성쇼핑 #플렉스조아 #갬성러버
11. 효율 추구자 - #가성비맛집 #효율러 #짠돌이생활
12. 실험 소비자 - #체험러 #경험수집 #인증필수
13. 책임 소비자 - #진지소비 #선택잘함 #소비엄선러
14. 감성 소비자 - #감성캐쳐 #느낌좋아 #갬성BGM필수
15. 균형 잡힌 소비자 - #지출저축밸런스 #균형잡힌삶 #프로조절러
16. 자유로운 영혼 - #자유영혼 #플렉스 #여행은생명

## 📌 추가 개선 예정사항

- 더 다양한 캐릭터 디자인 추가
- 소비 패턴 시각화 기능 강화
- 소비 분석 히스토리 저장 기능
- 결과 저장 및 공유 기능 추가
- 모바일 UI 최적화

---

# 한 줄 요약
**Streamlit + GPT로 소비 내역 파일을 업로드하면 16가지 소비유형으로 분석하고 맞춤형 조언까지 제공!** 🚀
