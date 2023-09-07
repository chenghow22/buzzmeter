# TODO: Set project_id to your Google Cloud Platform project ID.
project_id = 'your-project-id'

# TODO: Set table_id to the full destination table ID (including the dataset ID).
destination_table = 'your-project-id.dateset.table'

pandas_gbq.to_gbq(df,
                  destination_table,
                  project_id=project_id,
                  chunksize=None, # I have tried with several chunk sizes, it runs faster when it's one big chunk (at least for me)
                  if_exists='replace', # Use the if_exists argument to dictate whether to 'fail', 'replace' or 'append' if the destination table already exists. The default value is 'fail'.
                  table_schema=[{'name': 'date','type': 'STRING'},
                               {'name': 'video_id','type': 'STRING'},
                               {'name': 'comment','type': 'STRING'},
                               {'name': 'like_count','type': 'INTEGER'},
                               {'name': 'comment_id','type': 'STRING'},
                               {'name': 'sentiment','type': 'STRING'},
                               {'name': 'sentiment_prob','type': 'FLOAT'},
                               {'name': 'hate_speech','type': 'STRING'},
                               {'name': 'hate_speech_prob','type': 'FLOAT'},
                               {'name': 'irony','type': 'STRING'},
                               {'name': 'irony_prob','type': 'FLOAT'},
                               {'name': 'emotion_output','type': 'STRING'},
                               {'name': 'joy','type': 'FLOAT'},
                               {'name': 'sadness','type': 'FLOAT'},
                               {'name': 'anger','type': 'FLOAT'},
                               {'name': 'surprise','type': 'FLOAT'},
                               {'name': 'disgust','type': 'FLOAT'},
                               {'name': 'fear','type': 'FLOAT'},
                               {'name': 'others','type': 'FLOAT'},
                               ],
                  verbose=False
                  )
