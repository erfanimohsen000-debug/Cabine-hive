"""Envelope study for the mobile cabin hive (see docs/requirements-register.md).

All dimensions in mm, masses in kg. Values marked A-xx are assumptions
listed in docs/study-01-layout.md and must be confirmed before detailing.
"""

FRAMES = {
    # name: (frame height, box/floor height, full-frame mass)
    "deep": (232, 244, 3.6),
    "medium": (159, 168, 2.3),
}
TOP_BAR = 483           # Langstroth top bar length
PITCH = 35              # self-spacing frame pitch

CASSETTE_END = 20       # A-01 cassette end bars carrying the lugs (each end)
CASSETTE_SIDE = 25      # A-02 cassette side member + telescopic slide (each side)
CASSETTE_BAR = 20       # A-03 vertical add per floor for cassette structure
BEE_SPACE = 8           # A-04 clearance around cassette
DIVIDER = 20            # A-05 follower/division board for winter reduction
BOTTOM = 60             # A-06 screened bottom + debris tray
TOP = 40                # A-07 top space / inner cover / feeder
PARTITION = 25          # A-08 wall between neighbouring compartments
TIER_FLOOR = 100        # A-09 floor between rows; Q-09: min. 100 mm
OUTER_WALL = 100        # A-10 multilayer insulated outer wall
AISLE_WALL = 40         # A-11 aisle-side door/wall of each compartment
ROOF = FLOOR = 150      # A-12 insulated roof / floor
GROUND = 300            # A-13 body underside to ground (axles at the ends, see study-02)
ROOF_LUGS = 120         # A-15 crane lifting lugs above the roof (R-01)
TYRE_SIDE = 265         # A-16 tyre width + clearance, only if wheels sit beside the body

# Legal limits without an oversize permit (study-02). Width includes wheels.
LIMITS = {
    "Canada (MOU 2019)": {"width": 2600, "height": 4150},
    "Iran": {"width": 2600, "height": 4500},
    "Iran, Chalus/Haraz": {"width": 2600, "height": 3800},
}
WIDTH_LIMIT = min(l["width"] for l in LIMITS.values())
HEIGHT_LIMIT = min(l["height"] for l in LIMITS.values())

ROWS_PER_SIDE, COLS = 3, 5


def option(name, floors, wheels_beside=False):
    """floors: list of (frame type, frames per floor)."""
    n = max(c for _, c in floors)
    depth = TOP_BAR + 2 * CASSETTE_END + 2 * BEE_SPACE          # perpendicular to aisle
    width = n * PITCH + DIVIDER + 2 * CASSETTE_SIDE + 2 * BEE_SPACE  # along trailer
    height = BOTTOM + TOP + sum(FRAMES[t][1] + CASSETTE_BAR for t, _ in floors)
    tier = height + TIER_FLOOR

    length = COLS * width + (COLS - 1) * PARTITION + 2 * OUTER_WALL
    side = depth + OUTER_WALL + AISLE_WALL
    body_w = WIDTH_LIMIT - (2 * TYRE_SIDE if wheels_beside else 0)
    aisle = body_w - 2 * side
    body_h = ROWS_PER_SIDE * tier - TIER_FLOOR + ROOF + FLOOR
    cassette_kg = max(FRAMES[t][2] * c for t, c in floors)
    colony_kg = sum(FRAMES[t][2] * c for t, c in floors)
    # top of the upper cassette of the top tier, measured from the aisle floor
    top_reach = body_h - ROOF - TOP
    return {
        "option": name,
        "comp_int WxDxH": f"{width}x{depth}x{height}",
        "body L": length,
        "body W": body_w,
        "aisle": aisle,
        "body H": body_h,
        "total H": body_h + GROUND + ROOF_LUGS,
        "H margin": HEIGHT_LIMIT - (body_h + GROUND + ROOF_LUGS),
        "max cassette kg": round(cassette_kg),
        "top reach": top_reach,
        "frames mass t": round(30 * colony_kg / 1000, 2),
    }


OPTIONS = [
    option("A: 2x15 deep (Q-23)", [("deep", 15), ("deep", 15)]),
    option("A, wheels beside body", [("deep", 15), ("deep", 15)], wheels_beside=True),
    option("B: 15 deep + 15 medium", [("deep", 15), ("medium", 15)]),
    option("C: 3x10 deep", [("deep", 10)] * 3),
    option("D: 1x30 deep", [("deep", 30)]),
]

if __name__ == "__main__":
    keys = list(OPTIONS[0])
    print(" | ".join(keys))
    for o in OPTIONS:
        print(" | ".join(str(o[k]) for k in keys))
