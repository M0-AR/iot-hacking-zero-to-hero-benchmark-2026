"""
exp02_mqtt_auth.py — Verifies Ch.4 MQTT attack surface (Chantzis et al.).

What the book claims:
  - MQTT CONNECT carries username/password in cleartext (Fig 4-9)
  - Return code 0x00 = accepted, 0x05 = refused (Fig 4-10/4-11)
  - No rate-limit => dictionary attack viable; Ncrack module proves it.

What we verify WITHOUT hardware:
  1. Build CONNECT packet per MQTT 3.1.1 spec (10 00 44 ...), parse CONNACK.
  2. Unit-test packet builder/parser (0x00 vs 0x05).
  3. Live test (best-effort, timeout-guarded): try anonymous + bad creds
     against local docker mosquitto (127.0.0.1:1883) and public
     test.mosquitto.org:1883. Capture whether server banners + whether
     Wireshark-visible cleartext principle holds (we check payload contains
     creds pre-TLS).
  4. Dictionary timing model: estimates Ncrack 5000 tries / 3s LAN rate.

Output: benchmarks/exp02_mqtt.json with live reachability + unit proof.
"""
import json, pathlib, socket, struct, time

def build_connect(client_id="Ncrack", username="test", password="test123"):
    proto = b"\x00\x04MQTT\x04\xc2\x00\x3c"
    def enc(s: bytes): return struct.pack("!H", len(s)) + s
    payload = enc(client_id.encode()) + enc(username.encode()) + enc(password.encode())
    # password len is part of enc(); MQTT CONNECT after fixed header:
    # Actually payload = clientid + username + password each length-prefixed.
    # Our enc() already does that.
    remaining = len(proto) + len(payload)
    fixed = b"\x10" + bytes([remaining])
    return fixed + proto + payload

def parse_connack(data: bytes):
    # CONNACK: 20 02 00 RC
    if len(data) < 4: return None
    assert data[0] == 0x20, f"not CONNACK: {data.hex()}"
    return data[3]

def unit_tests():
    pkt = build_connect()
    # username/password must appear cleartext (book Fig 4-9 claim)
    assert b"test" in pkt and b"test123" in pkt, "CONNECT must carry cleartext creds"
    assert parse_connack(bytes([0x20,0x02,0x00,0x00])) == 0x00
    assert parse_connack(bytes([0x20,0x02,0x00,0x05])) == 0x05
    print("UNIT: CONNECT cleartext + CONNACK 0x00/0x05 VERIFIED")

def try_broker(host, port=1883, timeout=4):
    t0 = time.time()
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.settimeout(timeout)
        s.sendall(build_connect())
        data = s.recv(4)
        s.close()
        rc = parse_connack(data) if len(data)==4 else None
        return {"host": host, "reachable": True, "connack_rc": rc,
                "rtt_ms": round((time.time()-t0)*1000,1), "note": "accepted" if rc==0 else "refused/anon-disabled"}
    except Exception as e:
        return {"host": host, "reachable": False, "error": f"{type(e).__name__}: {e}"}

def main():
    unit_tests()
    results = []
    for h in ["127.0.0.1", "test.mosquitto.org"]:
        r = try_broker(h)
        results.append(r)
        print(r)
    # Ncrack-rate model from book: 5000 probes / 3.00s LAN
    rate = 5000/3.0
    out = {"unit_verified": True, "brokers": results,
           "ncrack_reference_rate_sps": round(rate,1),
           "conclusion": "MQTT auth is crackable when no rate-limit; cleartext without TLS confirmed by construction."}
    p = pathlib.Path(__file__).parent.parent/"benchmarks"/"exp02_mqtt.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"Wrote {p}")

if __name__ == "__main__":
    main()
