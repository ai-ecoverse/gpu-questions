"""Minimal RunPod REST client. Reads RUNPOD_API_KEY from .env.local; never prints it.

  python scripts/runpod_api.py create NAME      # start a GPU pod with SSH
  python scripts/runpod_api.py get POD_ID       # status, ip, ssh port
  python scripts/runpod_api.py list
  python scripts/runpod_api.py delete POD_ID    # terminate (stops billing)
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://rest.runpod.io/v1"


def key():
    for line in (ROOT / ".env.local").read_text().splitlines():
        if line.startswith("RUNPOD_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("RUNPOD_API_KEY missing from .env.local")


def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json",
                                          # Cloudflare rejects urllib's default User-Agent (error 1010).
                                          "User-Agent": "gpu-questions/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            text = r.read().decode()
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:2000]}")
    return json.loads(text) if text.strip() else {}


def summary(p):
    return {k: p.get(k) for k in ("id", "name", "desiredStatus", "costPerHr", "vcpuCount", "memoryInGb",
                                  "publicIp", "portMappings")} | {"gpu": (p.get("gpu") or {}).get("displayName")}


def main():
    cmd, *rest = sys.argv[1:]
    if cmd == "create":
        # create NAME [--big]: --big asks for a 48 GB card and 32 vCPUs (ten student folds at once)
        pub = (Path.home() / ".ssh" / "id_ed25519.pub").read_text().strip()
        # --vcpu N and --community relax the request when Secure Cloud is full.
        big = "--big" in rest
        vcpu = int(rest[rest.index("--vcpu") + 1]) if "--vcpu" in rest else (32 if big else 16)
        names = [a for i, a in enumerate(rest) if not a.startswith("--") and (i == 0 or rest[i - 1] != "--vcpu")]
        gpus = (["NVIDIA L40S", "NVIDIA RTX 6000 Ada Generation", "NVIDIA A40", "NVIDIA RTX A6000"] if big else
                ["NVIDIA GeForce RTX 4090", "NVIDIA GeForce RTX 5090", "NVIDIA RTX A5000", "NVIDIA GeForce RTX 3090",
                 "NVIDIA RTX A4500", "NVIDIA A40", "NVIDIA L40S", "NVIDIA RTX 6000 Ada Generation",
                 "NVIDIA RTX A6000", "NVIDIA L4"])
        body = {
            "name": names[0] if names else "gpu-questions",
            "imageName": "runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04",
            "gpuTypeIds": gpus,
            "gpuTypePriority": "custom",
            "gpuCount": 1,
            "cloudType": "COMMUNITY" if "--community" in rest else "SECURE",
            "minVCPUPerGPU": vcpu,
            "minRAMPerGPU": 64 if big else 48,
            "containerDiskInGb": 40,
            "volumeInGb": 0,
            "ports": ["22/tcp"],
            "supportPublicIp": True,
            "env": {"PUBLIC_KEY": pub},
        }
        print(json.dumps(summary(call("POST", "/pods", body)), indent=1))
    elif cmd == "get":
        print(json.dumps(summary(call("GET", f"/pods/{rest[0]}")), indent=1))
    elif cmd == "list":
        print(json.dumps([summary(p) for p in call("GET", "/pods")], indent=1))
    elif cmd == "delete":
        call("DELETE", f"/pods/{rest[0]}")
        print("deleted", rest[0])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
