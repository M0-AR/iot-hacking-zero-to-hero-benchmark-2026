"""
run_all.py — Zero-to-hero runner: executes exp01..exp07, aggregates scoreboard.
Produces benchmarks/summary.json + prints PASS/FAIL per book chapter.
Exit 0 only if every unit_verified == True (CI-gate for 'verified, not hand-waved').
"""
import subprocess, sys, json, pathlib

EXPS = ["exp01_threat_model_dread.py", "exp02_mqtt_auth.py", "exp03_upnp_ssdp.py",
        "exp04_firmware_static.py", "exp05_lorawan_bitflip.py", "exp06_wifi_pmkid.py",
        "exp07_rfid_ble.py"]

def main():
    base = pathlib.Path(__file__).parent
    results = []
    ok_all = True
    for e in EXPS:
        print(f"\n=== {e} ===")
        r = subprocess.run([sys.executable, str(base/e)], capture_output=True, text=True)
        print(r.stdout[-2000:])
        if r.returncode != 0:
            print(r.stderr[-2000:]); ok_all = False
            results.append({"exp": e, "pass": False})
        else:
            results.append({"exp": e, "pass": True})
    # Aggregate benchmark JSONs
    bench = pathlib.Path(__file__).parent.parent/"benchmarks"
    agg = {"experiments": results, "details": {}}
    for f in bench.glob("exp*.json"):
        try: agg["details"][f.name] = json.loads(f.read_text())
        except Exception as ex: agg["details"][f.name] = {"error": str(ex)}
    agg["all_pass"] = ok_all and all(x["pass"] for x in results)
    (bench/"summary.json").write_text(json.dumps(agg, indent=2))
    print("\n" + json.dumps({"all_pass": agg["all_pass"], "experiments": results}, indent=2))
    sys.exit(0 if agg["all_pass"] else 1)

if __name__ == "__main__":
    main()
