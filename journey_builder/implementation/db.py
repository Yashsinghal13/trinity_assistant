import pandas as pd
import numpy as np
from sqlalchemy.engine import create_engine
import trino
from dotenv import load_dotenv

load_dotenv(override=True)


trino_host = os.getenv("TRINO_HOST") 
trino_port = os.getenv("TRINO_PORT")   
trino_catalog = os.getenv("TRINO_CATALOG")
trino_schema = os.getenv("TRINO_SCHEMA")
trino_table = os.getenv("TRINO_TABLE")
trino_user = os.getenv("TRINO_USER")
trino_password = os.getenv("TRINO_PASSWORD")

# Create SQLAlchemy engine for Trino

conn = trino.dbapi.connect(
    host=trino_host,
    port=int(trino_port),
    user=trino_user,
    http_scheme="https",   # important since you’re using 8143 (TLS)
    auth=trino.auth.BasicAuthentication(trino_user, trino_password),
    catalog=trino_catalog,
    schema=trino_schema,
)

def get_report_by_planner_id(planner_id):
    query = f"""
    with agg as (
        SELECT planner_id,
            SUM(campaign_sent_count) AS Total_Sent_Count,
            SUM(num_recieved) AS total_received
        FROM campaign_auto_report_detail
        WHERE planner_id = {int(planner_id)}
        AND campaign_date >= DATE '2026-02-01'
        GROUP BY planner_id 
    )
    select t2.planner_name,t1.Total_Sent_Count,t1.total_received from agg as t1 inner join go_planner_tab as t2 on t1.planner_id = t2.planner_id
    """

    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")


def listing_all_journey(status):
    query=f"""
    SELECT planner_id,planner_name FROM go_planner_tab where lower(status) = '{status}'"""
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")

def create_template():
    return "Template Created Successfully"

def create_campaign():
    return "Campaign Created Successfully"



