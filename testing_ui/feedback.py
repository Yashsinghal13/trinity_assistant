import mysql.connector
import pandas as pd
from datetime import datetime
from implementation.answer import MODEL

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="octro",
        database="feedback"
    )


def get_feedback_data(role: str):
    conn = get_connection()

    # Total likes/dislikes
    totals_query = """
        SELECT r.name, COUNT(*) AS count
        FROM user_query f
        JOIN rating r ON f.rating_id = r.id
        WHERE f.role = %s
        GROUP BY r.name;
    """
    totals_df = pd.read_sql(totals_query, conn, params=[role])

    # Date-wise stats
    trend_query = """
        SELECT 
            DATE(f.feedback_date) AS feedback_date,
            SUM(CASE WHEN r.name = 'like' THEN 1 ELSE 0 END) AS likes,
            SUM(CASE WHEN r.name = 'dislike' THEN 1 ELSE 0 END) AS dislikes
        FROM user_query f
        JOIN rating r ON f.rating_id = r.id
        WHERE f.role = %s
        GROUP BY DATE(f.feedback_date)
        ORDER BY feedback_date;
    """
    trend_df = pd.read_sql(trend_query, conn, params=[role])


    model_query = """
        Select f.model,
        SUM(CASE WHEN r.name = 'like' THEN 1 ELSE 0 END) AS likes,
        SUM(CASE WHEN r.name = 'dislike' THEN 1 ELSE 0 END) AS dislikes
        from user_query f join rating r on f.rating_id = r.id where f.role = %s 
        group by f.model
    """

    model_df = pd.read_sql(model_query, conn, params=[role])

    conn.close()
    return totals_df, trend_df ,model_df


def insert_feedback(question: str, rating_name: str, role: str):
    conn = get_connection()
    cursor = conn.cursor()

    # Get rating_id
    cursor.execute(
        "SELECT id FROM rating WHERE name = %s",
        (rating_name,)
    )
    result = cursor.fetchone()

    if not result:
        conn.close()
        raise ValueError(f"Invalid rating_name: {rating_name}")

    rating_id = result[0]

    # Insert feedback
    cursor.execute("""
        INSERT INTO user_query (question, feedback_date, rating_id, role,model)
        VALUES (%s, %s, %s, %s,%s)
    """, (
        question,
        datetime.now().date(),   # since column is DATE
        rating_id,
        role,
        MODEL
    ))

    conn.commit()
    conn.close()