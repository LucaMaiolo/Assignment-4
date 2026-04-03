from __future__ import annotations
from typing import TypeVar, Optional

T = TypeVar("T")

class DoubleLink[T]:
    def __init__(self, element: T):
        self.element: T = element
        self.next: Optional[DoubleLink[T]] = None
        self.prev: Optional[DoubleLink[T]] = None


def build_circle(n: int) -> list[DoubleLink[str]]:
    links = [DoubleLink(chr(ord('A') + i)) for i in range(n)]
    for i in range(n):
        links[i].next = links[(i + 1) % n]
        links[i].prev = links[(i - 1) % n]
    return links


def count_clockwise(start: DoubleLink, steps: int) -> DoubleLink:
    """Count `steps` people clockwise from `start` (inclusive, step 1 = start)."""
    current = start
    for _ in range(steps - 1):
        current = current.next
    return current


def distance_to_clockwise(start: DoubleLink, target: DoubleLink) -> int:
    """Physical steps going clockwise from start to target (not counting start)."""
    steps = 0
    current = start
    while current is not target:
        current = current.next
        steps += 1
    return steps


def distance_to_counter_clockwise(start: DoubleLink, target: DoubleLink) -> int:
    """Physical steps going counter-clockwise from start to target (not counting start)."""
    steps = 0
    current = start
    while current is not target:
        current = current.prev
        steps += 1
    return steps


def remove_from_circle(node: DoubleLink) -> None:
    """Remove a node from the circular doubly-linked chain."""
    node.prev.next = node.next
    node.next.prev = node.prev
    node.next = None
    node.prev = None


def advance_clockwise(node: DoubleLink, steps: int = 1) -> DoubleLink:
    """Return the node `steps` hops clockwise from `node`."""
    current = node
    for _ in range(steps):
        current = current.next
    return current


def play_game(n: int, m: int, o: int) -> None:
    """
    Simulate the circle game and print results.

    Parameters:
        n: number of people
        m: 0-based position of the initial 'it' person
        o: counting offset to find the tagged person
    """
    links = build_circle(n)

    # The person at position m is 'it'; their spot becomes the exit gap.
    # We represent the exit as a dedicated sentinel node (not a person).
    exit_node = DoubleLink("EXIT")

    it_person = links[m]

    # Insert exit_node into the circle in place of it_person.
    # exit_node takes it_person's position; it_person steps one clockwise.
    prev_node = it_person.prev
    next_node = it_person.next

    exit_node.prev = prev_node
    exit_node.next = next_node
    prev_node.next = exit_node
    next_node.prev = exit_node

    # 'it' starts one step clockwise from the exit
    it_node = next_node  # it_person is no longer in the circle

    # The circle now has n-1 people + 1 exit sentinel = n nodes total.
    # 'remaining' tracks living people only.
    remaining = n - 1

    while remaining > 1:
        # --- Count o people clockwise from it_node (exit is in the chain
        #     but is a real node; we must skip it during counting) ---
        # We need count_clockwise that skips exit_node:
        counted = 0
        current = it_node
        while counted < o:
            if current is not exit_node:
                counted += 1
            if counted < o:
                current = current.next
        tagged_node = current

        # --- Race to exit ---
        dist_it = distance_to_clockwise(it_node, exit_node)
        dist_tagged = distance_to_counter_clockwise(tagged_node, exit_node)

        if dist_it <= dist_tagged:
            # 'it' reaches exit first (or tie: 'it' escapes)
            print(f"{it_node.element} escaped!")
            escaping = it_node
            new_it = tagged_node
            # Stitch exit_node out, put escaping person's slot back? No —
            # exit_node stays; the escaping person just leaves the circle.
            remove_from_circle(escaping)
            remaining -= 1
            it_node = new_it
        else:
            # Tagged reaches exit first
            print(f"{tagged_node.element} escaped!")
            remove_from_circle(tagged_node)
            remaining -= 1
            # 'it' advances one step clockwise, skipping exit if needed
            it_node = it_node.next
            if it_node is exit_node:
                it_node = it_node.next

    print(f"{it_node.element} is the loser.")


# --- Main ---
n = int(input("n> "))
m = int(input("m> "))
o = int(input("o> "))

play_game(n, m, o)