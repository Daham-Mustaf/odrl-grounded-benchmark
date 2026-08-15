from gen_bcp47    import generate_bcp47000
from gen_dpv      import generate_dpv000
from gen_geonames import generate_gn000

# Each takes a TTL path arg, no fixed expected count
RESOURCES = [
    ("BCP47000-0.ax", generate_bcp47000, "Resources/bcp47.ttl"),
    ("DPV000-0.ax",   generate_dpv000,   "Resources/dpv.ttl"),
    ("GN000-0.ax",    generate_gn000,    "Resources/geonames.ttl"),
]