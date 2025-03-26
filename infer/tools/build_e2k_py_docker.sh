# ビルド時にdocker内で実行するスクリプト。
# これをホスト環境で実行しないでください。

set -ex

if [ -z "$DOCKER" ]; then
    echo "このスクリプトはdocker内で実行してください"
    exit 1
fi

# 環境構築
apt-get install -y rsync
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -LsSf https://sh.rustup.rs | sh -s -- -y --profile minimal
export PATH=$HOME/.cargo/bin:$HOME/.local/bin:$PATH

# ファイルをコピー
mkdir /work
cat <<EOF > /work/copy_excludes.txt
.venv
target
__pycache__
dist
.pytest_cache
EOF
rsync -av --exclude-from=/work/copy_excludes.txt /mnt/infer/ /work

# ビルド
cd /work/tools
uv run ./build_e2k_py.py --wheel --version $VERSION --skip-notice

# tarにまとめて出力
cd /work/target/wheels
tar -czvf /mnt/wheels.tar.gz .
