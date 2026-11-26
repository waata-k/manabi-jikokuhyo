"""Generate sample-data.json: a fictional data file that shows the format and lets anyone try the app.
All stations, lines and timetables here are made up."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
strings = []


def si(s):
    if s not in strings:
        strings.append(s)
    return strings.index(s)


def leg(first, last, peak_gap, gap, run_local, run_rapid, dest, rapid_every=3, holiday=False):
    rows, t, n = [], first, 0
    while t <= last:
        peak = (7 * 60 <= t < 9 * 60) or (17 * 60 <= t < 19 * 60)
        rapid = rapid_every and n % rapid_every == 2 and 6 * 60 <= t < 22 * 60
        rows += [t, t + (run_rapid if rapid else run_local), si('快速' if rapid else '各駅停車'), si(dest), 1 if n == 0 else 0]
        t += (gap if holiday or not peak else peak_gap)
        n += 1
    return rows


legs = {
    'home_hub': {'wd': leg(5 * 60 + 30, 23 * 60 + 50, 6, 10, 18, 14, '中央駅'), 'hd': leg(5 * 60 + 40, 23 * 60 + 40, 12, 12, 18, 14, '中央駅', holiday=True)},
    'hub_campus': {'wd': leg(5 * 60 + 50, 24 * 60 + 10, 8, 12, 11, 11, '大学前', rapid_every=0), 'hd': leg(6 * 60, 24 * 60, 15, 15, 11, 11, '大学前', rapid_every=0, holiday=True)},
    'campus_hub': {'wd': leg(5 * 60 + 45, 24 * 60, 8, 12, 11, 11, '中央駅', rapid_every=0), 'hd': leg(6 * 60 + 5, 23 * 60 + 50, 15, 15, 11, 11, '中央駅', rapid_every=0, holiday=True)},
    'hub_home': {'wd': leg(5 * 60 + 35, 24 * 60 + 15, 6, 10, 18, 14, 'さくら台'), 'hd': leg(5 * 60 + 50, 24 * 60, 12, 12, 18, 14, 'さくら台', holiday=True)},
}

pack = {
    'format': 'manabi-data', 'version': 1,
    'title': 'お試しデータ（架空の路線と単元）',
    'transit': {
        'strings': strings, 'legs': legs,
        'lines': {
            'minato': {'name': 'みなと線', 'color': '#2a78d6', 'dark': '#3987e5'},
            'yamabiko': {'name': 'やまびこ線', 'color': '#1baf7a', 'dark': '#199e70'},
        },
        'transfers': {'hub': {'label': '中央駅乗換', 'min': 3, 'windows': [{'from': '07:30', 'to': '09:00', 'min': 5, 'label': '朝の混雑時間帯'}]}},
        'routes': [
            {'id': 'go', 'label': 'さくら台 → 大学前', 'note': '中央駅で乗換', 'transfers': ['hub'],
             'legs': [{'leg': 'home_hub', 'line': 'minato', 'from': 'さくら台', 'to': '中央駅'},
                      {'leg': 'hub_campus', 'line': 'yamabiko', 'from': '中央駅', 'to': '大学前'}]},
            {'id': 'back', 'label': '大学前 → さくら台', 'note': '中央駅で乗換', 'transfers': ['hub'],
             'legs': [{'leg': 'campus_hub', 'line': 'yamabiko', 'from': '大学前', 'to': '中央駅'},
                      {'leg': 'hub_home', 'line': 'minato', 'from': '中央駅', 'to': 'さくら台'}]},
        ],
        'groups': [{'id': 'out', 'label': '行き', 'routes': ['go']}, {'id': 'back', 'label': '帰り', 'routes': ['back']}],
        'autoSwitch': {'before': 'out', 'after': 'back', 'at': '14:00'},
        'source': 'お試しデータの路線・駅・時刻はすべて架空のものです。',
    },
    'bus': {
        'label': 'キャンパス間バス',
        'routes': [
            {'id': 'bus1', 'label': '本キャンパス → 第2キャンパス', 'short': '本 → 第2', 'sub': '本キャンパス発', 'from': '本キャンパス', 'to': '第2キャンパス',
             'arrLabel': '第2 着', 'trips': '08:00-08:30a 09:30-10:00a 10:30-11:00b 12:20-12:50a 14:00-14:30a 15:30-16:00b 17:00-17:30a'},
            {'id': 'bus2', 'label': '第2キャンパス → 本キャンパス', 'short': '第2 → 本', 'sub': '第2キャンパス発', 'from': '第2キャンパス', 'to': '本キャンパス',
             'arrLabel': '本 着', 'trips': '08:40-09:10a 10:10-10:40a 11:10-11:40b 13:00-13:30a 14:40-15:10a 16:10-16:40b 17:40-18:10a'},
        ],
        'classes': {'a': {'label': '定期便', 'short': '定期', 'runs': ['1', '2']}, 'b': {'label': '増便', 'short': '増便', 'runs': ['2']}},
        'dayTypes': {'1': '通常運行', '2': '増便あり'},
        'weekdays': {'1': [1, 2, 4, 5], '2': [3]},
        'legend': ['定期便: 平日すべて', '増便: 水曜のみ'],
        'source': 'お試しデータのバスはすべて架空のものです。',
    },
    'units': {
        'subjects': [
            {'id': 'ex_math', 'name': '数学', 'color': 0, 'sample': True},
            {'id': 'ex_eng', 'name': '英語', 'color': 1, 'sample': True},
        ],
        'units': [
            {'id': 'ex_u1', 'subjectId': 'ex_math', 'name': '微分の基礎', 'status': 'doing', 'week': '第1週', 'book': '教科書', 'sample': True,
             'steps': [{'t': '教科書 1章を読む', 'b': '教科書', 'plan': '-1', 'done': '-1'}, {'t': '例題 1〜5 を解く', 'b': '問題集', 'plan': '+0'},
                       {'t': '練習問題 1〜10 を解く', 'b': '問題集', 'plan': '+0'}, {'t': '発展問題', 'b': '問題集', 'kind': 'a'}]},
            {'id': 'ex_u2', 'subjectId': 'ex_math', 'name': '積分の基礎', 'status': 'todo', 'week': '第1週', 'book': '教科書', 'sample': True,
             'steps': [{'t': '教科書 2章を読む', 'b': '教科書', 'plan': '+1'}, {'t': '例題 1〜6 を解く', 'b': '問題集', 'plan': '+2'}]},
            {'id': 'ex_u3', 'subjectId': 'ex_math', 'name': '行列の計算', 'status': 'todo', 'plan': '+0', 'est': 30, 'sample': True},
            {'id': 'ex_u4', 'subjectId': 'ex_eng', 'name': '単語 Unit 1〜3', 'status': 'todo', 'plan': '-1', 'est': 20, 'sample': True},
            {'id': 'ex_u5', 'subjectId': 'ex_eng', 'name': '長文読解 1', 'status': 'done', 'doneAt': '-2', 'est': 40, 'sample': True},
        ],
        'tasks': [{'id': 'ex_t1', 'text': 'レポートの構成を考える', 'date': '+0', 'done': False, 'sample': True}],
    },
}
out = os.path.join(ROOT, 'sample-data.json')
open(out, 'w', encoding='utf-8').write(json.dumps(pack, ensure_ascii=False, indent=1))
print('wrote sample-data.json', os.path.getsize(out), 'bytes')
