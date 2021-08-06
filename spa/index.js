const express = require("express");
const path = require("path");
const swaggerUi = require("swagger-ui-express");

const swaggerDocument = require("./swagger.json");

const app = express();
const port = 3000;

/* dashboard */
app.set("view engine", "pug");
app.set("views", path.join(__dirname, "views"));
app.get("/", function (req, res) {
  res.render("blockchain", { blocks: [], pageTitle: "Blockchain" });
});

/* api docs */
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
