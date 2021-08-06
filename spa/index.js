const _ = require("lodash");
const axios = require("axios");
const express = require("express");
const multer = require("multer");
const path = require("path");
const swaggerUi = require("swagger-ui-express");
const timeago = require("timeago.js");

const swaggerDocument = require("./swagger.json");
const upload = multer();

const app = express();
const port = 3000;

/* pug views */
app.set("view engine", "pug");
app.set("views", path.join(__dirname, "views"));

/* formatters */
app.locals.formatters = {
  time: (rawTime) => {
    const timeInMS = new Date(rawTime * 1000);
    return `${timeInMS.toLocaleString()} - ${timeago.format(timeInMS)}`;
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
  id: (id) => id.slice(0, 6),
};

/* server */
app.get("/", async (req, res) => {
  const {
    data: { blockchain: blocks },
  } = await axios.get("http://localhost:8000/api/blockchain");

  blocks.forEach((block) =>
    block.data.forEach((transaction) => {
      transaction.type = transaction.txins.length ? "regular" : "reward";
    })
  );

  res.render("blockchain", { blocks, pageTitle: "Blockchain" });
});
app.get("/transaction", async (req, res) => {
  res.render("transaction", { pageTitle: "Transaction" });
});
app.post(
  "/make_transaction",
  upload.fields([{ name: "keyname" }]),
  async (req, res) => {
    console.log(req.body);
    res.send("hola");
  }
);

/* api docs */
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

/* init */
app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
