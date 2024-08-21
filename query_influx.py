import pandas as pd
import pantab as pt
from influxdb_client import InfluxDBClient
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Set up the InfluxDB client
url = os.environ.get("INFLUXDB_URL")
token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
bucket = os.environ.get("INFLUXDB_BUCKET")

client = InfluxDBClient(url=url, token=token, org=org, timeout=600000)
query_api = client.query_api()

# Define the query
query = f"""
    from(bucket: "{bucket}")
        |> range(start: 0) // Start the query from the begining of data
        |> filter(fn: (r) => r["_measurement"] == "plating")
        |> filter(fn: (r) => r["_field"] == "P_actv")
        |> group(columns: ["_measurement", "_field"])
        |> aggregateWindow(every: 1s, fn: mean, createEmpty: false)
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> yield(name: "mean")
        |> timeShift(duration: 7h) // Adjust the timestamp to timezone UTC+7 Jakarta
    """

# Execute the query
tables = query_api.query(query)

# Convert the result to a DataFrame
data = []
for table in tables:
    for record in table.records:
        data.append(record.values)

df = pd.DataFrame(data)

print(data)

# Rename columns
df.rename(
    columns={
        "_time": "date",
        "_measurement": "location",
        "P_actv": "power_meter",
    },
    inplace=True,
)

# Delete the unused columns
# del df["result"]
df.drop(columns=["result", "table", "location", "_start", "_stop"], axis=1, inplace=True)

# Ensure date column is in datetime format
df["date"] = pd.to_datetime(df["date"])

# Convert the data to .tde file format
pt.frame_to_hyper(df, "power_meter.hyper", table="power")

# Save to CSV
csv_filename = "power_meter_raw.csv"
df.to_csv(csv_filename, index=False)

print(f"Data has been successfully exported to '{csv_filename}'.")