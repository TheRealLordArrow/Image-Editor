SET = 0
REMOVE = 1


def from_set(old_color: tuple[int, int, int], new_color: tuple[int, int, int], position: tuple[int, int]) -> dict:
    return {"action_id": SET, "old_color": old_color, "new_color": new_color, "position": position}
