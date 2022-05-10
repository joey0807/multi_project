# multi_project

## 1차 프로젝트

- 프로젝트 목표

  - 제무제표 데이터를 통해 기업 펀더멘털 분석에 필요한 파생 지표를 도출한 후 그래프로 시각화

  - 도출한 결과물을 가지고 기업의 재무상태가 건전한지 결론을 도출

- 주제 선정 이유
  - DART-FSS에서 API를 통해 양질의 RawData를 제공받음
  - 파생 지표를 구하는 공식이 잘 알려져 있어 도메인 지식이 없어도 지표를 계산해 낼 수 있음
  - 표에서 필요한 값을 찾기만 하면 됨

- 맡은 기업 : Nexon
  - RawData를 정제하여 파생지표를 도출
  - 파생 지표를 시각화 후 결론 도출
- 사용한 도구들
  - 사용 언어 
    - python
  - 패키지 
    - pandas
    - matplotlib
    - seaborn
  - API
    - DART
  - IDE
    - Google Colab
    - Google Docs
- 분석 사례
  - 안정성
  - 수익성
  - 성장성

## 2차 프로젝트

- 프로젝트 목표
  - 날씨 데이터와 주식 데이터의 정제 후 그래프로 시각화
  - 날씨의 상태와 주식 간의 상관관계가 있는지 확인
- 주제 선정 이유
  - 행동투자론 : 주식을 구매하는데 있어, 이성적 판단에 근거하지 않고 날씨, 기분 등이 소비자의 심리에 영향을 끼쳐 주식을 구매한다는 이론
  - 행동투자론의 확인
- 사용 데이터
  - 주가 데이터
    - KOSIS(국가통계포털)-주식시장(일별)
  - 기온, 습도, 흐림, 강수량, 태풍 데이터
    - 기상청
- 사용한 도구들
  - 사용 언어
    - python
  - 패키지
    - pandas
    - matplotlib
    - seaborn
  - IDE
    - Google Colab

- 데이터 분석
  - 기온(최고 기온)
  - 불쾌지수
  - 전운량
  - 태풍
  - 주식
    - KOSPI
    - KOSDAQ

## 3차 프로젝트

- 프로젝트 목표
  - 음식이미지 인식을 통한 헬스케어 서비스 개발
- 주제 선정 이유
  - 요즘은 건강에 대해 관심이 많은 시대
  - 하지만 매일 식단을 기록하는 것은 쉽지 않은 일
  - 그래서 영양 섭취를 편리하게 추적하고 관리할 수 있는 서비스를 개발하고자 했음

- 사용한 도구들
  - 음식 검출 모델 개발
    - Google Colab Pro
    - roboflow
    - PyTorch
    - Weights & Biases
    - Google Drive
  - 데이터 수집
    - AI Hub
      - 음식 이미지 및 영양정보 텍스트
      - 한국인 다빈도 섭취 외식메뉴와 한식메뉴 400종
      - 720,000개 이미지, txt, XML
  - 백엔드
    - python
    - Flask
    - REST API
    - MySQL
    - amazon EC2
