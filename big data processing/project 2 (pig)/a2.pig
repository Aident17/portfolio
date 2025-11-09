--section 1 //////////////////////////////////////////

-- section 1.1 (loading the three datasets)
TRIPS = LOAD '/Input/Trips.txt'
      USING PigStorage('\t')
      AS (trip_id:int, taxi_id:int, company_id:int, dropoff_lat:double, dropoff_lon:double, distance_km:double, fare:double);

TAXIS = LOAD '/Input/Taxis.txt'
      USING PigStorage('\t')
      AS (taxi_id:int, license_plate:chararray, medallion_year:int, driver_rating:double);

COMPANIES = LOAD '/Input/Companies.txt'
      USING PigStorage('\t')
      AS (company_id:int, company_name:chararray);

-- section 1.2 (data cleaning, remove missing / null values)
cleaned_trips = FILTER TRIPS BY trip_id IS NOT NULL AND taxi_id IS NOT NULL AND company_id IS NOT NULL AND dropoff_lat IS NOT NULL AND dropoff_lon IS NOT NULL AND distance_km IS NOT NULL AND fare IS NOT NULL;

-- section 1.2 (only taking trips between 0.0 - 20.0, also fare must be greater than equal to 5.0)
cleaned_trips = FILTER cleaned_trips BY distance_km > 0.0 AND distance_km <= 20.0 AND fare >= 5.0;

-- section 1.3 (output for task 1)
STORE cleaned_trips INTO '/Output/clean_trips'
      USING PigStorage('\t');

-- section 2 //////////////////////////////////////////

-- section 2.1 (inner join cleaned_trips and TAXIS, then join with COMPANIES)
join1 = JOIN cleaned_trips BY taxi_id, TAXIS BY taxi_id;
join2 = JOIN join1 BY company_id, COMPANIES BY company_id;

-- section 2.2 (data enrichment, create a new dataset with the following columns)
enriched_trips = FOREACH join2 GENERATE
    cleaned_trips::taxi_id as taxi_id,
    cleaned_trips::company_id as company_id,
    COMPANIES::company_name as company_name,
    TAXIS::driver_rating as driver_rating,
    cleaned_trips::distance_km as distance_km,
    cleaned_trips::fare as fare,
    cleaned_trips::dropoff_lat as dropoff_lat,
    cleaned_trips::dropoff_lon as dropoff_lon;

-- section 2.3 (output task 2)
STORE enriched_trips INTO '/Output/enriched_trips'
      USING PigStorage('\t');

-- section 3 //////////////////////////////////////////

-- section 3.1 (group company id and company name, then calculate sum and avgs)
grouped_data = GROUP enriched_trips BY (company_id, company_name);

-- section 3.1 (use double and rount to getr the two decimal places/ clacate total and average)
company_stats = FOREACH grouped_data GENERATE
    group.company_id AS company_id,
    group.company_name AS company_name,
    COUNT(enriched_trips) AS trip_count,
    (double)ROUND(SUM(enriched_trips.distance_km) * 100) / 100.0 AS total_distance_km,
    (double)ROUND(AVG(enriched_trips.distance_km) * 100) / 100.0 AS avg_distance_km,
    (double)ROUND(AVG(enriched_trips.fare) * 100) / 100.0 AS avg_fare;

-- section 3.2 (sort by ascending by trip_count then company name)
sorted_stats = ORDER company_stats BY trip_count ASC, company_name ASC;

-- section 3.3 Store the output
STORE sorted_stats INTO '/Output/company_stats'
      USING PigStorage('\t');

-- section 4 //////////////////////////////////////////

-- register our python udf file to pig (fare_band.py)
REGISTER 'fare_band.py' USING jython AS pyfuncs;

-- create a new dataset using enriched trips
trips_with_bands = FOREACH enriched_trips GENERATE
    company_id,
    company_name,
    fare,
    pyfuncs.fare_band(fare) AS fare_band;

-- Grouped the data by company and then by fare_band
grouped = GROUP trips_with_bands BY (company_id, company_name, fare_band);

-- we count the number of trips for each group
data4 = FOREACH grouped GENERATE
    group.company_id,
    group.company_name,
    group.fare_band,
    COUNT(trips_with_bands) AS count;

-- (output for task 4)
STORE data4 INTO '/Output/fare_bands_by_company' 
    USING PigStorage('\t');
