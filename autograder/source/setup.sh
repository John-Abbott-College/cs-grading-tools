#!/usr/bin/env bash

YJ_VERSION=v5.1.0
PLATFORM=linux-amd64

apt-get update

# Xvfb: X-server virtual framebuffer
# Enables headless use of graphics libraries e.g. turtle, matplotlib
apt-get install -y xvfb

# Utilities for installing libraries and parsing json
apt-get install -y curl wget jq

# yj: convert between json/toml/yaml
wget https://github.com/sclevine/yj/releases/download/${YJ_VERSION}/yj_${PLATFORM} -O /usr/local/bin/yj

# uv: used to install required python versions and libraries
curl -LsSf https://astral.sh/uv/install.sh | sh
