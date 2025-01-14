const { Telegraf } = require("telegraf");
const getAttendance = require("./getAttendance");

// import Telegraf from "telegraf";
// import getAttendance from "./getAttendance";

let users = {};
const bot = new Telegraf("7882412221:AAHzYZuoZ9IjSWLZjJvh754zbPp9bWzWWa0");
const val = await getAttendance("23071A67F4");
console.log(val);
bot.start((ctx) => {
  const chatId = ctx.chat.id;
  if (!users[chatId]) {
    ctx.reply("Hello! Please provide your username.");
    users[chatId] = { waitingForUsername: true };
  } else {
    ctx.reply(
      "You are already registered. Type /fetch to get your attendance or /exit to unregister."
    );
  }
});

bot.on("text", async (ctx) => {
  const chatId = ctx.chat.id;
  const message = ctx.message.text;

  // First-time username collection
  if (users[chatId] && users[chatId].waitingForUsername) {
    // Save the username
    users[chatId].username = message;
    users[chatId].waitingForUsername = false;
    console.log(users);
    ctx.reply(
      `Thank you! Your username has been saved. Type /fetch to get your attendance or /exit to unregister.`
    );
  }
});

bot.command("fetch", async (ctx) => {
  const chatId = ctx.chat.id;
  if (users[chatId] && users[chatId].username) {
    const userName = users[chatId].username;
    try {
      console.log(`Fetching attendance for ${userName}`);
      const attendance = await getAttendance(userName);
      if (attendance) {
        ctx.reply(`Attendance for ${userName}: ${attendance}`);
      } else {
        ctx.reply(
          `Sorry, there was an issue fetching attendance for ${userName}.`
        );
      }
    } catch (error) {
      console.error("Error fetching attendance:", error);
      ctx.reply("An error occurred while fetching the attendance.");
    }
  } else {
    ctx.reply("Please provide your username first by typing /start.");
  }
});

bot.command("exit", (ctx) => {
  const chatId = ctx.chat.id;
  if (users[chatId] && users[chatId].username) {
    delete users[chatId]; // Remove the user from the users object
    ctx.reply("You have been unregistered. Type /start to register again.");
  } else {
    ctx.reply("You are not registered yet. Type /start to register.");
  }
});

bot.launch().then(() => {
  console.log("Bot started!");
});
