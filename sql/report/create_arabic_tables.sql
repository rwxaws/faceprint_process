-- attendants
CREATE OR REPLACE TABLE arabic_report_attendant AS
SELECT
    emp_voter_num AS "رقم الناخب",
    emp_name AS "اسم الموظف",
    date AS "تاريخ البصمة",
    unit AS "الشعبة",
    entry_time AS "وقت الدخول",
    leave_time AS "وقت الخروج",
    target_entry AS "وقت البصمة",
FROM
    report_attendant;

-- full day excuse
CREATE OR REPLACE TABLE arabic_report_fullday AS
SELECT
    emp_voter_num AS "رقم الناخب",
    emp_name AS "اسم الموظف",
    date AS "تاريخ البصمة",
    unit AS "الشعبة",
    entry_time AS "وقت الدخول",
    leave_time AS "وقت الخروج",
    target_entry AS "وقت البصمة",
    is_late AS "متأخر",
    is_early AS "مبكر",
    is_absent AS "غائب",
    excuse AS "عذر الجهاز",
    id AS "رقم الواجب او الاجازة",
    duty_date AS "تاريخ الواجب",
    status AS "الحالة",
    num_rest_days AS "عدد ايام الاجازة",
    rest_start_date AS "بداية الاجازة",
    rest_end_date AS "نهاية الاجازة"
FROM
    report_fullday;

-- half day excuse
CREATE OR REPLACE TABLE arabic_report_halfday AS
    SELECT * FROM report_halfday
    UNION ALL BY NAME
    SELECT * FROM report_halfday_missing;

CREATE OR REPLACE TABLE arabic_report_halfday AS
    SELECT
        emp_voter_num AS "رقم الناخب",
        emp_name AS "اسم الموظف",
        date AS "تاريخ البصمة",
        unit AS "الشعبة",
        entry_time AS "وقت الدخول",
        leave_time AS "وقت الخروج",
        target_entry AS "وقت البصمة",
        is_late AS "متأخر",
        is_early AS "مبكر",
        is_absent AS "غائب",
        excuse AS "عذر الجهاز",
        id AS "رقم الزمنية او الواجب",
        num_hours AS "عدد ساعات الزمنية او الواجب",
        duty_date AS "تاريخ الواجب",
        start_hour AS "ساعة البدء",
        end_hour AS "ساعة النهاية",
        status AS "الحالة"
    FROM
        arabic_report_halfday;

-- no excuse
CREATE OR REPLACE TABLE arabic_no_excuse AS
    SELECT
            emp_voter_num AS "رقم الناخب",
        emp_name AS "اسم الموظف",
        date AS "تاريخ البصمة",
        unit AS "الشعبة",
        entry_time AS "وقت الدخول",
        leave_time AS "وقت الخروج",
        target_entry AS "وقت البصمة",
        is_late AS "متأخر",
        is_early AS "مبكر",
        is_absent AS "غائب",
        excuse AS "عذر الجهاز"
    FROM
        report;
