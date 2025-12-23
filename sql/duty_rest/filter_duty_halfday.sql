DELETE FROM
    duty_halfday
WHERE
    duty_date != $1;
