# Tiny chess engine — alpha-beta + null-move R=3

[![make.fun](https://make.fun/badge/tiny-chess-01)](https://make.fun/competitions/tiny-chess-01)

A tiny chess engine written in pure Python, squeezed into 4 KB of source.
It plays a real game of chess over standard input and output using a JSON
protocol, with no external dependencies.

## How it plays

The engine searches with alpha-beta pruning and a transposition table, so
positions seen before are reused instead of searched again. Killer moves
are remembered and tried first to make the search cut off sooner. A
quiescence search keeps looking past captures so the engine does not stop
in the middle of a noisy sequence and misjudge the position. Null-move
pruning with reduction R=3 skips a side's turn when the position is strong
enough that even passing cannot lose it, which saves a large part of the
search tree. Move ordering, a simple piece-square evaluation and
iterative deepening round out the playing strength.

## Running it

```sh
python3 main.py
```

The engine reads one JSON object per line from stdin and writes one JSON
object per line to stdout. Send a position, then a `go` command, and it
replies with its best move. The whole engine is a single file, `main.py`,
small enough to read end to end.

## Competition

Built for the tiny-chess-01 competition on make.fun: a 4 KB Python chess
engine. See the badge above for the competition page, current leaderboard
rank and prize pool.
