import httpx
import pytest

from services.pdf_extractor import PDFExtractionService


@pytest.mark.parametrize('url', ['http://127.0.0.1/a.pdf', 'https://arxiv.org.evil.invalid/a.pdf',
                                'https://user:password@arxiv.org/a.pdf', 'file:///etc/passwd',
                                'https://arxiv.org:8080/a.pdf'])
def test_untrusted_pdf_origins_never_reach_transport(url):
    service = PDFExtractionService()
    def forbidden(request):
        pytest.fail('Blocked URL reached transport')
    service.client = httpx.Client(transport=httpx.MockTransport(forbidden))
    assert service.extract_text_from_url(url)['error'] == 'Unsupported PDF origin'


def test_redirect_is_not_followed():
    calls = []
    def respond(request):
        calls.append(str(request.url))
        return httpx.Response(302, headers={'Location': 'http://127.0.0.1/private'})
    service = PDFExtractionService()
    service.client = httpx.Client(transport=httpx.MockTransport(respond), follow_redirects=False)
    assert not service.extract_text_from_url('https://arxiv.org/abs/1234.5678')['success']
    assert calls == ['https://arxiv.org/pdf/1234.5678']


def test_download_size_is_bounded_before_pdf_parsing():
    service = PDFExtractionService()
    service.MAX_PDF_BYTES = 5
    service.client = httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200, content=b'123456')))
    assert service.extract_text_from_url('https://arxiv.org/pdf/example')['error'] == 'PDF exceeds byte limit'
