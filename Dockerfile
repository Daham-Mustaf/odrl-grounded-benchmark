# Reproducing the benchmark: two provers, one Python environment, and
# the vendored vocabularies.
#
#     docker build -t odrl-benchmark .
#     docker run --rm odrl-benchmark
#
# The default command rebuilds every resource from the vendored files,
# regenerates the problems, and runs both provers over all of them. It
# takes about a minute, most of it prover time.
#
# Both prover versions are pinned. A verdict is a property of the
# problem, but a timing and a proof are properties of the prover that
# produced them, and an unpinned image would report neither
# reproducibly.

# Bookworm, because its z3 package is 4.8.12, the version the suite ran;
# trixie, which the plain python:3.13-slim tag now names, has 4.13.3.
FROM python:3.13-slim-bookworm

# z3 from Debian; vampire from a release binary, since it has no
# package and building it needs a C++ toolchain we would then ship.
RUN apt-get update && apt-get install -y --no-install-recommends \
        z3=4.8.12-3.1 \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && z3 --version | grep -q "version 4.8.12 "

# Pin the Vampire release the suite ran: 5.0.1, commit 1b13eafde, the
# version full-run.sh prints. The suite's certificates record which
# prover produced them, and a different version may find a different
# proof of the same verdict.
ARG VAMPIRE_TAG=v5.0.1
ARG VAMPIRE_ASSET=vampire-Linux-X64.zip
ARG VAMPIRE_SHA256=6ff2f42ea7fb9753ee104efc3e623d5e39443190f7c82a63e1e1517bf9d2cde3
RUN wget -q --show-progress \
      "https://github.com/vprover/vampire/releases/download/${VAMPIRE_TAG}/${VAMPIRE_ASSET}" \
      -O /tmp/vampire.zip \
    && echo "${VAMPIRE_SHA256}  /tmp/vampire.zip" | sha256sum -c - \
    && python -m zipfile -e /tmp/vampire.zip /usr/local/bin \
    && rm /tmp/vampire.zip \
    && chmod +x /usr/local/bin/vampire \
    && vampire --version | grep -q "^Vampire 5.0.1 "

RUN pip install --no-cache-dir uv

WORKDIR /benchmark

# Dependencies before the source, so that editing a generator does not
# reinstall rdflib.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .

# Record what the image holds, so a reader of the output knows what
# produced it.
RUN echo "vampire: $(vampire --version 2>&1 | head -1)" > /benchmark/ENVIRONMENT \
    && echo "z3:      $(z3 --version)" >> /benchmark/ENVIRONMENT \
    && echo "python:  $(python --version)" >> /benchmark/ENVIRONMENT

CMD ["bash", "docker-run.sh"]