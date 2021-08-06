const _ = require("lodash");
const axios = require("axios");
const express = require("express");
const path = require("path");
const swaggerUi = require("swagger-ui-express");
const timeago = require("timeago.js");

const swaggerDocument = require("./swagger.json");

const app = express();
const port = 3000;
const apiUrl = `http://${process.env.BACKEND_URL}/api`;

/* form data handling */
app.use(express.json()); // Used to parse JSON bodies
app.use(express.urlencoded()); //Parse URL-encoded bodies

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
  let blocks;
  try {
    const {
      data: { blockchain },
    } = await axios.get(`${apiUrl}/blockchain`);
    blocks = blockchain;
  } catch (e) {
    blocks = [];
  }

  _.forEach(blocks, (block) =>
    _.forEach(block.data, (transaction) => {
      transaction.type = transaction.txins.length ? "regular" : "reward";
    })
  );

  res.render("blockchain", { blocks, pageTitle: "Blockchain" });
});

app.get("/transaction", async (req, res) => {
  let keynames;
  try {
    const response = await axios.get(`${apiUrl}/keys`);
    keynames = response.data.keynames;
  } catch (e) {
    keynames = ["Error :("];
  }

  res.render("transaction", { pageTitle: "Transaction", keynames });
});

app.post("/transaction", async (req, res) => {
  let keynames;
  try {
    const response = await axios.get(`${apiUrl}/keys`);
    keynames = response.data.keynames;
  } catch (e) {
    keynames = ["Error :("];
  }

  let status;
  try {
    await axios.post(`${apiUrl}/transaction`);
    status = "success";
  } catch (e) {
    status = "error";
  }

  res.render("transaction", {
    pageTitle: "Transaction",
    keynames,
    [status]: true,
  });
});

app.get("/key", async (req, res) => {
  res.render("key", { pageTitle: "Key" });
});

app.post("/key", async (req, res) => {
  let status;
  try {
    await axios.post(`${apiUrl}/keys`, {
      keyname: req.body.keyname,
    });
    status = "success";
  } catch (e) {
    status = "error";
  }

  res.render("key", { pageTitle: "Key", [status]: true });
});

/* api docs */
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

/* init */
app.listen(port, "0.0.0.0", () => {
  console.log(
    `${process.env.BACKEND_URL} app listening at http://localhost:${port}`
  );
});
