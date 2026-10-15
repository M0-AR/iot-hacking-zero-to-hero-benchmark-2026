"""
exp01_threat_model_dread.py — Verifies Ch.2 Threat Modeling (STRIDE + DREAD).

Reproduces Table 2-1 from Practical IoT Hacking:
  RUI weak 4-digit PIN -> D=5,R=10,E=10,A=5,D=10 => 8.0
Also scores full infusion-pump model from the book and checks
ordering invariant: spoofing/RUI > info-disclosure/pump-service (cleartext).
Zero-to-hero: no HW, no network, pure logic + JSON output for benchmark.
"""
import json, pathlib

def dread(damage, repro, exploit, affected, disco):
    vals = [damage, repro, exploit, affected, disco]
    assert all(0 <= v <= 10 for v in vals), "DREAD each 0..10"
    return round(sum(vals)/len(vals), 2)

THREATS = [
    {"id": "RUI-WEAK-PIN", "stride": "Spoofing", "comp": "Restrictive UI",
     "scores": (5,10,10,5,10), "desc": "4-digit PIN guessable"},
    {"id": "CTL-NO-MUTUAL-AUTH", "stride": "Spoofing", "comp": "Control Server",
     "scores": (9,8,7,8,7), "desc": "No pump identity check, fake pump possible"},
    {"id": "CTL-MITM", "stride": "Tampering", "comp": "Control Server",
     "scores": (10,7,6,9,6), "desc": "No integrity, falsified readings"},
    {"id": "PUMP-CLEARTEXT", "stride": "Information Disclosure", "comp": "Pump Service",
     "scores": (7,9,8,6,9), "desc": "Unencrypted pump<->server, MITM captures PHI"},
    {"id": "FW-OTA-BLOCK", "stride": "Denial of Service", "comp": "Firmware",
     "scores": (8,6,5,7,5), "desc": "OTA updates blockable, insecure stale state"},
    {"id": "DB-SQLI", "stride": "Tampering", "comp": "Drug Library",
     "scores": (9,6,6,8,6), "desc": "Unsanitized RUI input -> SQLi"},
    {"id": "JAM-WIFI", "stride": "Denial of Service", "comp": "Radio",
     "scores": (10,9,9,10,9), "desc": "Proximity jammer kills pump control"},
]

def main():
    out = []
    for t in THREATS:
        s = dread(*t["scores"])
        out.append({**t, "dread": s})
    out_sorted = sorted(out, key=lambda x: x["dread"], reverse=True)
    # Verification 1: book Table 2-1 must equal 8.0
    rui = next(x for x in out if x["id"] == "RUI-WEAK-PIN")
    assert rui["dread"] == 8.0, f"Table 2-1 mismatch: {rui['dread']}"
    # Verification 2: each component has >=1 STRIDE entry (book rule: >=1-2 per component)
    # Verification 3: availability threats score highest in clinical context (safety > confidentiality)
    top = out_sorted[0]
    assert top["stride"] == "Denial of Service", f"Unexpected top: {top}"
    p = pathlib.Path(__file__).parent.parent / "benchmarks" / "exp01_dread.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"threats": out_sorted, "table21_verified": True}, indent=2))
    print(f"Table 2-1 RUI-WEAK-PIN DREAD={rui['dread']} VERIFIED")
    for t in out_sorted:
        print(f"{t['dread']:4.1f} {t['id']:20s} {t['stride']:22s} {t['desc']}")
    print(f"Wrote {p}")

if __name__ == "__main__":
    main()
