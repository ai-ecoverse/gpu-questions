#!/bin/sh
# Usage: scripts/pod_setup.sh HOST PORT [--teacher]
# Copies /tmp/gqpod/bundle.tgz to a RunPod pod, installs uv and the project, and runs the tests.
set -e
host=$1 port=$2 group=${3:+--group teacher}
ssh="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=30 -p $port root@$host"
scp -q -o StrictHostKeyChecking=accept-new -P "$port" /tmp/gqpod/bundle.tgz "root@$host:/root/"
$ssh "set -e; mkdir -p /root/gq && cd /root/gq && tar xzf ../bundle.tgz 2>/dev/null
curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
export PATH=\$HOME/.local/bin:\$PATH
uv sync --group dev $group >/dev/null 2>&1
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
.venv/bin/python -m pytest -q tests 2>&1 | tail -1"
