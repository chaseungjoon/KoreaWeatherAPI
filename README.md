# Korea Weather API

Collects weather observations and disaster data as CSV files. [한국어](README_kor.md)

## Contents

- [Fetching data](#fetching-data)
- [Monitored hazards](#monitored-hazards)
- [Data sources](#data-sources)
- [Korea Forest Service (KFS)](#1-korea-forest-service-kfs)
- [Korea Meteorological Administration (KMA)](#2-korea-meteorological-administration-kma)
- [Ministry of Environment (MOE)](#3-ministry-of-environment-moe)
- [NASA FIRMS](#4-nasa-firms-api)

## Fetching data

The `*_data/` directories contain only a few example snapshots, not a complete archive. Install dependencies with `pip install -r requirements.txt`, then set the required API keys as environment variables (see `src/config.py`). Call collectors in `src/api/` to fetch more data.

```bash
PYTHONPATH=. python -c "from src.api.nasa_api import get_firms_data; get_firms_data(5)"
```

This fetches the previous five days of FIRMS data (`NASA_FIRMS_MAP_KEY` required). For specific dates, change `inqDt` in `src/api/kfs_api.py`, `time` or `date` in `src/api/kma_api.py`, or `ymdhm` in `src/api/moe_api.py`. AWS and real-time wildfire calls request the latest data; historical availability depends on each provider.

## Monitored hazards

- Wildfire — KFS real-time wildfire API
- UV exposure — KMA living weather index API
- Flood — MOE real-time flood API
- Landslide — KFS landslide forecast API
- Heavy snow — data source not specified
- Fog — KMA AWS minute visibility API

## Data sources

### Weather observations

#### KMA OpenAPI

- **Data:** temperature, pressure, cloud height and cover, visibility
- **Update interval:** one minute (approximately 5–7 minutes of publication delay)

### UV observations

#### KMA OpenAPI

- **Data:** regional UV index forecasts up to 75 hours ahead
- **Update interval:** eight times daily, every three hours (00:00, 03:00, …, 21:00)

### Fire monitoring

#### KFS API

- **Update interval:** real time, when a fire is reported

#### NASA FIRMS API

- **Update interval:** twice daily (01:00–03:00 and 13:00–14:00)

#### GK2A API

- **Update interval:** every two minutes (approximately 10 hours of publication delay)
- **Reference:** [GK2A metadata](https://datasvc.nmsc.kma.go.kr/datasvc/html/base/cmm/selectPage.do?page=static.software)

### Flood monitoring

#### MOE real-time flood API

- **Update interval:** every 10 minutes (approximately five minutes of publication delay)
- **Data:** river levels at 381 sites nationwide and flood risk (caution, warning, severe)
- **Reference:** [Flood Information System](https://n.flood.go.kr/main.do)

#### Flood trace OpenAPI

- **Update interval:** annually, at year-end
- **Data:** flood trace PNGs (124–132°E, 33–39°N)
- **Reference:** [Flood Trace OpenAPI](https://safemap.go.kr/opna/data/dataView.do)
- OpenCV extracts flood trace pixel coordinates into CSV (`safemap_data/csv/*.csv`); error rate: 20%.

### Landslide monitoring

#### KFS landslide forecast API

- **Update interval:** documented as every five minutes (observed updates appear to occur each morning)
- **Data:** forecasts for areas with high landslide probability
- **Reference:** [KFS landslide forecast OpenAPI](https://www.safetydata.go.kr/disaster-data/view?dataSn=696)

## 1. Korea Forest Service (KFS)

### 1-1. Wildfire API (`kfs_data/*.csv`)

#### Real-time wildfire information

- **Production:** updated when a fire is reported
- **Website:** [KFS wildfire GIS](http://fd.forest.go.kr/ffas/gis/main.do)

##### Response fields

| Field | Example | Meaning |
|---|---|---|
| frfrInfoId | 398504 | Unique wildfire incident ID |
| frfrFrngDtm | 2025-08-22 14:41:22 | Fire start time |
| frfrSttmnDt | 20250822 | Report date (YYYYMMDD) |
| frfrSttmnHms | 144122 | Report time (HHMMSS → 14:41:22) |
| frfrSttmnAddr | 충청북도 음성군 감곡면 영산리 | Reported administrative address |
| frfrSttmnAddrDe | 충청북도 음성군 감곡면 영산리 산55-3임 | Detailed address |
| frfrLctnXcrd | 127.67243000000057 | Fire longitude |
| frfrLctnYcrd | 37.08104000024055 | Fire latitude |
| frfrSttmnLctnXcrd | 127.67243000000029 | Reported longitude |
| frfrSttmnLctnYcrd | 37.08104000012027 | Reported latitude |
| lgdngCd | 4377037026 | Administrative area code |
| frfrPrgrsStcd | 02 | Progress status code |
| frfrPrgrsStcdNm | 진화중 | Progress status (firefighting in progress) |
| frfrPotfrRt | 70 | Containment rate (%) |
| frfrStepIssuCd | 00 | Response stage code |
| frfrStepIssuNm | 초기 대응 | Response stage (initial response) |
| frfrOccrrTpcd | 05 | Incident type code (lookup needed) |
| frfrOccrrStcd | 31 | Detailed cause code (lookup needed) |

### 1-2. Fire warning API (`kfs_data/warning_list/*.csv`)

#### Real-time wildfire warning areas

- **Production:** every 24 hours (morning update)
- **Website:** [KFS wildfire GIS](http://fd.forest.go.kr/ffas/gis/main.do)

##### Response fields

| Field | Example | Meaning |
|---|---|---|
| AREA | 영덕군 | City/county/district |
| AREA_ENG | Yeongdeok-gun | English city/county/district name |
| LOCATION | 경상북도 영덕군 | Full address (province + city/county/district) |
| WARNING_LEVEL | 관심 | Fire warning level (attention) |
| DATE | 2025-09-02 11:00 | Warning issue time |
| LAST_UPDATED | 2025-09-02 01:15:59 | Last update time |
| PROVINCE_CODE | 47 | Province code |
| CITY_CODE | 770 | City code |

### 1-3. Landslide API (`kfs_data/landslide/*.csv`)

#### Real-time landslide forecasts

- **Production:** every five minutes

#### Request parameters

| Parameter | API name | Type | Size | Required | Description |
|---|---|---|---|---|---|
| Service key | serviceKey | STRING | 50 | Yes | API service key |
| Rows per page | numOfRows | NUMBER | 30 | No | Rows per page |
| Page number | pageNo | NUMBER | 30 | No | Page number |
| Response format | returnType | VARCHAR | 30 | No | JSON or XML |
| Query start date | inqDt | STRING | — | No | YYYYMMDD |

#### Response fields

| Field | API name | Type | Size | Required | Description |
|---|---|---|---|---|---|
| Landslide forecast name | LNLD_FRCST_NM | — | 20 | Yes | Forecast name |
| City/county/district | SGG_NM | — | 100 | Yes | Area name |
| Prediction analysis time | PREDC_ANLS_DT | — | 50 | Yes | Analysis time |

## 2. Korea Meteorological Administration (KMA)

### 2-1. AWS (automated weather stations)

- **Production:** every minute (approximately 3–5 minutes of delay)
- **Stations:** 510 nationwide (see `map_data/grid.csv`)

#### 2-1-1. AWS minute observations (`kma_data/<timestamp>/AWS_*.csv`)

##### Measurements

- Wind direction and speed (one-minute mean, ten-minute mean, maximum gust)
- Air temperature (one-minute mean)
- Precipitation (detection; 15-minute, 60-minute, 12-hour, and daily totals)
- Relative humidity
- Local and sea-level pressure
- Dew point

| Index | Meaning | Unit / range |
|---|---|---|
| WD1 | One-minute mean wind direction | degrees (0=N, 90=E, 180=S, 270=W, 360=calm) |
| WS1 | One-minute mean wind speed | m/s |
| WDS | Maximum gust direction | degrees |
| WSS | Maximum gust speed | m/s |
| WD10 | Ten-minute mean wind direction | degrees |
| WS10 | Ten-minute mean wind speed | m/s |
| TA | One-minute mean air temperature | °C |
| RE | Precipitation detection | 0=no rain; nonzero=rain |
| RN-15m | 15-minute accumulated precipitation | mm |
| RN-60m | 60-minute accumulated precipitation | mm |
| RN-12H | 12-hour accumulated precipitation | mm |
| RN-DAY | Daily accumulated precipitation | mm |
| HM | One-minute mean relative humidity | % |
| PA | One-minute mean local pressure | hPa |
| PS | One-minute mean sea-level pressure | hPa |
| TD | Dew point temperature | °C |

#### 2-1-2. AWS cloud height and cover (`kma_data/<timestamp>/AWS_cloud_*.csv`)

##### Measurements

- Low, middle, and upper cloud height
- Total cloud cover

| Index | Meaning | Unit | Note |
|---|---|---|---|
| CH_LOW | Low cloud height | m | 7620 m = no clouds |
| CH_MID | Middle cloud height | m | — |
| CH_TOP | Upper cloud height | m | — |
| CA_TOT | Total cloud cover | % | — |

#### 2-1-3. AWS surface and soil temperature (`kma_data/<timestamp>/AWS_temp_*.csv`)

##### Measurements

- Air, dew point, grass minimum, and ground surface temperature
- Relative humidity
- Soil temperature (5 cm–5 m)
- Local and sea-level pressure

| Index | Meaning | Unit |
|---|---|---|
| TA | One-minute mean air temperature | °C |
| HM | One-minute mean relative humidity | % |
| TD | One-minute mean dew point | °C |
| TG | One-minute mean grass minimum temperature | °C |
| TS | One-minute mean ground surface temperature | °C |
| TE0.05 | Soil temperature at 5 cm | °C |
| TE0.1 | Soil temperature at 10 cm | °C |
| TE0.2 | Soil temperature at 20 cm | °C |
| TE0.3 | Soil temperature at 30 cm | °C |
| TE0.5 | Soil temperature at 50 cm | °C |
| TE1.0 | Soil temperature at 1.0 m | °C |
| TE1.5 | Soil temperature at 1.5 m | °C |
| TE3.0 | Soil temperature at 3.0 m | °C |
| TE5.0 | Soil temperature at 5.0 m | °C |
| PA | One-minute mean local pressure | hPa |
| PS | One-minute mean sea-level pressure | hPa |

Values of −50 or below indicate a missing observation or error. Soil temperature is measured at selected stations only.

#### 2-1-4. AWS visibility (`kma_data/<timestamp>/AWS_vis_*.csv`)

##### Measurements

- Visibility (one-minute and ten-minute mean)
- Fog and present weather

| Index | Meaning | Unit / note |
|---|---|---|
| S | Instrument type | 1=fog network; 2=modernized equipment |
| VIS1 | One-minute mean visibility | m; one-second sampling, modernized equipment |
| VIS10 | Ten-minute mean visibility | m; fog network only |
| WW1 | One-minute instantaneous weather code | one-second sampling, modernized equipment |
| WW15 | 15-minute mean weather code | fog network only |

##### Present weather codes

| Code | Meaning |
|---|---|
| 0–2 | Clear |
| 4 | Haze |
| 10 | Mist |
| 30 | Fog |
| 40–42 | Rain |
| 50–59 | Drizzle |
| 60–68 | Rain |
| 71–76 | Snow |

### 2-2. GK2A satellite API (`GK2A_data/csv/*.csv`)

#### Overview

- **Data:** suspected fire locations, delivered as NetCDF (`.nc`)
- **Production:** approximately every two minutes
- **Data delay:** approximately 10 hours
- **Coverage:** Korean Peninsula and extended area
- **Performance:** true positive 87.17%; false positive 15.20%

##### Response fields

| Column | Example | Meaning |
|---|---|---|
| `lat` | 37.48554 | Fire detection latitude (degrees) |
| `lon` | 129.0597 | Fire detection longitude (degrees) |
| `FF` | 0, 1 | Fire flag (0=no fire; 1=fire) |
| `DQF_FF` | 10 | Data quality flag (0–13) |

##### `DQF_FF` codes

| Code | Meaning |
|---|---|
| 0 | Invalid; outside observation range (SZA > 70°) |
| 1 | Invalid; masked area or missing input |
| 2 | Land |
| 3 | Water |
| 4 | Cloud |
| 5 | Rejected by cloud test |
| 6 | Rejected by bare soil, urban, and water test |
| 7 | Potential fire |
| 8 | Fire |
| 9 | Absolute fire |
| 10 | Industrial heat detection |
| 12 | Stability test |
| 13 | Probably cloud |

### 2-3. Living weather index: UV (`kma_data/uv/*.csv`)

#### Overview

- **Data:** UV index (0 to 11+)
- **Production:** every three hours, eight times daily (00:00, 03:00, …, 21:00)
- **Coverage:** Korean Peninsula

##### Response fields

| Column | Example | Meaning |
|---|---|---|
| areaNo | 110000000 | Administrative area code (see `map_data/korea_administrative_zone_code.csv`) |
| date | 2025090118 | Request time (YYYYMMDDHH) |
| h0–h75 | 8 | UV index `n` hours ahead in field `h<n>` |

##### UV index levels

| Level | Index |
|---|---|
| Extreme | 11+ |
| Very high | 8–10 |
| High | 6–7 |
| Moderate | 3–5 |
| Low | 0–2 |

## 3. Ministry of Environment (MOE)

### 3-1. Real-time flood API (`moe_data/*.csv`)

#### Overview

- **Data:** river levels and flood risk (caution, warning, severe)
- **Production:** every ten minutes (approximately five minutes of delay)
- **Coverage:** 381 sites nationwide

#### Response fields

| Column | Meaning | Example |
|---|---|---|
| lon | Longitude | 128.27 |
| lat | Latitude | 35.728 |
| obsnm | Observation site / bridge | 고령군(회천교) |
| ymdhm | Date and time | 2025-09-07 14:30 |
| wl | Current water level | 3.25 |
| wrnwl | Warning level (fixed) | 4.5 |
| almwl | Caution level (fixed) | 5.0 |

## 4. NASA FIRMS API

#### Overview

- **Output:** `firms_data/*.csv`
- **Data:** satellite-based fire monitoring
- **Production:** approximately every 12 hours (twice daily)
- **Coverage:** Korean Peninsula

##### Response fields

| Column | Example | Meaning |
|---|---|---|
| `latitude` | 37.48554 | Fire detection latitude (degrees) |
| `longitude` | 129.05978 | Fire detection longitude (degrees) |
| `frp` | 10.3 | Fire Radiative Power (MW; fire intensity) |
| `daynight` | D | Day/night (D=day, N=night) |
| `acq_date` | 2025-08-08 | Satellite observation date (UTC in API response) |
| `acq_time` | 0950 | Satellite observation time (UTC, HHMM, in API response) |
| `satellite` | Terra | Observing satellite |
| `instrument` | MODIS | Observing sensor |
| `version` | 6.1NRT | Algorithm version (NRT=near real time) |
| **VIIRS_NOAA20_NRT — confidence** | n | Fire confidence (l=low, n=normal, h=high) |
| **VIIRS_NOAA20_NRT — bright_ti4** | 331.48 | Band 4 brightness temperature (K) |
| **VIIRS_NOAA20_NRT — bright_ti5** | 302.14 | Band 5 brightness temperature (K) |
| **MODIS_NRT — confidence** | 65 | Fire confidence (%) |
| **MODIS_NRT — brightness** | 313.81 | Fire-pixel brightness temperature (K) |
| **MODIS_NRT — bright_t31** | 301.66 | Band 31 brightness temperature (K) |

The collector converts `acq_date` and `acq_time` from UTC to Korea Standard Time in saved CSV files.
