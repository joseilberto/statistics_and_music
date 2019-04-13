lower_side_notes = ["A0", "A#0", "B0"]
upper_side_notes = ["G#9", "A9", "A#9", "B9"]
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
full_range = [note + str(pitch) for pitch in range(1, 10) for note in notes if
                note + str(pitch) not in upper_side_notes]
full_range = lower_side_notes + full_range
note_numbers = range(21, 128)
NOTES_DICT = dict(zip(note_numbers, full_range))   
