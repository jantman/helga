from mock import Mock
from pretend import stub

from helga.plugins import stfu


def test_stfu_preprocess_does_nothing():
    stfu.silenced = set()
    chan, nick, msg = stfu.stfu.preprocess(None, '#bots', 'me', 'foo')
    assert msg == 'foo'


def test_stfu_preprocess_blanks_message_when_silenced():
    stfu.silenced = set(['#bots'])
    chan, nick, msg = stfu.stfu.preprocess(None, '#bots', 'me', 'foo')
    assert msg == ''


def test_stfu_snark_on_private_message():
    stfu.silenced = set()
    resp = stfu.stfu.process(stub(nickname='helga'), 'me', 'me', 'helga stfu')
    assert resp in map(lambda x: x.format(nick='me'), stfu.snarks)


def test_stfu_silences_channel():
    stfu.silenced = set()
    resp = stfu.stfu.process(stub(nickname='helga'), '#bots', 'me', 'helga stfu')
    assert resp in map(lambda x: x.format(nick='me'), stfu.silence_acks)
    assert '#bots' in stfu.silenced


def test_stfu_unsilences_channel():
    stfu.silenced = set(['#bots'])
    resp = stfu.stfu.process(stub(nickname='helga'), '#bots', 'me', 'helga speak')
    assert resp in map(lambda x: x.format(nick='me'), stfu.unsilence_acks)
    assert '#bots' not in stfu.silenced