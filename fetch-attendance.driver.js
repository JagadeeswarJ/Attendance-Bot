const getAttendance = require("./get-attendance");
require("dotenv").config();
const rollNumber = process.env.rollNumber;
(async () => {
  try {
    const attendance = await getAttendance(rollNumber);
    console.log("Attendance:", attendance);
  } catch (error) {
    console.error("Error fetching attendance:", error);
  }
})();
