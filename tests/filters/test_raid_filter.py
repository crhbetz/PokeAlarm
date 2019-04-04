from datetime import datetime, timedelta
import time
import unittest
import PokeAlarm.Filters as Filters
import PokeAlarm.Events as Events


class TestRaidFilter(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def gen_filter(self, settings):
        """ Generate a generic filter with given settings. """
        return Filters.RaidFilter(self._mgr, "testfilter", settings)

    def gen_event(self, values):
        """ Generate a generic raid, overriding with an specific values. """
        settings = {
            "gym_id": "OWNmOTFmMmM0YTY3NGQwYjg0Y2I1N2JlZjU4OWRkMTYuMTY=",
            "url": "???",
            "name": "Unknown",
            "description": "???",
            "pokemon_id": 150,
            "cp": 12345,
            "move_1": 123,
            "move_2": 123,
            "start": 1499244052,
            "end": 1499246052,
            "level": 5,
            "latitude": 37.7876146,
            "longitude": -122.390624,
            "sponsor": None,
            "park": None,
            "is_ex_raid_eligible": None
        }
        settings.update(values)
        return Events.RaidEvent(settings)

    @generic_filter_test
    def test_monster_id(self):
        # Create the filters
        settings = {"monsters": [382, "383", "Rayquaza"]}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({"pokemon_id": 382}))
        pass2 = Events.RaidEvent(generate_raid({"pokemon_id": 383}))
        pass3 = Events.RaidEvent(generate_raid({"pokemon_id": 384}))
        # Test passing events
        for e in [pass1, pass2, pass3]:
            self.assertTrue(raid_filter.check_event(e))

        # Generate events that should fail
        fail1 = Events.RaidEvent(generate_raid({"pokemon_id": 20}))
        fail2 = Events.RaidEvent(generate_raid({"pokemon_id": 150}))
        fail3 = Events.RaidEvent(generate_raid({"pokemon_id": 301}))

        # Test failing events
        for e in [fail1, fail2, fail3]:
            self.assertFalse(raid_filter.check_event(e))

    def test_exclude_monster_id(self):
        # Create the filters
        settings = {"monsters_exclude": [382, "383", "Rayquaza"]}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should fail
        pass1 = Events.RaidEvent(generate_raid({"pokemon_id": 20}))
        pass2 = Events.RaidEvent(generate_raid({"pokemon_id": 150}))
        pass3 = Events.RaidEvent(generate_raid({"pokemon_id": 301}))

        # Test failing events
        for e in [pass1, pass2, pass3]:
            self.assertTrue(raid_filter.check_event(e))

        # Generate events that should pass
        fail1 = Events.RaidEvent(generate_raid({"pokemon_id": 382}))
        fail2 = Events.RaidEvent(generate_raid({"pokemon_id": 383}))
        fail3 = Events.RaidEvent(generate_raid({"pokemon_id": 384}))

        # Test passing events
        for e in [fail1, fail2, fail3]:
            self.assertFalse(raid_filter.check_event(e))

    def test_quick_move(self):
        # Create the filters
        settings = {"quick_moves": [225, "88", "Present"]}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({"move_1": 225}))
        pass2 = Events.RaidEvent(generate_raid({"move_1": 88}))
        pass3 = Events.RaidEvent(generate_raid({"move_1": 291}))
        # Test passing events
        for e in [pass1, pass2, pass3]:
            self.assertTrue(raid_filter.check_event(e))

        # Generate events that should fail
        fail1 = Events.RaidEvent(generate_raid({"move_1": 200}))
        fail2 = Events.RaidEvent(generate_raid({"move_1": 201}))
        fail3 = Events.RaidEvent(generate_raid({"move_1": 202}))

        # Test failing events
        for e in [fail1, fail2, fail3]:
            self.assertFalse(raid_filter.check_event(e))

    def test_charge_move(self):
        # Create the filters
        settings = {"charge_moves": [283, "14", "Solar Beam"]}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({"move_2": 283}))
        pass2 = Events.RaidEvent(generate_raid({"move_2": 14}))
        pass3 = Events.RaidEvent(generate_raid({"move_2": 116}))
        # Test passing events
        for e in [pass1, pass2, pass3]:
            self.assertTrue(raid_filter.check_event(e))

        # Generate events that should fail
        fail1 = Events.RaidEvent(generate_raid({"move_2": 200}))
        fail2 = Events.RaidEvent(generate_raid({"move_2": 201}))
        fail3 = Events.RaidEvent(generate_raid({"move_2": 202}))

        # Test failing events
        for e in [fail1, fail2, fail3]:
            self.assertFalse(raid_filter.check_event(e))

    def test_raid_lvl(self):
        # Create the filters
        settings = {"min_raid_lvl": 2, "max_raid_lvl": 4}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({"level": 2}))
        pass2 = Events.RaidEvent(generate_raid({"level": 3}))
        pass3 = Events.RaidEvent(generate_raid({"level": 4}))
        # Test passing events
        for e in [pass1, pass2, pass3]:
            self.assertTrue(raid_filter.check_event(e))

        # Generate events that should fail
        fail1 = Events.RaidEvent(generate_raid({"level": 1}))
        fail2 = Events.RaidEvent(generate_raid({"level": 5}))

        # Test failing events
        for e in [fail1, fail2]:
            self.assertFalse(raid_filter.check_event(e))

    def test_gym_names(self):
        # Create the filters
        settings = {"gym_name_contains": ["pass"]}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({"name": "pass1"}))
        pass2 = Events.RaidEvent(generate_raid({"name": "2pass"}))
        pass3 = Events.RaidEvent(generate_raid({"name": "3pass3"}))
        # Test passing events
        for e in [pass1, pass2, pass3]:
            self.assertTrue(raid_filter.check_event(e))

        # Generate events that should fail
        fail1 = Events.RaidEvent(generate_raid({"name": "fail1"}))
        fail2 = Events.RaidEvent(generate_raid({"name": "failpas"}))
        fail3 = Events.RaidEvent(generate_raid({"name": "pasfail"}))

        # Test failing events
        for e in [fail1, fail2, fail3]:
            self.assertFalse(raid_filter.check_event(e))

    def test_gym_name_excludes(self):
        # Create the filters
        settings = {"gym_name_excludes": ["fail"]}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        for r in ["pass1", "2pass", "3pass3"]:
            event = Events.RaidEvent(generate_raid({"name": r}))
            self.assertTrue(raid_filter.check_event(event))

        # Generate events that should fail
        for r in ["fail1", "failpass", "passfail"]:
            event = Events.RaidEvent(generate_raid({"name": r}))
            self.assertFalse(raid_filter.check_event(event))

    def test_park(self):
        # Create the filters
        settings = {"park_contains": ["pass"]}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Test events that should pass
        for n in ["pass1", "2pass", "3pass3"]:
            event = Events.RaidEvent(generate_raid({"park": n}))
            self.assertTrue(raid_filter.check_event(event))

        # Test events that should fail
        for n in ["fail1", "failpas", "pasfail"]:
            event = Events.RaidEvent(generate_raid({"park": n}))
            self.assertFalse(raid_filter.check_event(event))

    def test_current_team(self):
        # Create the filters
        settings = {"current_teams": [1, "2", "Instinct"]}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({"team": 1}))
        pass2 = Events.RaidEvent(generate_raid({"team": 2}))
        pass3 = Events.RaidEvent(generate_raid({"team": 3}))
        # Test passing events
        for e in [pass1, pass2, pass3]:
            self.assertTrue(raid_filter.check_event(e))

        # Generate events that should fail
        fail1 = Events.RaidEvent(generate_raid({"team": 0}))

        # Test failing events
        for e in [fail1]:
            self.assertFalse(raid_filter.check_event(e))

    def test_sponsored(self):
        # Create the filters
        raid_filter1 = Filters.RaidFilter('filter1', {"sponsored": False})
        raid_filter2 = Filters.RaidFilter('filter2', {"sponsored": True})

        # Generate events
        not_sponsored = Events.RaidEvent(generate_raid({"sponsor": 0}))
        sponsored = Events.RaidEvent(generate_raid({"sponsor": 4}))

        # Test passing events
        self.assertTrue(raid_filter1.check_event(not_sponsored))
        self.assertTrue(raid_filter2.check_event(sponsored))

        # Test failing events
        self.assertFalse(raid_filter2.check_event(not_sponsored))
        self.assertFalse(raid_filter1.check_event(sponsored))

    def test_missing_info1(self):
        # Create the filters
        settings = {"max_dist": "inf", "is_missing_info": True}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({"dist": "Unknown"}))
        # Test passing events
        for e in [pass1]:
            self.assertTrue(raid_filter.check_event(e))

    def test_missing_info2(self):
        # Create the filters
        settings = {"max_dist": "inf", "is_missing_info": False}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({}))
        pass1.distance = 1000

        # Test passing events
        for e in [pass1]:
            self.assertTrue(raid_filter.check_event(e))

    def test_egg_distance(self):
        # Create the filters
        settings = {"max_dist": "2000", "min_dist": "400"}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({}))
        pass1.distance = 1000
        pass2 = Events.RaidEvent(generate_raid({}))
        pass2.distance = 800
        pass3 = Events.RaidEvent(generate_raid({}))
        pass3.distance = 600

        # Test passing events
        for e in [pass1]:
            self.assertTrue(raid_filter.check_event(e))

        # Generate events that should fail
        fail1 = Events.RaidEvent(generate_raid({}))
        fail1.distance = 3000
        fail2 = Events.RaidEvent(generate_raid({}))
        fail2.distance = 300
        fail3 = Events.RaidEvent(generate_raid({}))
        fail3.distance = 0

        # Test failing events
        for e in [fail1, fail2, fail3]:
            self.assertFalse(raid_filter.check_event(e))

    def test_custom_dts(self):
        # Create the filters
        settings = {"custom_dts": {"key1": "pass1"}}
        raid_filter = Filters.RaidFilter('filter1', settings)

        # Generate events that should pass
        pass1 = Events.RaidEvent(generate_raid({}))
        # Test passing events
        for e in [pass1]:
            self.assertTrue(raid_filter.check_event(e))

    def test_cp(self):
        settings = {'min_cp': 5000, 'max_cp': 9000}
        raid_filter = Filters.RaidFilter('cp_filter', settings)
        for i in [5000, 8000, 9000]:
            event = Events.RaidEvent(generate_raid({'cp': i}))
            self.assertTrue(raid_filter.check_event(event))
        for i in [4999, 9001, 999999]:
            event = Events.RaidEvent(generate_raid({'cp': i}))
            self.assertFalse(raid_filter.check_event(event))

    def test_time_left(self):
        # Create the filters
        settings = {'min_time_left': 1000, 'max_time_left': 8000}
        raid_filter = Filters.RaidFilter('time_filter', settings)

        # Test events that should pass
        for s in [2000, 4000, 6000]:
            d = (datetime.now() + timedelta(seconds=s))
            t = time.mktime(d.timetuple())
            event = Events.RaidEvent(generate_raid({"end": t}))
            self.assertTrue(raid_filter.check_event(event))

        # Test events that should fail
        for s in [200, 999, 8001]:
            d = (datetime.now() + timedelta(seconds=s))
            t = time.mktime(d.timetuple())
            event = Events.RaidEvent(generate_raid({"end": t}))
            self.assertFalse(raid_filter.check_event(event))


# Create a generic raid, overriding with an specific values
def generate_raid(values):
    raid = {
        "gym_id": "OWNmOTFmMmM0YTY3NGQwYjg0Y2I1N2JlZjU4OWRkMTYuMTY=",
        "url": "???",
        "name": "Unknown",
        "description": "???",
        "pokemon_id": 150,
        "cp": 12345,
        "move_1": 123,
        "move_2": 123,
        "start": 1499244052,
        "end": 1499246052,
        "level": 5,
        "latitude": 37.7876146,
        "longitude": -122.390624,
        "sponsor": None,
        "park": None
    }
    raid.update(values)
    return raid

    def test_is_ex_eligible(self):
        # Create the filters
        eligible = self.gen_filter({"is_ex_eligible": True})
        not_eligible = self.gen_filter({"is_ex_eligible": False})

        ex_event = self.gen_event({"is_ex_raid_eligible": True})
        not_ex_event = self.gen_event({"is_ex_raid_eligible": False})

        # Test passing
        self.assertTrue(eligible.check_event(ex_event))
        self.assertTrue(not_eligible.check_event(not_ex_event))

        # Test failing
        self.assertFalse(eligible.check_event(not_ex_event))
        self.assertFalse(not_eligible.check_event(ex_event))


if __name__ == '__main__':
    unittest.main()
