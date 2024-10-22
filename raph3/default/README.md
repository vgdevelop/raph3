These are the backup files that will be restored when an uncontrolled exception occurs within the application, which should not happen but better safe than sorry.

These must contain a valid json document when changing any type of value, adding, or modifying any structure that you want to implement in case something bad happens.

Personally, I configure the entire device as I want it to work, create the corresponding actions, save the device status from the application control panel and proceed to connect it to a computer to set the default restore code to the last configuration that worked correctly by copying the contents of the /raph3/files folder where the databases are located by default to this /raph3/default folder by default and modifying the file extensions from .json to .bak

By default, the .bak extension is used, you can modify it as you like in /raph3/system.py - line 209 in restore() function