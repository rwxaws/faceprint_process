DELETE from
    rest_day
WHERE
    $1::DATE < rest_start_date::DATE OR
    $1::DATE > rest_end_date::DATE;
