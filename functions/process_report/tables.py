def get_excuses(con):
    return con.sql("""
        SELECT
            emp_voter_num AS 'رقم الناخب',
            emp_name AS 'اسم الموظف',
            date AS 'تاريخ البصمة',
            unit AS 'الشعبة',
            entry_time AS 'وقت الدخول',
            leave_time AS 'وقت الخروج',
            target_entry AS 'وقت البصمة',
            is_late AS 'متأخر',
            is_early AS 'مبكر',
            is_absent AS 'غائب',
            excuse AS 'عذر الجهاز',
            id AS 'رقم الواجب او الاجازة',
            num_hours AS 'عدد ساعات الواجب او الزمنية',
            start_hour AS 'ساعة البدء',
            end_hour AS 'ساعة النهاية',
            duty_date AS 'التاريخ',
            status AS 'الحالة'
        FROM report_duty_fullday
        UNION BY NAME
        SELECT
            emp_voter_num AS 'رقم الناخب',
            emp_name AS 'اسم الموظف',
            date AS 'تاريخ البصمة',
            unit AS 'الشعبة',
            entry_time AS 'وقت الدخول',
            leave_time AS 'وقت الخروج',
            target_entry AS 'وقت البصمة',
            is_late AS 'متأخر',
            is_early AS 'مبكر',
            is_absent AS 'غائب',
            excuse AS 'عذر الجهاز',
            id AS 'رقم الواجب او الاجازة',
            num_hours AS 'عدد ساعات الواجب او الزمنية',
            start_hour AS 'ساعة البدء',
            end_hour AS 'ساعة النهاية',
            duty_date AS 'التاريخ',
            status AS 'الحالة'
        FROM report_duty_halfday
        UNION BY NAME
        SELECT
            emp_voter_num AS 'رقم الناخب',
            emp_name AS 'اسم الموظف',
            date AS 'تاريخ البصمة',
            unit AS 'الشعبة',
            entry_time AS 'وقت الدخول',
            leave_time AS 'وقت الخروج',
            target_entry AS 'وقت البصمة',
            is_late AS 'متأخر',
            is_early AS 'مبكر',
            is_absent AS 'غائب',
            excuse AS 'عذر الجهاز',
            id AS 'رقم الواجب او الاجازة',
            num_rest_days AS 'عدد ايام الاجازة',
            rest_start_date AS 'تاريخ بدء الاجازة',
            rest_end_date AS 'تاريخ نهاية الاجازة',
            status AS 'الحالة'
        FROM report_restday
        UNION BY NAME
        SELECT
            emp_voter_num AS 'رقم الناخب',
            emp_name AS 'اسم الموظف',
            date AS 'تاريخ البصمة',
            unit AS 'الشعبة',
            entry_time AS 'وقت الدخول',
            leave_time AS 'وقت الخروج',
            target_entry AS 'وقت البصمة',
            is_late AS 'متأخر',
            is_early AS 'مبكر',
            is_absent AS 'غائب',
            excuse AS 'عذر الجهاز',
            id AS 'رقم الواجب او الاجازة',
            num_hours AS 'عدد ساعات الواجب او الزمنية',
            start_hour AS 'ساعة البدء',
            end_hour AS 'ساعة النهاية',
            status AS 'الحالة'
        FROM report_resttime
    """).df().astype(str).replace(['NaT', '<NA>', 'None'], '')

def get_no_excuses(con):
    return con.sql("""
        SELECT
            emp_voter_num AS 'رقم الناخب',
            emp_name AS 'اسم الموظف',
            date AS 'تاريخ البصمة',
            unit AS 'الشعبة',
            entry_time AS 'وقت الدخول',
            leave_time AS 'وقت الخروج',
            target_entry AS 'وقت البصمة',
            is_late AS 'متأخر',
            is_early AS 'مبكر',
            is_absent AS 'غائب',
            excuse AS 'عذر الجهاز',
        FROM report
    """).df().astype(str).replace(['NaT', '<NA>', 'None'], '')
