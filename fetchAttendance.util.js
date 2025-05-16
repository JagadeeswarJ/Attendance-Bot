const getAttendance = require("./getAttendance");

(async () => {
  try {
    const attendance = await getAttendance("23071A67F4");
    console.log("Attendance:", attendance);
  } catch (error) {
    console.error("Error fetching attendance:", error);
  }
})();
