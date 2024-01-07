import pytest

from .responses import mock_responses_from_hf


@pytest.fixture()
def atfbooru(httpx_mock):
    with mock_responses_from_hf('atfbooru', httpx_mock):
        yield


@pytest.fixture()
def danbooru(httpx_mock):
    with mock_responses_from_hf('danbooru', httpx_mock):
        yield


@pytest.fixture()
def duitang_nian(httpx_mock):
    with mock_responses_from_hf('duitang_nian', httpx_mock):
        yield


@pytest.fixture()
def duitang_nian_non_strict(httpx_mock):
    with mock_responses_from_hf('duitang_nian_non_strict', httpx_mock):
        yield


@pytest.fixture()
def e621_amiya(httpx_mock):
    with mock_responses_from_hf('e621_amiya', httpx_mock):
        yield


@pytest.fixture()
def e621_surtr(httpx_mock):
    with mock_responses_from_hf('e621_surtr', httpx_mock):
        yield


@pytest.fixture()
def e926_amiya(httpx_mock):
    with mock_responses_from_hf('e926_amiya', httpx_mock):
        yield


@pytest.fixture()
def e926_surtr(httpx_mock):
    with mock_responses_from_hf('e926_surtr', httpx_mock):
        yield


@pytest.fixture()
def gelbooru_2dogs(httpx_mock):
    with mock_responses_from_hf('gelbooru_2dogs', httpx_mock):
        yield


@pytest.fixture()
def gelbooru_surtr(httpx_mock):
    with mock_responses_from_hf('gelbooru_surtr', httpx_mock):
        yield


@pytest.fixture()
def huashi6_nian(httpx_mock):
    with mock_responses_from_hf('huashi6_nian', httpx_mock):
        yield


@pytest.fixture()
def hypnohub_2dogs(httpx_mock):
    with mock_responses_from_hf('hypnohub_2dogs', httpx_mock):
        yield


@pytest.fixture()
def hypnohub_surtr(httpx_mock):
    with mock_responses_from_hf('hypnohub_surtr', httpx_mock):
        yield


@pytest.fixture()
def konachan_2dogs(httpx_mock):
    with mock_responses_from_hf('konachan_2dogs', httpx_mock):
        yield


@pytest.fixture()
def konachan_net_2dogs(httpx_mock):
    with mock_responses_from_hf('konachan_net_2dogs', httpx_mock):
        yield


@pytest.fixture()
def konachan_net_surtr(httpx_mock):
    with mock_responses_from_hf('konachan_net_surtr', httpx_mock):
        yield


@pytest.fixture()
def konachan_surtr(httpx_mock):
    with mock_responses_from_hf('konachan_surtr', httpx_mock):
        yield


@pytest.fixture()
def lolibooru_2dogs(httpx_mock):
    with mock_responses_from_hf('lolibooru_2dogs', httpx_mock):
        yield


@pytest.fixture()
def lolibooru_surtr(httpx_mock):
    with mock_responses_from_hf('lolibooru_surtr', httpx_mock):
        yield


@pytest.fixture()
def paheal_surtr(httpx_mock):
    with mock_responses_from_hf('paheal_surtr', httpx_mock):
        yield


@pytest.fixture()
def realbooru_thong(httpx_mock):
    with mock_responses_from_hf('realbooru_thong', httpx_mock):
        yield


@pytest.fixture()
def rule34_2dogs(httpx_mock):
    with mock_responses_from_hf('rule34_2dogs', httpx_mock):
        yield


@pytest.fixture()
def rule34_surtr(httpx_mock):
    with mock_responses_from_hf('rule34_surtr', httpx_mock):
        yield


@pytest.fixture()
def safebooru(httpx_mock):
    with mock_responses_from_hf('safebooru', httpx_mock):
        yield


@pytest.fixture()
def safebooru_org_2dogs(httpx_mock):
    with mock_responses_from_hf('safebooru_org_2dogs', httpx_mock):
        yield


@pytest.fixture()
def safebooru_org_surtr(httpx_mock):
    with mock_responses_from_hf('safebooru_org_surtr', httpx_mock):
        yield


@pytest.fixture()
def sankaku_2dogs(httpx_mock):
    with mock_responses_from_hf('sankaku_2dogs', httpx_mock):
        yield


@pytest.fixture()
def sankaku_surtr(httpx_mock):
    with mock_responses_from_hf('sankaku_surtr', httpx_mock):
        yield


@pytest.fixture()
def sankaku_texas_yuri(httpx_mock):
    with mock_responses_from_hf('sankaku_texas_yuri', httpx_mock):
        yield


@pytest.fixture()
def tbib_2dogs(httpx_mock):
    with mock_responses_from_hf('tbib_2dogs', httpx_mock):
        yield


@pytest.fixture()
def tbib_surtr(httpx_mock):
    with mock_responses_from_hf('tbib_surtr', httpx_mock):
        yield


@pytest.fixture()
def threedbooru_misaka_mikoto(httpx_mock):
    with mock_responses_from_hf('threedbooru_misaka_mikoto', httpx_mock):
        yield


@pytest.fixture()
def xbooru_2dogs(httpx_mock):
    with mock_responses_from_hf('xbooru_2dogs', httpx_mock):
        yield


@pytest.fixture()
def xbooru_surtr(httpx_mock):
    with mock_responses_from_hf('xbooru_surtr', httpx_mock):
        yield


@pytest.fixture()
def yande_2dogs(httpx_mock):
    with mock_responses_from_hf('yande_2dogs', httpx_mock):
        yield


@pytest.fixture()
def yande_surtr(httpx_mock):
    with mock_responses_from_hf('yande_surtr', httpx_mock):
        yield


@pytest.fixture()
def zerochan_amiya_login(httpx_mock):
    with mock_responses_from_hf('zerochan_amiya_login', httpx_mock):
        yield


@pytest.fixture()
def zerochan_amiya_login_strict(httpx_mock):
    with mock_responses_from_hf('zerochan_amiya_login_strict', httpx_mock):
        yield


@pytest.fixture()
def zerochan_camilla_strict(httpx_mock):
    with mock_responses_from_hf('zerochan_camilla_strict', httpx_mock):
        yield


@pytest.fixture()
def zerochan_surtr(httpx_mock):
    with mock_responses_from_hf('zerochan_surtr', httpx_mock):
        yield


@pytest.fixture()
def zerochan_surtr_full(httpx_mock):
    with mock_responses_from_hf('zerochan_surtr_full', httpx_mock):
        yield


@pytest.fixture()
def zerochan_surtr_strict(httpx_mock):
    with mock_responses_from_hf('zerochan_surtr_strict', httpx_mock):
        yield
