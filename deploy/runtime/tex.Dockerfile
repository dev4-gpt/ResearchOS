FROM texlive/texlive@sha256:3a3949a847929f989eb70a4c92ba43b38dcd4242e08a8a6a0b6f5ef3db1525ee
COPY texmf/ /opt/researchingos/texmf/
ENV TEXMFHOME=/opt/researchingos/texmf
RUN kpsewhich IEEEtran.cls && kpsewhich IEEEtran.bst && pdflatex --version && bibtex --version
