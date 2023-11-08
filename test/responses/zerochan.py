import os

from test.responses import resp_recorder
from waifuc.source import ZerochanSource


@resp_recorder()
def zerochan_surtr():
    source = ZerochanSource('Surtr (Arknights)')
    _ = list(source[:10])


@resp_recorder()
def zerochan_surtr_full():
    source = ZerochanSource('Surtr (Arknights)', select='full')
    _ = list(source[:10])


@resp_recorder()
def zerochan_surtr_strict():
    source = ZerochanSource('Surtr (Arknights)', strict=True)
    _ = list(source[:10])


@resp_recorder()
def zerochan_camilla_strict():
    source = ZerochanSource('Camilla (Fire Emblem)', strict=True)
    _ = list(source[:10])


@resp_recorder()
def zerochan_amiya_login():
    source = ZerochanSource(
        'Amiya',
        username=os.environ['ZEROCHAN_USERNAME'],
        password=os.environ['ZEROCHAN_PASSWORD'],
    )
    _ = list(source[:10])


@resp_recorder()
def zerochan_amiya_login_strict():
    source = ZerochanSource(
        'Amiya',
        username=os.environ['ZEROCHAN_USERNAME'],
        password=os.environ['ZEROCHAN_PASSWORD'],
        strict=True,
    )
    _ = list(source[:10])
