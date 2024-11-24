from earningscall.errors import InsufficientApiAccessError


def test_errors():
    ##
    error = InsufficientApiAccessError("You don't have access")
    ##
    assert error.msg == "You don't have access"
    assert str(error) == "You don't have access"
    ##
    error = InsufficientApiAccessError()
    ##
    assert error.msg is None
    assert str(error) == ""
