from datetime import datetime, timedelta


def test_VaccineNotifier(notifier):
    assert notifier.api_url_prod == 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
    assert notifier.api_url_test == 'https://cdndemo-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'


def test_getTodaysData(notifier):
    data = notifier.get_todays_data(431203)

    assert isinstance(data, dict)
    assert len(data.get('centers')) > 0


def test_getNumberOfSlots(notifier):
    input_json = {'centers': [
        {'sessions': [
            {'available_capacity': 0, 'min_age_limit': 0},
            {'available_capacity': 0, 'min_age_limit': 0}
        ]},
        {'sessions': [
            {'available_capacity': 0, 'min_age_limit': 0, }
        ]},
        {'sessions': [
            {'available_capacity': 0, 'min_age_limit': 0},
            {'available_capacity': 0, 'min_age_limit': 0, }
        ]},
        {'sessions': [
            {'available_capacity': 0, 'min_age_limit': 0, }
        ]}
    ]}

    slots_18, slots_45 = notifier.get_number_of_slots(input_json)

    assert slots_18 == 0
    assert slots_45 == 0

    input_json = {'centers': [
        {'sessions': [
            {'available_capacity': 23, 'min_age_limit': 45},
            {'available_capacity': 23, 'min_age_limit': 18}
        ]},
        {'sessions': [
            {'available_capacity': 56, 'min_age_limit': 45, }
        ]},
        {'sessions': [
            {'available_capacity': 9, 'min_age_limit': 18},
            {'available_capacity': 56, 'min_age_limit': 45, }
        ]},
        {'sessions': [
            {'available_capacity': 15, 'min_age_limit': 18, }
        ]}
    ]}

    slots_18, slots_45 = notifier.get_number_of_slots(input_json)

    assert slots_18 == 47
    assert slots_45 == 135

    input_json = {'centers': [
        {'sessions': [
            {'available_capacity': 23, 'min_age_limit': 45},
        ]},
        {'sessions': [
            {'available_capacity': 56, 'min_age_limit': 45, }
        ]},
        {'sessions': [
            {'available_capacity': 56, 'min_age_limit': 45, }
        ]},
    ]}

    slots_18, slots_45 = notifier.get_number_of_slots(input_json)

    assert slots_18 == 0
    assert slots_45 == 135


def test_canSendEmail(notifier):
    assert not notifier.can_send_email(
        0, None), 'Cannot send email when 0 slots available'

    assert not notifier.can_send_email(
        0, datetime.now() - timedelta(hours=24)), 'Cannot send email when 0 slots available'

    assert not notifier.can_send_email(
        12, datetime.now() - timedelta(hours=1)), 'Last mail was send an hour ago'

    assert not notifier.can_send_email(
        56, datetime.now()), 'Last mail was send right now'

    assert notifier.can_send_email(
        5, None), '12 slots available and its the first mail'

    assert notifier.can_send_email(
        1, datetime.now() - timedelta(hours=25)), 'Last mail was sent 25 hours ago'
