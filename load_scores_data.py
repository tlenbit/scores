import json
from datetime import datetime, timezone
from typing import List, Set

from scores.models import Score


INPUT_FILE = 'static/input'


def load_scores_from_file(filename):
    with open(filename) as f:
        for line in f:
            message = json.loads(line)
            load_from_message(message)


def load_from_message(message):
    event_result_notifications = [n for n in message
                                  if n['class'] == 'Fon.Notification.EventResultNotification']

    load_from_notifications(event_result_notifications)


def load_from_notifications(notifications):
    for n in notifications:
        scores = n['object']['eventResultInstance']['object']['scores']
        event_id = n['object']['eventResultId']
        created_at = n['object']['timeCreate']

        for score in scores:
            load_score(score['object'], event_id, created_at)


def load_score(score, event_id, created_at):
    score_unique_fields = (event_id,
                           score['score1'],
                           score['score2'],
                           score['scoreIndex'])
    if score_unique_fields not in seen:
        scores.append(Score(
            score1=score['score1'],
            score2=score['score2'],
            score_idx=score['scoreIndex'],
            event_id=event_id,
            created_at=datetime.fromtimestamp(created_at/1000,
                                              tz=timezone.utc)
            )
        )
        seen.add(score_unique_fields)


def load_to_db(scores):
    Score.objects.bulk_create(scores)


print('Loading scores data...')

scores: List[Score] = []
seen: Set[tuple] = set()

load_scores_from_file(INPUT_FILE)

load_to_db(scores)
