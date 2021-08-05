const express = require("express");
const swaggerUi = require("swagger-ui-express");

const port = 3000;
const app = express();
const swaggerDocument = require("./swagger.json");

app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
