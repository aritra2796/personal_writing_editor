from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="tiiuae/falcon-7b-instruct",
    local_dir="./models/falcon-7b",
    local_dir_use_symlinks=False
)