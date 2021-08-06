const express = require("express");
const axios = require("axios");
const path = require("path");
const swaggerUi = require("swagger-ui-express");

const swaggerDocument = require("./swagger.json");

const app = express();
const port = 3000;

/* dashboard */
app.set("view engine", "pug");
app.set("views", path.join(__dirname, "views"));
app.locals.formatters = {
  time: (rawTime) => {
    const timeInMS = new Date(rawTime * 1000);
    return `${timeInMS.toLocaleString()} - ${timeago().format(timeInMS)}`;
  },
  hash: (hashString) => {
    return hashString != "0"
      ? `${hashString.substr(0, 5)}...${hashString.substr(
          hashString.length - 5,
          5
        )}`
      : "<empty>";
  },
  amount: (amount) => amount.toLocaleString(),
};
app.get("/", async function (req, res) {
  const {
    data: { blockchain: blocks },
  } = await axios.get("http://localhost:8000/api/blockchain");
  res.render("blockchain", { blocks, pageTitle: "Blockchain" });
});

/* api docs */
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
