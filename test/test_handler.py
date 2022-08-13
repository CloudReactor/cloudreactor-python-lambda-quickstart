from functions.handler import make_result

class TestHandler:
    def test_make_result(self):
        x = make_result('Done')
        assert x == 'Done -- SUCCESS!'
