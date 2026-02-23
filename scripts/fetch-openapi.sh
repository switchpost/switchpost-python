#!/usr/bin/env bash
# Fetch the OpenAPI spec from switchpost-spec (the single source of truth).
#
# Local dev: copies from sibling directory ../switchpost-spec/
# CI:        downloads from GitHub at a pinned tag
set -euo pipefail

REPO="switchpost/switchpost-spec"
TAG="${OPENAPI_TAG:-latest}"
OUTPUT="openapi.json"
LOCAL_PATH="../switchpost-spec/openapi.json"

if [ "$TAG" = "latest" ] && [ -f "$LOCAL_PATH" ]; then
  echo "Copying from local switchpost-spec..."
  cp "$LOCAL_PATH" "$OUTPUT"
elif command -v gh &>/dev/null; then
  echo "Downloading from GitHub ($REPO @ $TAG)..."
  if [ "$TAG" = "latest" ]; then
    gh release download --repo "$REPO" --pattern openapi.json --output "$OUTPUT" --clobber
  else
    gh release download "$TAG" --repo "$REPO" --pattern openapi.json --output "$OUTPUT" --clobber
  fi
else
  echo "Error: gh CLI not found and no local switchpost-spec directory available."
  exit 1
fi

echo "Wrote $OUTPUT ($(wc -c < "$OUTPUT" | tr -d ' ') bytes)"
