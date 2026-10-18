"""Prepare Lichess January 2013 rated PGN headers for an increment study.
Run: python prepare_increment_data.py --input path/to/file.pgn --outdir path/to/output
"""
import argparse
from pathlib import Path
import re
import pandas as pd

HEADER_RE = re.compile(r'^\[([^ ]+) "(.*)"\]$')
TIME_RE = re.compile(r'^(\d+)\+(\d+)$')

def read_headers(path):
    headers = {}
    with open(path, encoding='utf-8-sig', errors='replace') as f:
        for line in f:
            line = line.strip()
            hit = HEADER_RE.match(line)
            if hit:
                headers[hit.group(1)] = hit.group(2)
            elif not line and headers:
                yield headers
                headers = {}
        if headers:
            yield headers

def build(input_path, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for h in read_headers(input_path):
        match = TIME_RE.fullmatch(h.get('TimeControl', ''))
        if not match:
            continue
        initial, increment = map(int, match.groups())
        if initial == 0:  # 0+1 and related controls are substantively different; exclude from main cohort.
            continue
        if h.get('Result') not in ('1-0', '0-1', '1/2-1/2'):
            continue
        if h.get('Termination') not in ('Normal', 'Time forfeit'):
            continue
        try:
            white_elo = int(h['WhiteElo'])
            black_elo = int(h['BlackElo'])
        except (KeyError, ValueError):
            continue
        if not h.get('Site') or not h.get('White') or not h.get('Black'):
            continue
        rows.append({
            'game_id': h['Site'].rsplit('/', 1)[-1],
            'date_utc': h.get('UTCDate'), 'time_utc': h.get('UTCTime'),
            'event': h.get('Event'), 'white': h['White'], 'black': h['Black'],
            'white_elo': white_elo, 'black_elo': black_elo,
            'result': h['Result'], 'termination': h['Termination'],
            'initial_seconds': initial, 'increment_seconds': increment,
            'has_increment': int(increment > 0),
            'time_control': h['TimeControl'],
        })
    games = pd.DataFrame(rows)
    games['started_at_utc'] = pd.to_datetime(
        games['date_utc'] + ' ' + games['time_utc'],
        format='%Y.%m.%d %H:%M:%S', errors='coerce', utc=True)
    games = games.dropna(subset=['started_at_utc']).drop_duplicates(subset=['game_id'])
    # Main study: starting-clock durations with both increment and no-increment games.
    overlap = games.groupby('initial_seconds')['has_increment'].nunique()
    eligible_bases = overlap[overlap.eq(2)].index
    games['common_support_base'] = games['initial_seconds'].isin(eligible_bases).astype(int)
    games.to_csv(outdir / 'increment_games.csv', index=False)

    players = []
    for color in ('white', 'black'):
        other = 'black' if color == 'white' else 'white'
        frame = games[['game_id','started_at_utc','event','result','termination',
                       'initial_seconds','increment_seconds','has_increment',
                       'time_control','common_support_base',color,other,
                       color+'_elo',other+'_elo']].copy()
        frame.columns = ['game_id','started_at_utc','event','result','termination',
                         'initial_seconds','increment_seconds','has_increment',
                         'time_control','common_support_base','player','opponent',
                         'player_elo','opponent_elo']
        frame['color'] = color
        frame['elo_diff'] = frame['player_elo'] - frame['opponent_elo']
        frame['lost'] = ((frame['result'] == '0-1') if color == 'white' else
                         (frame['result'] == '1-0')).astype(int)
        frame['won'] = ((frame['result'] == '1-0') if color == 'white' else
                        (frame['result'] == '0-1')).astype(int)
        frame['draw'] = (frame['result'] == '1/2-1/2').astype(int)
        # A time forfeit labels the game, not the winner or each player's outcome.
        frame['lost_on_time'] = ((frame['termination'] == 'Time forfeit') &
                                 (frame['lost'] == 1)).astype(int)
        players.append(frame)
    pg = pd.concat(players, ignore_index=True)
    pg.to_csv(outdir / 'increment_player_games.csv', index=False)

    n_games = len(games)
    print(f'Included games: {n_games:,}; player-game observations: {len(pg):,}')
    print(f'Games with increment: {games.has_increment.sum():,}; without: {(games.has_increment==0).sum():,}')
    print(f'Games with common-support starting durations: {games.common_support_base.sum():,}')
    print('Player-game outcomes by increment:')
    print(pg.groupby('has_increment').agg(n=('lost_on_time','size'),
             timeout_loss_rate=('lost_on_time','mean')).to_string())
    print('Saved to', outdir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--outdir', type=Path, default=Path('.'))
    a = parser.parse_args()
    build(a.input, a.outdir)
