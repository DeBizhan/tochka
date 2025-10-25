import sys
import heapq

ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_INDEX = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
ROOM_POS = [2, 4, 6, 8]
HALL_VALID = [0, 1, 3, 5, 7, 9, 10]

def parse_input(lines):
    if len(lines) not in (5, 7):
        print("Ошибка ввода: неверное количество строк")
        sys.exit(1)
    if not lines[0].startswith("#############") or not lines[1].startswith("#...........#"):
        print("Ошибка ввода: неверный формат верхних строк")
        sys.exit(1)
    depth = len(lines) - 3
    if depth not in (2, 4):
        print("Ошибка ввода: допустимы только глубины комнат 2 или 4")
        sys.exit(1)
    room_lines = lines[2:-1]
    rooms = [[] for _ in range(4)]
    try:
        for rline in room_lines:
            parts = [c for c in rline if c in "ABCD"]
            if len(parts) != 4:
                raise ValueError
            for i in range(4):
                rooms[i].append(parts[i])
    except Exception:
        print("Ошибка ввода: неверный формат комнат")
        sys.exit(1)
    if not lines[-1].strip().startswith("#########"):
        print("Ошибка ввода: неверное завершение лабиринта")
        sys.exit(1)
    for i in range(4):
        rooms[i] = rooms[i][::-1]
    hallway = "." * 11
    return hallway, tuple(tuple(r) for r in rooms), depth

def is_goal(rooms, depth):
    for i, room in enumerate(rooms):
        if any(x != "ABCD"[i] for x in room) or len(room) != depth:
            return False
    return True

def path_clear(hall, start, end):
    if start < end:
        rng = range(start + 1, end + 1)
    else:
        rng = range(end, start)
    return all(hall[i] == '.' for i in rng)

def moves_from_state(hall, rooms, depth):
    result = []
    for i, room in enumerate(rooms):
        if not room:
            continue
        amph = room[-1]  # верхний
        if all(x == "ABCD"[i] for x in room) and len(room) == depth:
            continue
        hall_pos = ROOM_POS[i]
        for pos in reversed(range(0, hall_pos)):
            if hall[pos] != '.':
                break
            if pos in HALL_VALID:
                new_hall = list(hall)
                new_rooms = [list(r) for r in rooms]
                new_rooms[i].pop()
                new_hall[pos] = amph
                dist = (hall_pos - pos) + (depth - len(room) + 1)
                cost = ENERGY[amph] * dist
                result.append(("".join(new_hall), tuple(tuple(r) for r in new_rooms), cost))
        for pos in range(hall_pos + 1, 11):
            if hall[pos] != '.':
                break
            if pos in HALL_VALID:
                new_hall = list(hall)
                new_rooms = [list(r) for r in rooms]
                new_rooms[i].pop()
                new_hall[pos] = amph
                dist = (pos - hall_pos) + (depth - len(room) + 1)
                cost = ENERGY[amph] * dist
                result.append(("".join(new_hall), tuple(tuple(r) for r in new_rooms), cost))

    for pos, amph in enumerate(hall):
        if amph == '.':
            continue
        target_room = ROOM_INDEX[amph]
        room_pos = ROOM_POS[target_room]
        room = rooms[target_room]
        if not path_clear(hall, pos, room_pos):
            continue
        if any(x != amph for x in room):
            continue
        if len(room) == depth:
            continue
        new_hall = list(hall)
        new_rooms = [list(r) for r in rooms]
        new_hall[pos] = '.'
        new_rooms[target_room].append(amph)
        dist = abs(pos - room_pos) + (depth - len(room))
        cost = ENERGY[amph] * dist
        result.append(("".join(new_hall), tuple(tuple(r) for r in new_rooms), cost))

    return result

def solve(lines):
    hallway, rooms, depth = parse_input(lines)
    start = (hallway, rooms)
    target_rooms = tuple(tuple([c] * depth) for c in "ABCD")
    heap = [(0, start)]
    best_cost = {start: 0}

    while heap:
        cost, (hall, rooms) = heapq.heappop(heap)
        if is_goal(rooms, depth):
            return cost
        if best_cost[(hall, rooms)] < cost:
            continue
        for new_hall, new_rooms, move_cost in moves_from_state(hall, rooms, depth):
            new_state = (new_hall, new_rooms)
            new_total = cost + move_cost
            if new_state not in best_cost or new_total < best_cost[new_state]:
                best_cost[new_state] = new_total
                heapq.heappush(heap, (new_total, new_state))
    return -1

def main():
    lines = [line.rstrip("\n") for line in sys.stdin if line.strip()]
    if not lines:
        print("Ошибка ввода: пустой ввод")
        return
    result = solve(lines)
    print(result)

if __name__ == "__main__":
    main()
