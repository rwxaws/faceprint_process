CREATE OR REPLACE TABLE export_faceprint_attendant AS
SELECT
    emp_voter_num AS "رقم الناخب",
    emp_name AS "اسم الموظف",
    date AS "تاريخ البصمة",
    emp_center_num AS "رقم المركز",
    entry_time AS "وقت الدخول",
    mid_time AS "بصمة وسطية",
    leave_time AS "وقت الخروج",
    target_entry AS "وقت بصمة الدخول",
    target_mid AS "وقت البصمة الوسطية"
FROM faceprint_attendant;

CREATE OR REPLACE TABLE export_faceprint_excused_full AS
SELECT
    emp_voter_num AS "رقم الناخب",
    emp_name AS "اسم الموظف",
    date AS "تاريخ البصمة",
    emp_center_num AS "رقم المركز",
    id AS "رقم العذر",
    excuse_type AS "نوع العذر",
    duty_date AS "تاريخ الواجب",
    num_rest_days AS "عدد الايام",
    rest_start_date AS "يوم البداية",
    rest_end_date AS "يوم النهاية",
    status AS "حالة العذر"
FROM faceprint_excused_full;

CREATE OR REPLACE TABLE export_faceprint_excused_half AS
SELECT
    emp_voter_num AS "رقم الناخب",
    emp_name AS "اسم الموظف",
    date AS "تاريخ البصمة",
    emp_center_num AS "رقم المركز",
    entry_time AS "وقت الدخول",
    mid_time AS "وقت الوسطية",
    leave_time AS "وقت الخروج",
    target_entry AS "وقت بصمة الدخول",
    target_mid AS "وقت البصمة الوسطية",
    is_late AS "متأخر",
    is_mid AS "حالة البصمة الوسطية",
    is_early AS "مبكر",

    entry_excuse_id AS "رقم عذر الدخول",
    entry_excuse_type AS "نوع عذر الدخول",
    entry_num_hours AS "عدد ساعات عذر الدخول",
    entry_start_hour AS "ساعة بدء عذر الدخول",
    entry_end_hour AS "ساعة نهاية عذر الدخول",
    entry_status AS "حالة عذر الدخول",

    mid_excuse_id AS "رقم عذر الوسطية",
    mid_excuse_type AS "نوع عذر الوسطية",
    mid_num_hours AS "عدد ساعات عذر الوسطية",
    mid_start_hour AS "ساعة بدء عذر الوسطية",
    mid_end_hour AS "ساعة نهاية عذر الوسطية",
    mid_status AS "حالة عذر الوسطية",

    leave_excuse_id AS "رقم عذر الخروج",
    leave_excuse_type AS "نوع عذر الخروج",
    leave_num_hours AS "عدد ساعات عذر الخروج",
    leave_start_hour AS "ساعة بدء عذر الخروج",
    leave_end_hour AS "ساعة نهاية عذر الخروج",
    leave_status AS "حالة عذر الخروج"
FROM faceprint_excused_half;

CREATE OR REPLACE TABLE export_faceprint_unexcused AS
SELECT
    emp_voter_num AS "رقم الناخب",
    emp_name AS "اسم الموظف",
    date AS "تاريخ البصمة",
    emp_center_num AS "رقم المركز",
    entry_time AS "وقت الدخول",
    mid_time AS "بصمة وسطية",
    leave_time AS "وقت الخروج",
    target_entry AS "وقت البصمة",
    target_mid AS "وقت البصمة الوسطية",
    is_late AS "متأخر",
    is_early AS "مبكر",
    is_absent AS "غائب"
FROM faceprint;
