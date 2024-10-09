# The RDZ Stack
Development of IoT Project in Hirose Indonesia is using this stack. This project includes a Python application that queries data from InfluxDB and exports it to Hyper files for use in Tableau. The application is designed to run inside a Docker container, utilizing various services defined in the `compose.yaml` file.

The list of stack used:
1. **Grafana**
   - This stack is used for dashboard monitoring.
2. **InfluxDB**
   - Needs to handle real-time data.
3. **Telegraf**
   - Agent that acts as a fetcher and inserts data into InfluxDB.
4. **Python**
   - Used to create and export the data into `.hyper` files that are used on Tableau.

This stack runs inside the Docker container.

The project that is currently running using this stack:
1. **RDZ-E**, collects data power metrics from IoT devices.
   - This project 
2. x

## How To Use

### Setup
1. Ensure you have Python installed (preferably Python 3.7 or higher).
2. Install the required packages:
   ```bash
   pip install pandas pantab influxdb-client python-dotenv tqdm
   ```
3. Create a `.env` file in the same directory as your script with the following variables:
   ```bash
   INFLUXDB_URL=<your_influxdb_url>
   INFLUXDB_TOKEN=<your_influxdb_token>
   INFLUXDB_ORG=<your_influxdb_org>
   INFLUXDB_BUCKET=<your_influxdb_bucket>
   ```

### Running the Script
To run the script, use the command line and navigate to the directory containing `query_influx.py`. Execute the script with the following command:
```bash
python query_influx.py [start_date='0'] [aggregate_time='1s'] [aggregate_fn='mean']
```
- `<start_date>`: The start date for the query (default is '0').
- `<aggregate_time>`: The time interval for aggregation (default is '1s').
- `<aggregate_fn>`: The aggregation function to use (default is 'mean').
**_Notes: Defaults apply if args not provided_**

### Expected Results
- The script will connect to the InfluxDB instance using the provided credentials.
- It will construct a query to fetch power metrics from the specified bucket.
- The fetched data will be exported to a `.hyper` file named `power_meter.hyper` in the same directory.
- Logs will be created in a `logs` directory, with errors recorded if any issues occur during execution.
