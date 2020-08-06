import * as React from "react";
import ScatterPlot from "./components/scatter-plot.jsx"
import { clusterPDistribution } from "./dice.js"
const n = 2
const f = 6
const range = (start, end) => {
  return [...Array(end - start).keys()].map(i => i + start);
}
// const data = [[0, 3], [5, 13], [10, 22], [15, 36], [20, 48], [25, 59], [30, 77], [35, 85], [40, 95], [45, 105], [50, 120], [55, 150], [60, 147], [65, 168], [70, 176], [75, 188], [80, 199], [85, 213], [90, 222], [95, 236], [100, 249]]
const dist = clusterPDistribution([[n, f]])
const xData = range(n, n * f + 1)
const yData = xData.map(p => dist.coeff[p])
const data = xData.map((x, i) => [x, yData[i]])
console.log(xData)
console.log(yData)
export default () => (
  <>
    <h1>Welcome to React Parcel Micro App!</h1>
    <p>Hard to get more minimal than this React app.</p>
    <ScatterPlot data={data} />
  </>
);
