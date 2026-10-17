"""Prepare the connected VLM task without GPU jobs or model calls."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from services.vlm_research import VLMResearchService


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ingest-pdfs', action='store_true', help='Ingest all pages of local original PDFs into the vault.')
    parser.add_argument('--sample-per-group', type=int, default=30)
    args = parser.parse_args()
    result = VLMResearchService().prepare(args.sample_per_group, args.ingest_pdfs)
    print(json.dumps({'run_id': result['run_id'], 'status': result['status'],
                      'bundles': len(result['bundles']), 'papers_ingested': len(result['papers_ingested']),
                      'blinded_queue_rows': result['blinded_queue_rows'],
                      'blinded_queue_path': result['blinded_queue_path']}, indent=2))


if __name__ == '__main__':
    main()
