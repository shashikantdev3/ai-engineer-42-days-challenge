# clip-watcher: clip a live stream while it's live

GTA 6 launches at midnight local time on 19 Nov 2026. Most clips of launch-night streams will be cut **after** the stream ends: download the whole night, scan it, post. This tool watches **live** instead and cuts a clip the moment chat explodes.

```
streamlink  ->  records the stream the moment it goes live      (rec/)
Twitch chat ->  read anonymously: no account, no token
every 10 s  ->  count chat messages; spike = 2.5x the recent normal
ffmpeg      ->  cuts 30 s around every spike                     (clips/)
Whisper     ->  writes captions for each clip (optional)         (clips/*.srt)
```

## Run it

You need Python 3.9+ and [ffmpeg](https://ffmpeg.org/download.html) on your PATH.

```
pip install -r requirements.txt
python watch.py <channel>              # e.g. your own Twitch channel
python watch.py <channel> --captions   # + Whisper captions
```

Output while it runs:

```
[00:02:30] chat  142 msgs/10s ████████████████████████████████████████
[00:02:40] chat  138 msgs/10s ████████████████████████████████████████  <- SPIKE
  ✂  clips/clip_001.mp4  (30 s)
```

Tune the numbers at the top of `watch.py`: `SPIKE_X`, `MIN_MSGS`, `BEFORE`, `AFTER`, `COOLDOWN`.

## The honest catch

- It only works **while the channel is live**. Start it before the stream, not after.
- A chat spike is a guess, not a guarantee: some clips will be boring.
- **Clip your own stream, or a stream whose owner said yes.** The stream belongs to the streamer; reposting someone's clips without permission can break the platform's rules and copyright.
- Anonymous chat (`justinfan` + a number) is read-only. It cannot send messages.

## Tested

17 Nov 2026 on a live Twitch channel: recording started, anonymous chat counted every 10 s, spikes detected, ffmpeg cut 1080p clips from the growing recording. Test clips were deleted afterwards.

All tools here are free and open source: [streamlink](https://github.com/streamlink/streamlink) (BSD-2), [ffmpeg](https://ffmpeg.org), [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (MIT).
