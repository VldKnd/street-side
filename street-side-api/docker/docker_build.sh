docker build $(git rev-parse --show-toplevel) \
    -f Dockerfile \
    --tag street-side-api-worker \
    --target worker