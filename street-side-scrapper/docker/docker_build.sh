docker build $(git rev-parse --show-toplevel) \
    -f Dockerfile \
    --tag street-side-scrapper-worker \
    --target worker