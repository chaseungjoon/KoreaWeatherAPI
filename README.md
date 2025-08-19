    기상청 OpenAPI - 기온, 기압, 운고, 운량, 가시거리 (1분 단위 업데이트)(약 5~7분 딜레이)
    
    NASA FIRMS API - 화재 모니터링 (매일 01시~03시 한번, 13시~14시 한번 업데이트)

    천리안2호 API - 화재 모니터링 (매일 2분마다 업데이트, 10시간 딜레이)

    ***산림청 API - 실시간 산불 정보 (실시간)***

[천리안2호 메타데이터](https://datasvc.nmsc.kma.go.kr/datasvc/html/base/cmm/selectPage.do?page=static.software)

+ **Ambee wildfire API : 유료, 1시간 단위 화재 업데이트**

---

# KFS(산림청) API Endpoint

## 실시간 산불 정보

> 생산주기 : 모름 하지만 실시간 예상
> 
> [웹사이트](http://fd.forest.go.kr/ffas/gis/main.do)

### API Call : 화재 의심 지점의 정보(아래 필드)를 리턴

| 필드 | 의미 |
|------|------|
| `frfrInfoId` | 산불 고유 ID |
| `frfrLctnXcrd` | 산불 발생 경도 (Longitude) |
| `frfrLctnYcrd` | 산불 발생 위도 (Latitude) |
| `frfrSttmnAddr` | 산불 발생 주소 |
| `frfrFrngDtm` | 산불 발생 일시 (`YYYY-MM-DD HH:mm:ss`) |
| `potfrCmpleDtm` | 산불 진화 완료 일시 (`YYYY-MM-DD HH:mm:ss`), 완료 전에는 `null` |
| `frfrPrgrsStcd` | 산불 진행 상태 코드<br>00: 초기 대응<br>01: 산불 1단계<br>02: 산불 2단계<br>03: 산불 3단계<br>05: 삭제/해제 |
| `frfrPrgrsStcdNm` | 산불 진행 상태명 (예: "진화중", "진화완료", "삭제") |
| `frfrStepIssuCd` | 산불 대응 단계 코드<br>00~03: 단계별 대응<br>99: 동원령 해제 |
| `frfrStepIssuNm` | 산불 대응 단계명 (예: "초기진화단계", "산불1단계") |
| `frfrPotfrRt` | 산불 진화율 (%) |

# 천리안2호 인공위성 API

## 인공위성 화재 모니터링 - 기상청 자체 알고리즘

- True Positive 87.17%, False Positive 15.20%

> 생산주기 : 약 2분마다 화재 의심점 업데이트
> 
> 데이터 딜레이 약 10시간 
>
> 위치 : 한반도 전역 및 extended area

### API Call : 화재 의심 지점을 row로 생성 [satellite_data/csv/YYYYMMDDHHMM.csv]

| Column | 예시 값      | 설명                              |
|--------|-----------|---------------------------------|
| lat    | 37.48554  | 화재 탐지 지점의 위도 (도)                |
| lon    | 129.05978 | 화재 탐지 지점의 경도 (도)                |
| FF     | 0,1,2     | 화재 탐지 플래그 (0 : 화재 없음, 1: 화재 있음) |
| DQF_FF | 10.3      | 데이터의 신뢰성 (0~13)                 |

| DQF_FF | 의미                                                       | 
|--------|----------------------------------------------------------|
| 0      | Invalid, outside observation range (SZA above 70 degree) |
| 1      | Invalid, masked area or missing input data               |
| 2      | Land                                                     |
| 3      | Water                                                    |
| 4      | Cloud                                                    |
| 5      | Rejection by cloud test                                  |
| 6      | Rejection by bare soil, urban and water test             |
| 7      | Potential Fire                                           |
| 8      | Fire                                                     |
| 9      | Absolute Fire                                            |
| 10     | Industrial Heat Detection                                |
| 12     | Stability test                                           |
| 13     | Probably Cloud                                           |


# NASA FIRMS API

## 인공위성 화재 모니터링

> 생산주기 : 약 12시간마다 화재 상황 업데이트
> 
> 위치 : 한반도 전역

### API Call : 화재 의심 지점을 row로 생성 [fire_data_MMDDHHMMSS.csv]

| Column                        | 예시 값       | 설명                                  |
|-------------------------------|------------|-------------------------------------|
| latitude                      | 37.48554   | 화재 탐지 지점의 위도 (도)                    |
| longitude                     | 129.05978  | 화재 탐지 지점의 경도 (도)                    |
| frp                           | 10.3       | Fire Radiative Power (메가와트, 화재 강도)  |
| daynight                      | D          | 낮/밤 여부 (D=Day, N=Night)             |
| acq_Date                      | 2025-08-08 | 위성 관측 날짜 (UTC)                      |
| acq_Time                      | 0950       | 위성 관측 시간 (UTC, HHMM 형식)             |
| satellite                     | Terra      | 관측 위성 이름                            |
| instrument                    | MODIS      | 관측 센서 이름                            |
| version                       | 6.1NRT     | 알고리즘 버전 (NRT = Near Real Time)      |
| **(VIIRS_NOAA20_NRT)** confidence | n          | 화재 탐지 신뢰도 (l=low, n=normal, h=high) |
| **(VIIRS_NOAA20_NRT)** bright_ti4 | 331.48     | 4번 밴드 밝기 (Kelvin) - 특정 파장 관측        |
| **(VIIRS_NOAA20_NRT)** bright_ti5 | 302.14     | 5번 밴드 밝기 (Kelvin) - 특정 파장 관측        |
| **(MODIS_NRT)** confidence        | 65         | 화재 탐지 신뢰도 (%)                       |
| **(MODIS_NRT)** brightness        | 313.81     | 화재 픽셀의 밝기 온도(켈빈)                    |
| **(MODIS_NRT)** bright_t31        | 301.66     | 31번 밴드 밝기 (Kelvin) — 특정 파장 관측       |



---

# 기상청 OpenAPI


## 방재기상관측 (AWS)

> 생산주기 : 매 분 (3분정도 delay존재)
> 
> 위치 : 전국 510지점 (grid.csv 에 지점정보 저장)

---

## EndPoints

### 1. AWS 매분자료 [AWS_MMDDHHMMSS.csv]

* 풍향, 풍속 - 1분 평균/10분 평균/최대 순간 
* 기온 - 1분 평균
* 강수 - 강수감지/(15분,60분,12시간, 일) 누적 강수량
* 상대습도, 현지기압, 해면기압 - 1분 평균
* 이슬점온도

| Index     | 설명 | 단위 / 범위 |
|-----------|------|-------------|
| WD1       | 1분 평균 풍향 | degree (0-N, 90-E, 180-S, 270-W, 360-무풍) |
| WS1       | 1분 평균 풍속 | m/s |
| WDS       | 최대 순간 풍향 | degree |
| WSS       | 최대 순간 풍속 | m/s |
| WD10      | 10분 평균 풍향 | degree |
| WS10      | 10분 평균 풍속 | m/s |
| TA        | 1분 평균 기온 | °C |
| RE        | 강수감지 | 0: 무강수, 0이 아니면: 강수 |
| RN-15m    | 15분 누적 강수량 | mm |
| RN-60m    | 60분 누적 강수량 | mm |
| RN-12H    | 12시간 누적 강수량 | mm |
| RN-DAY    | 일 누적 강수량 | mm |
| HM        | 1분 평균 상대습도 | % |
| PA        | 1분 평균 현지기압 | hPa |
| PS        | 1분 평균 해면기압 | hPa |
| TD        | 이슬점온도 | °C |

---

### 2. AWS 운고 운량 [AWS_cloud_MMDDHHMMSS.csv]

* (하,중,상)층 운고, 전운량

| Index   | 설명     | 단위 | 비고                    |
|---------|----------|------|-------------------------|
| CH_LOW  | 하층 운고 | m    | 7620m 이면 구름없음     |
| CH_MID  | 중층 운고 | m    | -                       |
| CH_TOP  | 상층 운고 | m    | -                       |
| CA_TOT  | 전운량   | %    | -                       |

---

### 3. AWS 초상온도 (1분 평균) [AWS_temp_MMDDHHMMSS.csv]


* 기온, 이슬점온도, 초상온도, 지면온도
* 상대습도
* 지중온도 (5cm, 10cm, 20cm, 30cm, 50cm, 1.0m, 1.5m, 3.0m, 5.0m)
* 현지기압, 해면기압

| Index   | 설명              | 단위 | 비고                          |
|---------|-------------------|------|-------------------------------|
| TA      | 1분 평균 기온      | °C   | -                             |
| HM      | 1분 평균 상대습도  | %    | -                             |
| TD      | 1분 평균 이슬점온도| °C   | -                             |
| TG      | 1분 평균 초상온도  | °C   | -                             |
| TS      | 1분 평균 지면온도  | °C   | -                             |
| TE0.05  | 1분 평균 5cm 지중온도 | °C | -                             |
| TE0.1   | 1분 평균 10cm 지중온도| °C | -                             |
| TE0.2   | 1분 평균 20cm 지중온도| °C | -                             |
| TE0.3   | 1분 평균 30cm 지중온도| °C | -                             |
| TE0.5   | 1분 평균 50cm 지중온도| °C | -                             |
| TE1.0   | 1분 평균 1.0m 지중온도| °C | -                             |
| TE1.5   | 1분 평균 1.5m 지중온도| °C | -                             |
| TE3.0   | 1분 평균 3.0m 지중온도| °C | -                             |
| TE5.0   | 1분 평균 5.0m 지중온도| °C | -                             |
| PA      | 1분 평균 현지기압   | hPa  | -                             |
| PS      | 1분 평균 해면기압   | hPa  | -                             |
| *       | 관측값 -50 이하일 경우 관측 없음 또는 에러 처리 | - | 지중온도는 일부 지점만 관측됨 |

---

### 4. AWS 시정자료 (가시거리) [AWS_vis_MMDDHHMMSS.csv]

* 가시거리 (1분/10분평균)
* 안개 (현천)

| Index  | 설명                    | 단위 / 비고                          |
|--------|-------------------------|------------------------------------|
| S      | 장비구분                | 1: 안개관측망(먼저 설치), 2: 첨단화장비 |
| VIS1   | 1분 평균 시정           | m (샘플링 1초 간격, 첨단화장비)    |
| VIS10  | 10분 평균 시정          | m (안개관측망에서만 있음)           |
| WW1    | 1분 순간 현천 (코드)    | 샘플링 1초 간격 (첨단화장비)       |
| WW15   | 15분 평균 현천 (코드)   | 안개관측망에서만 있음               |


> 현천 코드 (WW1, WW15) 설명

| 코드 범위   | 의미   |
|-------------|---------|
| 0 ~ 2       | 맑음    |
| 4           | 연무    |
| 10          | 박무    |
| 30          | 안개    |
| 40 ~ 42     | 비      |
| 50 ~ 59     | 안개비  |
| 60 ~ 68     | 비      |
| 71 ~ 76     | 눈      |