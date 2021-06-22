from collections import defaultdict
from django.http import JsonResponse

from .models import Score


def events(request):
    scores = Score.objects.raw('''SELECT DISTINCT * FROM
                                    (SELECT *, ROW_NUMBER() OVER
                                                   (PARTITION BY event_id, score_idx
                                                     ORDER BY created_at DESC
                                                   ) AS date_rank
                                     FROM scores_score
                                     ) sub
                                   WHERE date_rank=1''')

    response = defaultdict(dict)

    for s in scores:
        response[s.event_id][s.score_idx] = {'score1': s.score1,
                                             'score2': s.score2}

    return JsonResponse(response)


def score_history(request, event_id):
    scores = Score.objects.filter(event_id=event_id).order_by('created_at')

    response = defaultdict(list)

    for s in scores:
        response[s.score_idx].append({'score1': s.score1,
                                      'score2': s.score2,
                                      'created_at': s.created_at})

    return JsonResponse(response)
