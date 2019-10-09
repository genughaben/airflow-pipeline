class SqlQueries:
    songplay_table_insert = ("""
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)


# INSERT DATA INTO STAGING TABLES

# staging_events_copy = (
#     f"COPY staging_events "
#     f"FROM {LOG_DATA} "
#     f"CREDENTIALS 'aws_iam_role={DWH_ROLE_ARN}' "
#     f"FORMAT as JSON {LOG_JSONPATH} "
#     f"STATUPDATE ON "
#     f"region 'eu-west-1';"
# )
#
# staging_songs_copy = (
#     f"COPY staging_songs FROM {SONG_DATA} "
#     f"CREDENTIALS 'aws_iam_role={DWH_ROLE_ARN}' "
#     f"FORMAT as JSON 'auto' "
#     f"ACCEPTINVCHARS AS '^' "
#     f"STATUPDATE ON "
#     f"region 'eu-west-1';"
# )

copy_sql = """
    COPY {}
    FROM 's3://{}/{}'
    FORMAT AS JSON 'auto'
    ACCESS_KEY_ID '{}'
    SECRET_ACCESS_KEY '{}'
    ACCEPTINVCHARS AS '^'
    STATUPDATE ON
    REGION '{}';
"""


# INSERT INTO FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (
        start_time,
        user_id,
        level,
        song_id,
        artist_id,
        session_id,
        location,
        user_agent
    ) 
    SELECT DISTINCT
        se.ts                 AS start_time,
        se.userId             AS user_id,
        se.level,
        so.song_id            AS song_id,
        se.artist             AS artist_id,
        se.sessionId          AS session_id,
        se.location,
        se.userAgent          AS user_agent
    FROM staging_events se, staging_songs so 
    WHERE se.song = so.title AND page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO users (
        user_id,
        first_name,
        last_name,
        gender,
        level
    )
    SELECT DISTINCT
        userId              AS user_id,
        firstName           AS first_name,
        lastName            AS last_name,
        gender              AS gender,
        level               AS level
    FROM staging_events
    WHERE page = 'NextSong' AND user_id IS NOT NULL;
""")

song_table_insert = ("""
    INSERT INTO songs (
        song_id,
        title,
        artist_id,
        year,
        duration
    )
    SELECT DISTINCT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs;
""")

artist_table_insert = ("""
    INSERT INTO artists (
        artist_id,
        name,
        location,
        latitude,
        longitude
    )
    SELECT DISTINCT
        artist_id,
        artist_name         AS name,
        artist_location     AS location,        
        artist_latitude     AS latitude,
        artist_longitude    AS longitude
    FROM staging_songs;
""")

time_table_insert = ("""
    INSERT INTO time (
        start_time,
        hour,
        day,
        week,
        month,
        year,
        week_day
    )
    SELECT ts as start_time,
           EXTRACT(hour FROM date_string)     AS hour,
           EXTRACT(day FROM date_string)      AS day,
           EXTRACT(week FROM date_string)     AS week,
           EXTRACT(month FROM date_string)    AS month,
           EXTRACT(year FROM date_string)     AS year,
           EXTRACT(weekday FROM date_string) AS week_day
    FROM ( SELECT DISTINCT 
               ts, 
               '1970-01-01'::date + ts / 1000 * INTERVAL '1 second' AS date_string 
           FROM staging_events 
           WHERE page = 'NextSong')
    ORDER BY start_time;
""")

insert_table_queries = {
    "users": user_table_insert,
    "songs": song_table_insert,
    "artists": artist_table_insert,
    "time": time_table_insert,
    "songplays": songplay_table_insert
}