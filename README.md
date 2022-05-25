# okay-to-wait
A simple (very simple) okay to wait clock using a Raspberry Pi with a Sensehat.

Requires a Raspberry Pi with networking and a Sensehat.

Schedules are set to run continuously, but have no validation apart from being json. The clock will be red between the intervals, which should follow this format:
[["HH:MM", "HH:MM"], ["HH:MM", "HH:MM"]]