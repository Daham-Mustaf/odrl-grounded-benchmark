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

FROM python:3.13-slim

# z3 from Debian; vampire from a release binary, since it has no
# package and building it needs a C++ toolchain we would then ship.
RUN apt-get update && apt-get install -y --no-install-recommends \
        z3 \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Pin the Vampire release. Check the tag against what you ran locally:
# the suite's certificates record which prover produced them, and a
# different version may find a different proof of the same verdict.
ARG VAMPIRE_TAG=v4.9casc2024
ARG VAMPIRE_ASSET=vampire
RUN wget -q --show-progress \
      "https://github.com/vprover/vampire/releases/download/${VAMPIRE_TAG}/${VAMPIRE_ASSET}" \
      -O /usr/local/bin/vampire \
    && chmod +x /usr/local/bin/vampire \
    && vampire --version

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