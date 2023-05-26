# Spotnet Idle Poke
Tricks Spotify and Discord into thinking they are not idle, so streaming via Spotify on Discord isn't killed after 10 minutes.
Does so by sending WM_ACTIVATE messages to the windows, which is sufficient to avoid idle and doesn't change current window focus.

**Only works on Windows.**

## Installation & Usage Instructions
Download a portable binary .exe from the releases page and run it. 
The terminal will periodically give status updates. 

To build from source, python 3.6 is required (remove f-strings to lower python version requirement). 
Run `pip install -r requirements.txt` to install dependencies then run from source.
Furthermore, to obtain a single binary executable, install pyinstaller and run `pyinstaller -F .\SpotnetIdlePoke.py`.

## Why?
Discord and Spotify integration is shit, and I'm getting pissed off having to manually "poke" Discord every 10 minutes when hanging out in VR.
