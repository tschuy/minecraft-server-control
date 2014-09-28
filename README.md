Minecraft Server Control
========================

A Python script to control and back up a Minecraft server.

This Python script allows you to control a Minecraft server through init.d-like commands. You can view the status of the server, start the server, and stop the server:

``minecraft.py start``

``minecraft.py stop``

``minecraft.py status``

The script also allows you to back up your server. It is set up to be run by cron every 5 minutes; it saves any backup under 15 minutes old, along with one per day for a week.

``minecraft.py backup``
