import pandas as pd
import pantab as pt
from influxdb_client import InfluxDBClient
from datetime import datetime
from dotenv import load_dotenv
import os
from time import time
import logging
from tqdm import tqdm


def setup_logging():
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def load_env_variables():
    load_dotenv()
    return {
        "url": os.environ.get("INFLUXDB_URL"),
        "token": os.environ.get("INFLUXDB_TOKEN"),
        "org": os.environ.get("INFLUXDB_ORG"),
        "bucket": os.environ.get("INFLUXDB_BUCKET"),
    }


def setup_influxdb_client(env_vars):
    try:
        client = InfluxDBClient(
            url=env_vars["url"],
            token=env_vars["token"],
            org=env_vars["org"],
            timeout=600000,
        )
        query_api = client.query_api()
        logging.info("InfluxDB client setup successful.")
        return query_api
    except Exception as e:
        logging.error(f"Failed to setup InfluxDB client detail: {e}.")
        raise


def construct_query(bucket):
    try:
        print("Starting query construction...")  # Print status
        start_time = time()  # Start timing
        with tqdm(total=1, desc="Constructing query") as pbar:
            query = f"""
                from(bucket: "{bucket}")
                    |> range(start: -2d)
                    |> filter(fn: (r) => r["_measurement"] == "plating")
                    |> filter(fn: (r) => r["_field"] == "P_actv")
                    |> group(columns: ["_measurement", "_field"])
                    |> aggregateWindow(every: 1s, fn: mean, createEmpty: false)
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
                    |> yield(name: "mean")
                    |> timeShift(duration: -7h)
                """
            pbar.update(1)
        elapsed_time = time() - start_time  # Calculate elapsed time
        print(f"Query constructed in {elapsed_time:.2f} seconds.")
        return query
    except Exception as e:
        logging.error(f"Failed to construct query: {e}.")
        raise


def fetch_data(query_api, query):
    try:
        print("Starting data fetching...")  # Print status
        start_time = time()  # Start timing
        tables = query_api.query(query)
        records = [
            {
                "date": record["_time"],
                "location": record["_measurement"],
                "power_meter": record["P_actv"],
            }
            for table in tqdm(tables, desc="Fetching data")
            for record in table.records
        ]
        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"])
        elapsed_time = time() - start_time  # Calculate elapsed time
        print(f"Data fetched in {elapsed_time:.2f} seconds.")
        return df
    except Exception as e:
        logging.error(f"Failed to fetch data: {e}.")
        raise


def export_data_to_hyper(df, filename="power_meter.hyper"):
    try:
        print("Starting data export to Hyper...")  # Print status
        start_time = time()  # Start timing
        with tqdm(total=1, desc="Exporting data to Hyper") as pbar:
            pt.frame_to_hyper(df, filename, table="power")
            pbar.update(1)
        elapsed_time = time() - start_time  # Calculate elapsed time
        print(f"Data exported to Hyper in {elapsed_time:.2f} seconds.")
    except Exception as e:
        logging.error(f"Failed to export data: {e}.")
        raise


def main():
    setup_logging()
    env_vars = load_env_variables()
    query_api = setup_influxdb_client(env_vars)

    start_time = time()

    query = construct_query(env_vars["bucket"])
    df = fetch_data(query_api, query)

    # Uncomment this and pass to the function export_data_to_hyper to add timestamps to the exported file
    # costum_filename = f"power_meter-{datetime.now().strftime('%Y-%m-%d')}.hyper"

    export_data_to_hyper(df)

    end_time = time()
    elapsed = end_time - start_time
    print(f"Total process finished in {elapsed:.2f} seconds elapsed")


if __name__ == "__main__":
    main()
