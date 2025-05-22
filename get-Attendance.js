// attendance widget
const puppeteer = require("puppeteer");
let attendanceValue = 0;
async function getAttendance(userName) {
  const browser = await puppeteer.launch({
    headless: true,
  });
  const page = await browser.newPage();
  await page.goto("https://automation.vnrvjiet.ac.in/eduprime3");
  // await page.screenshot({ path: "example.png" });

  const usernameSelector = '[name="username"]';
  await page.waitForSelector(usernameSelector);
  await page.click(usernameSelector);
  userName = userName + "p";
  await page.type(usernameSelector, userName);

  const passwordSelector = '[name="xpassword"]';
  await page.waitForSelector(passwordSelector);
  await page.click(passwordSelector);
  await page.type(passwordSelector, "Welcome@123");

  const loginSelector = ".btn.btn-sm.btn-primary.mt-2";
  await page.click(loginSelector);

  await page.waitForNavigation({ waitUntil: "networkidle0" });

  const attendanceSelector = "#attp";
  await page.waitForSelector(attendanceSelector);
  await page.click(attendanceSelector);

  const attValueSelector = ".font-medium.m-b-0";
  await page.waitForSelector(attValueSelector);
  await page.click(attValueSelector);

  const textContent = await page.$eval(
    attValueSelector,
    (element) => element.textContent
  );
  //   console.log("attendance is :", textContent);
  // await page.screenshot({ path: "login.png" });
  attendanceValue = textContent;
  await browser.close();
  //   console.log(attendanceValue);
  return attendanceValue;
}

module.exports = getAttendance;
