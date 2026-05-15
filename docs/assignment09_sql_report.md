# Задание 9. Аналитический SQL-запрос

## Задача (естественный язык)

> Топ-10 номеров отеля по суммарной выручке от бронирований за последние 30 дней, с количеством бронирований.

## Запрос

Файл: `sql/top_rooms_by_revenue.sql`

## Логика

1. **`FROM rooms r`** — все номера как основа (номера без броней тоже попадут с выручкой 0).
2. **`LEFT JOIN bookings b`** — присоединяем бронирования по `room_id`.
3. **Фильтр в `ON`**:
   - `status NOT IN ('cancelled')` — не учитываем отменённые;
   - `check_in >= CURRENT_DATE - 30 days` — окно 30 дней.
4. **`GROUP BY`** номер — одна строка на комнату.
5. **`SUM(total_price)`** — выручка; **`COUNT(b.id)`** — число броней.
6. **`ORDER BY total_revenue DESC LIMIT 10`** — топ-10.

## Связи в схеме

- `bookings.room_id` → `rooms.id` (**многие-к-одному**)
- `bookings.guest_id` → `guests.id`
- `stays.booking_id` → `bookings.id` (**один-к-одному**)

Индексы `ix_bookings_room_id`, `ix_bookings_check_in` ускоряют JOIN и фильтр по дате.
