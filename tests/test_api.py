from earningscall.api import get_user_agent


def test_get_user_agent():
    user_agent = get_user_agent()
    assert user_agent is not None
    assert "EarningsCallPython/" in user_agent
    assert "Python" in user_agent
    assert "Requests" in user_agent
