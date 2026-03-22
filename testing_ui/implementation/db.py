import pandas as pd
import numpy as np
from sqlalchemy.engine import create_engine
import trino


trino_host = "trinoprod.octro.com"  # Trino server hostname/IP
trino_port = "8143"                         # Trino port
trino_catalog = "trinity_sql"                     # Catalog
trino_schema = "octro_crm"                    # Schema
trino_table = "campaign_auto_report_detail"                   # Table
trino_user = "superset"                      # Username
trino_password = "superset123"               # Password

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
    return "continue"
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
    return "continue"
    query=f"""
    SELECT planner_id,planner_name FROM go_planner_tab where lower(status) = '{status}'"""
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")

def create_template():
    return "Template Created Successfully"

def create_campaign():
    return "Campaign Created Successfully"



