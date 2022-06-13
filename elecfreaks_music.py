# SPDX-FileCopyrightText: Copyright ELECFREAKS
# SPDX-License-Identifier: MIT

"""
`Music`
====================================================
This is the `Music` class that you can use to play melodies through a buzzer
in CircuitPython. The library was inspired by the micro:bit `music` module.
"""

import time
import asyncio
import pwmio
from micropython import const


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/elecfreaks/circuitpython_ef_music.git"


_ARTICULATION_MS = const(10)  # articulation between notes in milliseconds
_MIDDLE_FREQUENCIES = [
    const(440),
    const(494),
    const(262),
    const(294),
    const(330),
    const(349),
    const(392),
]
_MIDDLE_SHARPS_FREQUENCIES = [
    const(466),
    const(0),
    const(277),
    const(311),
    const(0),
    const(370),
    const(415),
]


class Music:
    """
    You can use the Music class to play melodies through a buzzer
    in CircuitPython.

    :param ~microcontroller.Pin pin: The buzzer pin.
    :param int ticks: A number of ticks constitute a beat. Defaults to 4.
    :param int bpm: Beats per minute. Defaults to 120.
    """
    def __init__(self, pin, ticks=4, bpm=120):
        self._ticks = ticks
        self._bpm = bpm
        self._octave = 4
        self._duration = 4
        self._pwm = pwmio.PWMOut(pin, frequency=1, variable_frequency=True)
        self._pwm.duty_cycle = 0
        self._playing = False

    def _tone(self, frequency):
        if frequency <= 0:
            self._pwm.duty_cycle = 0
        else:
            self._pwm.duty_cycle = 0x8000
            self._pwm.frequency = int(frequency)

    def _get_frequency_duration(self, note_str):
        note_split = note_str.lower().split(":")
        note = 'r'
        sharp = False
        note_index = 0

        if len(note_split) > 0:
            note = note_split[0]
        if len(note_split) > 1:
            try:
                self._duration = int(note_split[1])
            except ValueError as error:
                raise ValueError(
                    f"note '{note_str}' format is incorrect."
                ) from error

        # note(a, b, c, d, e, f, g, r), note_index(0, 1, 2, 3, 4, 5, 6, 17)
        note_index = ord(note[0]) - ord("a")
        if note_index < 0 or (note_index > 6 and note_index != 17):
            raise ValueError(f"note '{note_str}' format is incorrect.")

        # Like "c4", "c#" or "db"
        if len(note) == 2:
            try:
                # Like "c4"
                self._octave = int(note[1])
            except ValueError as error:
                # Like "c#" or "db"
                sharp = True
                if note[1] == "b" and note_index <= 6:
                    note_index -= 1
                elif note[1] != "#":
                    raise ValueError(
                        f"note '{note_str}' format is incorrect."
                    ) from error
        # Like "c#4"
        elif len(note) == 3:
            try:
                self._octave = int(note[2])
            except ValueError as error:
                raise ValueError(
                    f"note '{note_str}' format is incorrect."
                ) from error

            sharp = True
            if note[1] == "b" and note_index <= 6:
                note_index -= 1
            elif note[1] != "#":
                raise ValueError(f"note '{note_str}' format is incorrect.")
        elif len(note) != 1:
            raise ValueError(f"note '{note_str}' format is incorrect.")

        frequency = 0
        if note_index <= 6:
            shift_count = self._octave - 4
            if sharp:
                if shift_count > 0:
                    frequency = _MIDDLE_SHARPS_FREQUENCIES[note_index] \
                        << shift_count
                else:
                    frequency = _MIDDLE_SHARPS_FREQUENCIES[note_index] \
                        >> -shift_count
            else:
                if shift_count > 0:
                    frequency = _MIDDLE_FREQUENCIES[note_index] << shift_count
                else:
                    frequency = _MIDDLE_FREQUENCIES[note_index] >> -shift_count

        return [frequency, self._duration * (60000 / self._bpm / self._ticks)]

    def set_tempo(self, ticks=4, bpm=120):
        """Sets the approximate tempo for playback.

        :param int ticks: A number of ticks constitute a beat. Defaults to 4.
        :param int bpm: Beats per minute. Defaults to 120.
        """
        self._ticks = ticks
        self._bpm = bpm

    def get_tempo(self):
        """Gets the current tempo as a tuple of integers: (ticks, bpm).
        """
        return (self._ticks, self._bpm)

    def play(self, music):
        """Plays a melody.

        :param music: The musical DSL.
        """
        self._octave = 4
        self._duration = 4

        if not isinstance(music, (list, str)):
            raise TypeError("the music type must be a list or string.")

        if isinstance(music, str):
            frequency_duration = self._get_frequency_duration(music)
            self.pitch(frequency_duration[0], frequency_duration[1])
            return

        for note in music:
            if not isinstance(note, str):
                raise ValueError("the music contains unexpected element.")

            frequency_duration = self._get_frequency_duration(note)
            self.pitch(frequency_duration[0], frequency_duration[1])

    async def play_async(self, music):
        """Asynchronously plays a melody.

        :param music: The musical DSL.
        """
        self._octave = 4
        self._duration = 4
        self._playing = True

        if not isinstance(music, (list, str)):
            raise TypeError("the music type must be a list or string.")

        if isinstance(music, str):
            frequency_duration = self._get_frequency_duration(music)
            await self.pitch_async(
                frequency_duration[0], frequency_duration[1]
            )
            return

        for note in music:
            if not isinstance(note, str):
                raise ValueError("the music contains unexpected element.")

            if not self._playing:
                break

            frequency_duration = self._get_frequency_duration(note)
            await self.pitch_async(
                frequency_duration[0], frequency_duration[1]
            )

        self._playing = False

    def pitch(self, frequency, duration=-1):
        """Plays a pitch at the integer frequency given for the specified
        number of milliseconds.

        :param int frequency: The specified frequency.
        :param int duration: The specified duration.
        """
        self._tone(frequency)
        if duration >= 0:
            duration -= _ARTICULATION_MS
            if duration < 0:
                duration = 10
            time.sleep(duration / 1000)
            self._tone(0)
            time.sleep(_ARTICULATION_MS / 1000)

    async def pitch_async(self, frequency, duration=-1):
        """Asynchronously plays a pitch at the integer frequency given for the
        specified number of milliseconds.

        :param int frequency: The specified frequency.
        :param int duration: The specified duration.
        """
        self._tone(frequency)
        if duration >= 0:
            duration -= _ARTICULATION_MS
            if duration < 0:
                duration = 10
            await asyncio.sleep(duration / 1000)
            self._tone(0)
            await asyncio.sleep(_ARTICULATION_MS / 1000)

    def stop(self):
        """Stops the music playback.
        In fact, works only for `play_async(music)`.
        """
        self._playing = False

    def reset(self):
        """Resets to default state.
        """
        self._ticks = 4
        self._bpm = 120
        self._octave = 4
        self._duration = 4
