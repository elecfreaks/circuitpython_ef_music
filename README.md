# circuitpython_ef_music

This is the `Music` class that you can use to play melodies through a buzzer
in CircuitPython. The library was inspired by the [micro:bit `music` module](https://microbit-micropython.readthedocs.io/en/v2-docs/music.html).

## Dependencies

- [CircuitPython](https://circuitpython.org/)
- [CircuitPython_asyncio](https://github.com/adafruit/Adafruit_CircuitPython_asyncio.git)
- [CircuitPython_Ticks](https://github.com/adafruit/Adafruit_CircuitPython_Ticks.git)

## Musical Notation

An individual note is specified thus:

```py
NOTE[octave][:duration]
```

For example, `A1:4` refers to the note “A” in octave 1 that lasts for four ticks (a tick is an arbitrary length of time defined by a tempo setting function - see below). If the note name `R` is used then it is treated as a rest (silence).

Accidentals (flats and sharps) are denoted by the `b` (flat - a lower case b) and `#` (sharp - a hash symbol). For example, `Ab` is A-flat and `C#` is C-sharp.

**Note names are case-insensitive.**

The `octave` and `duration` parameters are states that carry over to subsequent notes until re-specified. The default states are `octave = 4` (containing middle C) and `duration = 4` (a crotchet, given the default tempo settings - see below).

For example, if 4 ticks is a crotchet, the following list is crotchet, quaver, quaver, crotchet based arpeggio:

```py
['c1:4', 'e:2', 'g', 'c2:4']
```

The opening of Beethoven’s 5th Symphony would be encoded thus:

```py
['r4:2', 'g', 'g', 'g', 'eb:8', 'r:2', 'f', 'f', 'f', 'd:8']
```

The definition and scope of an octave conforms to the table listed [on this page about scientific pitch notation](https://en.wikipedia.org/wiki/Scientific_pitch_notation#Table_of_note_frequencies). For example, middle “C” is `'c4'` and concert “A” (440) is `'a4'`. Octaves start on the note “C”.

The library has quite a lot of built-in melodies. Here’s a complete list:

- DADADADUM
- ENTERTAINER
- PRELUDE
- ODE
- NYAN
- RINGTONE
- FUNK
- BLUES
- BIRTHDAY
- WEDDING
- FUNERAL
- PUNCHLINE
- PYTHON
- BADDY
- CHASE
- BA_DING
- WAWAWAWAA
- JUMP_UP
- JUMP_DOWN
- POWER_UP
- POWER_DOWN

## Class

### `class Music(pin, ticks=4, bpm=120)`

You can use the Music class to play melodies through a buzzer in CircuitPython.

- **pin -** The buzzer pin.
- **ticks -** A number of ticks constitute a beat. Defaults to 4.
- **bpm -** Beats per minute. Defaults to 120.

> `set_tempo(ticks=4, bpm=120)`

Sets the approximate tempo for playback.

- **ticks -** A number of ticks constitute a beat. Defaults to 4.
- **bpm -** Beats per minute. Defaults to 120.

> `get_tempo()`

Gets the current tempo as a tuple of integers: (ticks, bpm).

> `play(music)`

Plays a melody.

- **music -** The musical DSL.

> `play_async(music)`

Asynchronously plays a melody.

- **music -** The musical DSL.

> `pitch(frequency, duration=-1)`

Plays a pitch at the integer frequency given for the specified number of milliseconds.

- **frequency -** The specified frequency.
- **duration -** The specified duration.

> `pitch_async(frequency, duration=-1)`

Asynchronously plays a pitch at the integer frequency given for the specified number of milliseconds.

- **frequency -** The specified frequency.
- **duration -** The specified duration.

> `stop()`

Stops the music playback. In fact, works only for `play_async(music)`.


> `reset()`

Resets to default state.

## Usage Example

Play built-in melody

```py
import board
from elecfreaks_music import Music

music = Music(board.BUZZER_GP0)

music.play(music.DADADADUM)
```

Synchronize playback

```py
import board
from elecfreaks_music import Music

music = Music(board.BUZZER_GP0)

# play Prelude in C.
notes = [
    'c4:1', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5', 'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5',
    'c4', 'd', 'a', 'd5', 'f5', 'a4', 'd5', 'f5', 'c4', 'd', 'a', 'd5', 'f5', 'a4', 'd5', 'f5',
    'b3', 'd4', 'g', 'd5', 'f5', 'g4', 'd5', 'f5', 'b3', 'd4', 'g', 'd5', 'f5', 'g4', 'd5', 'f5',
    'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5', 'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5',
    'c4', 'e', 'a', 'e5', 'a5', 'a4', 'e5', 'a5', 'c4', 'e', 'a', 'e5', 'a5', 'a4', 'e5', 'a5',
    'c4', 'd', 'f#', 'a', 'd5', 'f#4', 'a', 'd5', 'c4', 'd', 'f#', 'a', 'd5', 'f#4', 'a', 'd5',
    'b3', 'd4', 'g', 'd5', 'g5', 'g4', 'd5', 'g5', 'b3', 'd4', 'g', 'd5', 'g5', 'g4', 'd5', 'g5',
    'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
    'a3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'a3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
    'd3', 'a', 'd4', 'f#', 'c5', 'd4', 'f#', 'c5', 'd3', 'a', 'd4', 'f#', 'c5', 'd4', 'f#', 'c5',
    'g3', 'b', 'd4', 'g', 'b', 'd', 'g', 'b', 'g3', 'b3', 'd4', 'g', 'b', 'd', 'g', 'b'
]

music.play(notes)
```

Asynchronous playback

```py
import board
import digitalio
import asyncio
from elecfreaks_music import Music

music = Music(board.BUZZER_GP0)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# play Prelude in C.
notes = [
    'c4:1', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5', 'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5',
    'c4', 'd', 'a', 'd5', 'f5', 'a4', 'd5', 'f5', 'c4', 'd', 'a', 'd5', 'f5', 'a4', 'd5', 'f5',
    'b3', 'd4', 'g', 'd5', 'f5', 'g4', 'd5', 'f5', 'b3', 'd4', 'g', 'd5', 'f5', 'g4', 'd5', 'f5',
    'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5', 'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5',
    'c4', 'e', 'a', 'e5', 'a5', 'a4', 'e5', 'a5', 'c4', 'e', 'a', 'e5', 'a5', 'a4', 'e5', 'a5',
    'c4', 'd', 'f#', 'a', 'd5', 'f#4', 'a', 'd5', 'c4', 'd', 'f#', 'a', 'd5', 'f#4', 'a', 'd5',
    'b3', 'd4', 'g', 'd5', 'g5', 'g4', 'd5', 'g5', 'b3', 'd4', 'g', 'd5', 'g5', 'g4', 'd5', 'g5',
    'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
    'a3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'a3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
    'd3', 'a', 'd4', 'f#', 'c5', 'd4', 'f#', 'c5', 'd3', 'a', 'd4', 'f#', 'c5', 'd4', 'f#', 'c5',
    'g3', 'b', 'd4', 'g', 'b', 'd', 'g', 'b', 'g3', 'b3', 'd4', 'g', 'b', 'd', 'g', 'b'
]

async def blink(interval):
    while True:
        led.value = True
        await asyncio.sleep(interval)
        led.value = False
        await asyncio.sleep(interval)

async def main():
    player = asyncio.create_task(music.play_async(notes))
    light = asyncio.create_task(blink(0.1))
    await asyncio.gather(player)
    await asyncio.gather(light)

asyncio.run(main())
```
