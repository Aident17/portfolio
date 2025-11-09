#!/bin/bash

# Remove existing input and output
hdfs dfs -rm -r -f /Output/Task1
hdfs dfs -rm -r -f /Input

# create input direcotry and put trips.txt in it
hdfs dfs -mkdir -p /Input
hdfs dfs -put -f Trips.txt /Input/

# Run Hadoop Streaming
hadoop jar hadoop-streaming-3.1.4.jar \
    -D stream.num.map.output.key.fields=3 \
    -D mapred.reduce.tasks=3 \
    -input /Input/Trips.txt \
    -output /Output/Task1 \
    -file mapper1.py \
    -mapper mapper1.py \
    -file reducer1.py \
    -reducer reducer1.py

#3 map reduce tasks
#file names are mapper1.py, reducer1.py Task1-run.sh