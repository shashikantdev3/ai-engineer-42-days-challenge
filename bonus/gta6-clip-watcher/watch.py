"""clip-watcher: clip a Twitch stream WHILE it is live.

  python watch.py CHANNEL              record + watch chat + cut clips
  python watch.py CHANNEL --captions   also write Whisper captions (.srt) for every clip

How it works
  1. streamlink records the stream to rec/ the moment it goes live.
  2. Twitch chat is read anonymously (nick justinfanNNNN): no account, no token.
  3. Every 10 s we count chat messages. A spike = way more than the recent normal.
  4. ffmpeg cuts the 30 s around every spike into clips/.
  5. (optional) Whisper writes captions for each clip.

Only clip your own stream, or a stream whose owner said yes. Works only while the channel is live.
"""
import argparse, os, random, shutil, socket, statistics, subprocess, sys, threading, time
from collections import deque
from datetime import datetime

WINDOW = 10        # seconds per chat count
HISTORY = 18       # windows in the "normal" baseline (3 minutes)
SPIKE_X = 2.5      # spike = this many times the median of the baseline
MIN_MSGS = 5       # ...and at least this many messages
BEFORE, AFTER = 25, 5   # seconds of video before / after the spike
COOLDOWN = 60      # no two clips closer than this


def tool(name):
    path = shutil.which(name) or os.path.expanduser(f"~/.local/bin/{name}")
    if not os.path.exists(path):
        sys.exit(f"{name} not found. Install it first (see README).")
    return path


def record(channel, out):
    """streamlink waits for the stream to go live, then records it to out."""
    return subprocess.Popen([tool("streamlink"), f"https://twitch.tv/{channel}", "best", "-o", out, "--force",
                             "--twitch-disable-ads", "--retry-streams", "30"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def chat(channel, counter, stop):
    """Anonymous Twitch chat: justinfan + any number is a read-only guest login."""
    while not stop.is_set():
        try:
            s = socket.create_connection(("irc.chat.twitch.tv", 6667), timeout=30)
            s.sendall(f"NICK justinfan{random.randint(10000, 99999)}\r\nJOIN #{channel}\r\n".encode())
            buf = ""
            while not stop.is_set():
                data = s.recv(4096).decode("utf-8", "ignore")
                if not data:
                    break
                buf += data
                *lines, buf = buf.split("\r\n")
                for line in lines:
                    if line.startswith("PING"):
                        s.sendall(b"PONG :tmi.twitch.tv\r\n")
                    elif " PRIVMSG " in line:
                        counter[0] += 1
        except OSError:
            time.sleep(3)


def cut(video, start, n, captions):
    out = f"clips/clip_{n:03d}.mp4"
    time.sleep(AFTER + 5)   # let the recording catch up past the moment
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0, start):.1f}", "-i", video,
                    "-t", str(BEFORE + AFTER), "-c", "copy", out])
    print(f"  ✂  {out}  ({BEFORE + AFTER} s)")
    if captions:
        from faster_whisper import WhisperModel   # pip install faster-whisper
        model = WhisperModel("small", compute_type="int8")
        segs, _ = model.transcribe(out)
        with open(out[:-4] + ".srt", "w", encoding="utf-8") as f:
            for i, sg in enumerate(segs, 1):
                ts = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}"
                f.write(f"{i}\n{ts(sg.start)} --> {ts(sg.end)}\n{sg.text.strip()}\n\n")
        print(f"  📝 {out[:-4]}.srt")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("channel")
    ap.add_argument("--captions", action="store_true")
    a = ap.parse_args()
    ch = a.channel.lower().lstrip("#")
    os.makedirs("rec", exist_ok=True); os.makedirs("clips", exist_ok=True)
    video = f"rec/{ch}-{datetime.now():%Y%m%d-%H%M%S}.ts"
    rec = record(ch, video)
    counter, stop = [0], threading.Event()
    threading.Thread(target=chat, args=(ch, counter, stop), daemon=True).start()
    print(f"watching #{ch}: recording to {video}, counting chat every {WINDOW} s (Ctrl+C to stop)")

    hist, t0, last_clip, n = deque(maxlen=HISTORY), None, -COOLDOWN, 0
    try:
        while rec.poll() is None:
            time.sleep(WINDOW)
            msgs, counter[0] = counter[0], 0
            if t0 is None:
                if os.path.exists(video) and os.path.getsize(video) > 0:
                    t0 = time.time() - WINDOW          # recording started during this window
                else:
                    print("  waiting for the stream to go live..."); continue
            now = time.time() - t0
            base = statistics.median(hist) if len(hist) >= 3 else None
            spike = base is not None and msgs >= max(MIN_MSGS, SPIKE_X * base) and now - last_clip > COOLDOWN
            print(f"[{int(now // 3600):02d}:{int(now % 3600 // 60):02d}:{int(now % 60):02d}] chat {msgs:4d} msgs/{WINDOW}s {'█' * min(40, msgs // 2)}{'  <- SPIKE' if spike else ''}")
            if spike:
                n += 1; last_clip = now
                threading.Thread(target=cut, args=(video, now - BEFORE, n, a.captions)).start()
            hist.append(msgs)
        print("stream ended.")
    except KeyboardInterrupt:
        pass
    finally:
        stop.set(); rec.terminate()
        print("stopped. Clips still being cut will finish in a few seconds.")


if __name__ == "__main__":
    main()
