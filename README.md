# VNRVJIET Telegram Bot - Attendance Fetcher

This bot allows VNRVJIET students to fetch their attendance information directly through Telegram by providing their username.

## Features

- **Register Once**: Users are asked to provide their username once at the start.
- **Fetch Attendance**: After registering, users can type `/fetch` to retrieve their attendance.
- **Unregister**: Users can type `/exit` to unregister, which will remove their username from the bot.

## Modules Used

1. **`Telegraf`** - A modern Telegram Bot API framework for Node.js. It makes it easy to develop bots on Telegram.

2. **`puppeteer`** -Puppeteer is a Node.js library that provides a high-level API to control headless Chrome or Chromium browsers, enabling automation of tasks like web scraping, testing, and rendering

## Additional Usage

Apart from the Telegram bot, the attendance can also be fetched independently using the `getAttendance` script file. This script allows a single user to fetch their attendance without interacting with the bot.
or a windows batch file to call the node script. 