#!/bin/bash

# Remove existing input and output
hdfs dfs -rm -r -f /Output/Task2
hdfs dfs -rm -r -f /Input

# Create input directory and put Trips.txt in it
hdfs dfs -mkdir -p /Input
hdfs dfs -put -f Trips.txt /Input/Trips.txt

# read v and seed medoids (skip first line = v)
v=$(head -n1 initialization.txt)
tail -n +2 initialization.txt > medoids.txt
# print iterations
i=1
while [ "$i" -le "$v" ]; do
  echo "======================"
  echo "Iteration $i"
  echo "======================"

  # set output path for this iteration
  out="/mapreduce-output$i"

  # clean previous output
  hadoop fs -rm -r -f "$out" >/dev/null 2>&1

  # run Hadoop streaming job
  hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \
    -D mapred.text.key.partitioner.options=-k1 \
    -files mapper2.py,reducer2.py,medoids.txt \
    -mapper mapper2.py \
    -reducer reducer2.py \
    -input /Input/Trips.txt \
    -output "$out" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

  # merges the  reducer outputs into a single medoid list
  rm -f new_medoids.txt
  hadoop fs -getmerge "$out/part-*" new_medoids.txt

  # keep only the first k medoids (avoid duplicates from 3 reducers)
  k=$(wc -l < medoids.txt)
  head -n "$k" new_medoids.txt > trimmed.txt
  mv trimmed.txt new_medoids.txt

  echo "Medoids after iteration $i:"
  cat new_medoids.txt
  echo

  # this is to end the loop
  if cmp -s medoids.txt new_medoids.txt; then
    echo "Converged at iteration $i"
    mv new_medoids.txt medoids.txt
    break
  fi

  # updates medoids.txt for next round
  mv new_medoids.txt medoids.txt
  i=$((i+1))
done

# saves the final medoids as final Task2 result
hdfs dfs -rm -r -f /Output/Task2 >/dev/null 2>&1
hdfs dfs -mkdir -p /Output/Task2
hdfs dfs -cp "$out/part-*" /Output/Task2/