-- set absent
UPDATE report
SET is_absent = 'غائب'
WHERE
    entry_time IS NULL
    AND leave_time IS NULL;

-- set without entry
UPDATE report
SET is_late = 'بدون بصمة دخول'
WHERE
    entry_time IS NULL
    AND is_absent IS NULL;

-- set without leave
UPDATE report
SET is_early = 'بدون بصمة خروج'
WHERE
    leave_time IS NULL
    AND is_absent IS NULL;

-- set late entry
UPDATE report
SET is_late = 'متأخر'
WHERE
    entry_time IS NOT NULL
    AND target_entry = TIME '08:00:00'
    AND entry_time >= TIME '08:31:00';

-- set early leave
UPDATE report
SET is_early = 'مبكر'
WHERE
    leave_time IS NOT NULL
    AND target_entry = TIME '08:00:00'
    AND leave_time < TIME '15:00:00';
