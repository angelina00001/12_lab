-- Задание 9: Топ-10 номеров по выручке за последние 30 дней
-- Связи: bookings.room_id -> rooms.id (многие-к-одному)

SELECT
    r.id AS room_id,
    r.number AS room_code,
    r.room_type,
    COUNT(b.id) AS booking_count,
    COALESCE(SUM(b.total_price), 0) AS total_revenue
FROM rooms r
LEFT JOIN bookings b
    ON b.room_id = r.id
    AND b.status NOT IN ('cancelled')
    AND b.check_in >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY r.id, r.number, r.room_type
ORDER BY total_revenue DESC
LIMIT 10;
