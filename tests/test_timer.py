from parsers.timer import Timer


class TestTimer:

    def test_timer(self):  # tests for when start time has a value (not none)
        timer = Timer('Pairings')

        assert timer == Timer(name='Pairings', text='Elapsed time: {:0.4f} seconds')

    def test_start_time_is_none(self):
        timer = Timer()
        nil_time = None
        assert nil_time == timer.start()

    # def test_stop_time_when_start_time_is_none(self):
