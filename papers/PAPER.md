# PhD-Ready Paper Draft — From Practitioner Methodology to Verifiable IoT Science

This folder holds the publication skeleton. The full narrative lives in
`../README.md` (which is itself the paper). Use this file as the
conference submission front-matter.

## Title

**Verifying Practical IoT Hacking End-to-End: A Hardware-Free Reproducible
Benchmark Spanning Threat Modeling to Smart-Home Chains with Live 2026
Validation and a Cross-Layer Authentication-Confusion Finding**

## Authors (placeholder)

Independent Reproduction Lab — contact via repo issues.

## Venue targets

- USENIX Security (Artifacts), IEEE S&P (Tools), NDSS (Measurements)
- Electronics/MDPI IoT special issue (IoTFuzzBench/IoTBenchSL lineage)
- Black Hat Arsenal / DEF CON Demo Labs (hands-on zero-to-hero)

## Contributions (claim checklist for reviewers)

1. 7 hardware-free oracles covering Ch.2,4,6,9,10,11,12,13 of Chantzis et al.
2. Live 2026 validation: public MQTT broker RC 0x05, GitHub firmware releases reachable, PMKID vector byte-identical to book.
3. Novel synthesis: discovery-identifier-as-authenticator confusion across 6 protocols.
4. One-command reproduction: `docker compose up` + `python experiments/run_all.py`.
5. Negative-result discipline: 0 UPnP replies in hardened CI reported as datum.

## Structure (8 pages + appendix)

1. Intro (Mirai → CRA → reproducibility crisis)
2. Background (ISTG/FSTM/ETS I TR 104 287/IoTFuzzBench/IoTBenchSL/IoTVulBench)
3. Method (falsifiable predicates, verify-before-commit, ethics)
4. Experiments (table + per-RQ results)
5. Hidden pattern + mitigations (mutual auth, per-device keys, MIC-before-act)
6. Limitations & future (HW UART/JTAG/SWD, SDR jamming, EAP-TTLS, large-scale fuzzing)
7. Related work (full citations in README §9)
8. Conclusion

## Artifact appendix

- `experiments/run_all.py` exit code is the artifact result.
- `benchmarks/summary.json` is the machine-readable claim registry.
- Docker images pinned; random seeds fixed; timeouts guarded.

## Future PhD extensions (pick one)

- Scale to 100-firmware corpus via IoTBenchSL pipeline + measure fuzzer recall.
- LLM-assisted decompilation (EMBA+Ghidra+LLM, Mane et al. 2025) vs. manual triage time.
- Energy-robustness (Lich, Aldini et al. 2025) correlation with exploitability.
- Cross-corpus generalization (IoTVulBench MCC 0.73) for IoT-specific CWE classifiers.
