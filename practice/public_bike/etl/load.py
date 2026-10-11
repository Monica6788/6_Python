"""
    Load: 데이터를 DB에 적재 (저장)
"""
import time

from .config import connect, CHUNK_SIZE
from schema import RAW_BIKES_DDL, RAW_RENTALS_DDL, BIKES_DDL, RENTALS_DDL, STATIONS_DDL, 

# DB에 저장할 컬럼 순서
BIKES_COLS = ["bike_id", "station_id", "bike_type", "gear_count",
              "manufacture_year", "daily_fee"]
RENTALS_COLS = ["rental_id", "bike_id", "user_id",
                "rent_time", "return_time", "distance_km",
                "fee", "payment_method"]
STATIONS_COLS = ["station_id", "station_name", "district"]

# -------------------- SQL 조각 --------------------
B_COLS_SQL = ", ".join(c for c in BIKES_COLS)
R_COLS_SQL = ", ".join(c for c in RENTALS_COLS)
S_COLS_SQL = ", ".join(c for c in STATIONS_COLS)

# PlaceHolder
B_PH = ", ".join(f":{i + 1}" for i in range(len(BIKES_COLS)))
R_PH = ", ".join(f":{i + 1}" for i in range(len(RENTALS_COLS)))
S_PH = ", ".join(f":{i + 1}" for i in range(len(STATIONS_COLS)))

B_MERGE_USING = ", ".join(f":{i + 1} AS {c}" for i, c in enumerate(BIKES_COLS))
R_MERGE_USING = ", ".join(f":{i + 1} AS {c}" for i, c in enumerate(RENTALS_COLS))
S_MERGE_USING = ", ".join(f":{i + 1} AS {c}" for i, c in enumerate(STATIONS_COLS))

B_UPSERT = f"""
MERGE INTO bikes dst
USING (SELECT {B_MERGE_USING} FROM dual) src
ON (dst.bike_id = src.bike_id)
WHEN MATCHED THEN
    UPDATE SET dst.station_id = src.station_id,
               dst.bike_type = src.bike_type,
               dst.gear_count = src.gear_count,
               dst.manufacture_year = src.manufacture_year,
               dst.daily_fee = src.daily_fee
WHEN NOT MATCHED THEN
    INSERT {B_COLS_SQL}
    VALUES (src.bike_id, src.station_id, src.bike_type,
            src.gear_count, src.manufacture_year,
            src.daily_fee)
"""

R_UPSERT = f"""
MERGE INTO rentals dst
USING (SELECT {R_MERGE_USING} FROM dual) src
ON (dst.rental_id = src.rental_id AND
    dst.bike_id = src.bike_id AND
    dst.user_id = src.user_id)
WHEN MATCHED THEN
    UPDATE SET dst.rent_time = src.rent_time,
               dst.return_time = src.return_time,
               dst.distance_km = src.distance_km,
               dst.fee = src.fee,
               dsf.payment_method = src.payment_method
WHEN NOT MATCHED THEN
    INSERT {R_COLS_SQL}
    VALUES (src.rental_id, src.bike_id, src.user_id,
            src.rent_time, src.return_time,
            src.distance_km, src.fee,
            src.payment_method)
"""


