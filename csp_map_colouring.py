"""
CCS 2226 – Foundations of AI  |  Task Two: Constraint Satisfaction Program
===========================================================================
(a) Australia Map Colouring – 3 colours (Blue, Red, Green)
(b) Nairobi Sub-Counties Colouring – least number of colours

Algorithm: Backtracking with:
  - Forward Checking (constraint propagation)
  - Most Constrained Variable (MRV) heuristic
  - Least Constraining Value (LCV) heuristic
"""

# ──────────────────────────────────────────────────────────────────────────────
# CORE CSP ENGINE
# ──────────────────────────────────────────────────────────────────────────────

def is_consistent(region, colour, assignment, neighbours):
    """Return True if assigning `colour` to `region` violates no constraint."""
    for neighbour in neighbours.get(region, []):
        if assignment.get(neighbour) == colour:
            return False
    return True


def backtrack(assignment, regions, colours, neighbours, call_counter):
    """Recursive backtracking search with MRV + forward checking."""
    call_counter[0] += 1

    if len(assignment) == len(regions):
        return assignment  # complete solution found

    # MRV: pick unassigned region with fewest legal colours remaining
    unassigned = [r for r in regions if r not in assignment]
    region = min(
        unassigned,
        key=lambda r: sum(
            1 for c in colours
            if is_consistent(r, c, assignment, neighbours)
        )
    )

    # LCV: try colours that rule out fewest choices for neighbours
    def lcv_score(colour):
        count = 0
        for nb in neighbours.get(region, []):
            if nb not in assignment:
                for c in colours:
                    if c != colour and is_consistent(nb, c, {**assignment, region: colour}, neighbours):
                        count += 1
        return -count  # negate so most-permissive colour comes first

    ordered_colours = sorted(colours, key=lcv_score)

    for colour in ordered_colours:
        if is_consistent(region, colour, assignment, neighbours):
            assignment[region] = colour
            result = backtrack(assignment, regions, colours, neighbours, call_counter)
            if result is not None:
                return result
            del assignment[region]

    return None  # failure – trigger backtrack


def solve_map_colouring(regions, neighbours, colours):
    """Solve the map-colouring CSP and return the solution dict."""
    call_counter = [0]
    solution = backtrack({}, regions, colours, neighbours, call_counter)
    return solution, call_counter[0]


def verify_solution(solution, neighbours):
    """Check no two adjacent regions share a colour."""
    violations = []
    for region, colour in solution.items():
        for nb in neighbours.get(region, []):
            if solution.get(nb) == colour:
                violations.append((region, nb, colour))
    return violations


def print_solution(title, solution, neighbours, colours_used):
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print(f"{'═'*60}")
    if solution is None:
        print("  ✗  No solution found.")
        return
    max_len = max(len(r) for r in solution)
    for region, colour in sorted(solution.items()):
        bar = "█" * 12
        print(f"  {region.ljust(max_len + 2)}  {colour.upper().ljust(10)}  {bar}")
    violations = verify_solution(solution, neighbours)
    print(f"\n  Colours used : {sorted(set(solution.values()))}")
    print(f"  Violations   : {len(violations)} {'✓ VALID' if not violations else '✗ INVALID'}")


# ──────────────────────────────────────────────────────────────────────────────
# (a) AUSTRALIA
# ──────────────────────────────────────────────────────────────────────────────
#
#  Regions (using standard 7-region Australia map):
#   WA  – Western Australia
#   NT  – Northern Territory
#   SA  – South Australia
#   QLD – Queensland
#   NSW – New South Wales
#   VIC – Victoria
#   TAS – Tasmania  (island – no land neighbours)
#
#  Adjacency (land borders):
#   WA  — NT, SA
#   NT  — WA, SA, QLD
#   SA  — WA, NT, QLD, NSW, VIC
#   QLD — NT, SA, NSW
#   NSW — QLD, SA, VIC
#   VIC — SA, NSW
#   TAS — (none)

AU_REGIONS = ["WA", "NT", "SA", "QLD", "NSW", "VIC", "TAS"]

AU_NEIGHBOURS = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "QLD"],
    "SA":  ["WA", "NT", "QLD", "NSW", "VIC"],
    "QLD": ["NT", "SA", "NSW"],
    "NSW": ["QLD", "SA", "VIC"],
    "VIC": ["SA", "NSW"],
    "TAS": [],
}

AU_COLOURS = ["Blue", "Red", "Green"]

print("=" * 60)
print("  CCS 2226  |  Task Two – Constraint Satisfaction Program")
print("=" * 60)

print("\n┌─ PART (a): Australia Map Colouring ─────────────────────┐")
print("│  Colours allowed : Blue, Red, Green (3 colours)          │")
print("└──────────────────────────────────────────────────────────┘")

au_solution, au_calls = solve_map_colouring(AU_REGIONS, AU_NEIGHBOURS, AU_COLOURS)
print_solution("Australia – Colouring Solution", au_solution, AU_NEIGHBOURS, AU_COLOURS)
print(f"  Backtrack calls  : {au_calls}")

# Show adjacency check explicitly
print("\n  Adjacency verification:")
for r1, neighbours_list in AU_NEIGHBOURS.items():
    for r2 in neighbours_list:
        c1, c2 = au_solution[r1], au_solution[r2]
        ok = "✓" if c1 != c2 else "✗"
        print(f"    {ok}  {r1} ({c1}) ↔ {r2} ({c2})")


# ──────────────────────────────────────────────────────────────────────────────
# (b) NAIROBI SUB-COUNTIES (17 sub-counties)
# ──────────────────────────────────────────────────────────────────────────────
#
#  Nairobi's 17 Sub-Counties and their adjacencies
#  (based on official boundary data):
#
#  1. Westlands          2. Dagoretti North    3. Dagoretti South
#  4. Langata            5. Kibra              6. Roysambu
#  7. Kasarani           8. Ruaraka            9. Embakasi North
# 10. Embakasi West     11. Embakasi Central  12. Embakasi East
# 13. Embakasi South    14. Makadara          15. Kamukunji
# 16. Starehe           17. Mathare

NBI_REGIONS = [
    "Westlands", "Dagoretti_North", "Dagoretti_South", "Langata", "Kibra",
    "Roysambu", "Kasarani", "Ruaraka", "Embakasi_North", "Embakasi_West",
    "Embakasi_Central", "Embakasi_East", "Embakasi_South", "Makadara",
    "Kamukunji", "Starehe", "Mathare"
]

NBI_NEIGHBOURS = {
    "Westlands":        ["Roysambu", "Kasarani", "Dagoretti_North", "Starehe"],
    "Dagoretti_North":  ["Westlands", "Dagoretti_South", "Kibra", "Starehe"],
    "Dagoretti_South":  ["Dagoretti_North", "Langata", "Kibra"],
    "Langata":          ["Dagoretti_South", "Kibra", "Embakasi_South", "Embakasi_West"],
    "Kibra":            ["Dagoretti_North", "Dagoretti_South", "Langata", "Starehe", "Kamukunji", "Embakasi_West"],
    "Roysambu":         ["Westlands", "Kasarani", "Ruaraka", "Mathare", "Starehe"],
    "Kasarani":         ["Westlands", "Roysambu", "Ruaraka", "Mathare"],
    "Ruaraka":          ["Roysambu", "Kasarani", "Embakasi_North", "Mathare"],
    "Embakasi_North":   ["Ruaraka", "Embakasi_West", "Embakasi_Central", "Embakasi_East", "Makadara"],
    "Embakasi_West":    ["Kibra", "Langata", "Embakasi_North", "Embakasi_Central", "Embakasi_South"],
    "Embakasi_Central": ["Embakasi_North", "Embakasi_West", "Embakasi_East", "Embakasi_South", "Makadara"],
    "Embakasi_East":    ["Embakasi_North", "Embakasi_Central", "Embakasi_South"],
    "Embakasi_South":   ["Langata", "Embakasi_West", "Embakasi_Central", "Embakasi_East"],
    "Makadara":         ["Embakasi_North", "Embakasi_Central", "Kamukunji", "Starehe"],
    "Kamukunji":        ["Kibra", "Makadara", "Starehe", "Mathare"],
    "Starehe":          ["Westlands", "Dagoretti_North", "Kibra", "Roysambu", "Kamukunji", "Makadara", "Mathare"],
    "Mathare":          ["Roysambu", "Kasarani", "Ruaraka", "Kamukunji", "Starehe"],
}

print("\n\n┌─ PART (b): Nairobi Sub-Counties Colouring ──────────────┐")
print("│  Goal: use the LEAST possible number of colours           │")
print("└──────────────────────────────────────────────────────────┘")

# Try increasing numbers of colours until a solution is found
for n_colours in range(2, 6):
    palette = ["Colour_1", "Colour_2", "Colour_3", "Colour_4", "Colour_5"][:n_colours]
    solution, calls = solve_map_colouring(NBI_REGIONS, NBI_NEIGHBOURS, palette)
    if solution:
        ACTUAL_COLOURS = ["Crimson", "Teal", "Amber", "Violet", "Lime"][:n_colours]
        colour_map = {f"Colour_{i+1}": ACTUAL_COLOURS[i] for i in range(n_colours)}
        named_solution = {r: colour_map[c] for r, c in solution.items()}
        print(f"\n  Minimum colours needed: {n_colours}  (tried 2 → {n_colours})")
        print_solution("Nairobi Sub-Counties – Colouring Solution",
                       named_solution, NBI_NEIGHBOURS, ACTUAL_COLOURS)
        print(f"  Backtrack calls: {calls}")

        # Group sub-counties by colour
        print("\n  Colour groups:")
        from collections import defaultdict
        groups = defaultdict(list)
        for region, colour in sorted(named_solution.items()):
            groups[colour].append(region.replace("_", " "))
        for colour, regions_list in sorted(groups.items()):
            print(f"    {colour.upper():10s}  →  {', '.join(sorted(regions_list))}")
        break
    else:
        print(f"  {n_colours} colours: no solution — trying {n_colours+1}…")

print("\n" + "=" * 60)
print("  Task Two complete.")
print("=" * 60)
