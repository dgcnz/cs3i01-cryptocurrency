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
const getBlocks = async () => {
  let blocks;
  try {
    const response = await axios.get(`${apiUrl}/blockchain`);
    blocks = response.data.blockchain;
  } catch (e) {
    blocks = [];
  }
  _.forEach(blocks, (block) =>
    _.forEach(block.data, (transaction) => {
      transaction.type = transaction.txins.length ? "regular" : "reward";
    })
  );

  return blocks;
};

app.get("/", async (req, res) => {
  const blocks = await getBlocks();
  res.render("blockchain", { blocks, pageTitle: "Blockchain" });
});

const getKeynames = async () => {
  let keynames;
  try {
    const response = await axios.get(`${apiUrl}/keys`);
    keynames = _.map(response.data.keys, "keyname");
  } catch (e) {
    keynames = ["Error :("];
  }
  return keynames;
};

app.get("/transaction", async (req, res) => {
  const keynames = await getKeynames();
  res.render("transaction", {
    pageTitle: "Transaction",
    keynames,
  });
});

const postTransaction = async (data) => {
  let status;
  try {
    await axios.post(`${apiUrl}/transaction`, data);
    status = "success";
  } catch (e) {
    status = "error";
  }
  return status;
};

app.post("/transaction", async (req, res) => {
  const keynames = await getKeynames();
  const status = await postTransaction(req.body);
  res.render("transaction", {
    pageTitle: "Transaction",
    keynames,
    [status]: true,
  });
});

app.get("/key", async (req, res) => {
  res.render("key", { pageTitle: "Key" });
});

const postKey = async (data) => {
  let status;
  try {
    await axios.post(`${apiUrl}/keys`, data);
    status = "success";
  } catch (e) {
    status = "error";
  }
  return status;
};

app.post("/key", async (req, res) => {
  const status = await postKey(req.body);
  res.render("key", { pageTitle: "Key", [status]: true });
});

const getBalances = async () => {
  const getBalance = async (address) => {
    let balance;
    try {
      const response = await axios.get(`${apiUrl}/balance?address=${address}`);
      balance = response.data.balance;
    } catch (e) {
      balance = -1;
    }
    return balance;
  };
  let balances;
  try {
    const response = await axios.get(`${apiUrl}/keys`);
    balances = response.data.keys;
    for (let i = 0; i < balances.length; ++i) {
      balances[i].balance = await getBalance(balances[i].address);
    }
  } catch (e) {
    balances = [];
  }
  return balances;
};

app.get("/balance", async (req, res) => {
  const balances = await getBalances();
  res.render("balance", {
    balances,
    columns: ["keyname", "address", "balance"],
    pageTitle: "Balance",
  });
});

/* api docs */
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

/* init */
app.listen(port, "0.0.0.0", () => {
  console.log(
    `${process.env.BACKEND_URL} app listening at http://localhost:${port}`
  );
});
