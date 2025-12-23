SELECT
    emp_voter_num  AS "رقم الناخب",
    emp_name       AS "اسم الموظف",
    date           AS "تاريخ البصمة",
    emp_center_num AS "رقم المركز",
    entry_time     AS "وقت الدخول",
    mid_time       AS "بصمة وسطية",
    leave_time     AS "وقت الخروج",
    target_entry   AS "وقت البصمة",
    target_mid     AS "وقت البصمة الوسطية",
    is_late        AS "متأخر",
    is_mid         AS "حالة البصمة الوسطية",
    is_early       AS "مبكر",
    is_absent      AS "غائب"
FROM
    faceprint_attendant;
