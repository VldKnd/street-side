docker build $(git rev-parse --show-toplevel) \
    -f Dockerfile \
    --tag street-side-frontend \
    --target production