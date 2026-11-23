FROM python@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704 AS python
WORKDIR /build
COPY writer-requirements.lock .
RUN python -m pip install --disable-pip-version-check --no-cache-dir \
    --require-hashes --only-binary=:all: --prefix=/opt/dependencies -r writer-requirements.lock

FROM texlive/texlive@sha256:3a3949a847929f989eb70a4c92ba43b38dcd4242e08a8a6a0b6f5ef3db1525ee
COPY --from=python /usr/local/ /usr/local/
COPY --from=python /opt/dependencies/ /usr/local/
COPY texmf/ /opt/researchingos/texmf/
COPY writer_entrypoint.py /opt/researchingos/writer_entrypoint.py
ENV TEXMFHOME=/opt/researchingos/texmf PYTHONDONTWRITEBYTECODE=1
RUN /usr/local/bin/python -c 'import cv2, fitz, pymupdf4llm; from google import genai' && kpsewhich IEEEtran.cls
ENTRYPOINT ["/usr/local/bin/python", "/opt/researchingos/writer_entrypoint.py"]
