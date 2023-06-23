# Doora On Device Software

This is the repository for the python code that runs on the raspberry pi.

## Important notes for development

1. The playing of audio fully utilizes the cpu
2. If the serial connection is physically connected but pi does not directly respond to serial input, the connection breaks

As a result, sometimes during the execution of the program the serial connection breaks. This can be fixed by unplugging and replugging the serial connection and restarting the program.
