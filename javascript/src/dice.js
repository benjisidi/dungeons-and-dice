const Polynomial = require("polynomial")

/*
  Nomenclature:
    A _set_ of dice is a collection of n dice all with the same number of faces, f,
      denoted ndf - eg, three six-sided die would be the set 3d6. These are represented
      as a tuple [n, f]
    A _cluster_ of dice is a collection of N sets, represented as a 2xN matrix:
    [
      [ n1, f1 ],
      [ n2, f2 ],
      ...,
      [ nN, fN ]
    ]
*/

const rollSet = ([n, f]) => Array(n).fill().map(_ => Math.floor(Math.random() * (f - 1) + 1))

const rollCluster = (cluster, n = 1) => cluster.map(set => roll(set))

const expectedResult = (cluster) => cluster.map(([n, f]) => n * (f + 1) / 2)

const powerset = (set) => Polynomial([0, ...Array(set[1]).fill(1)]).pow(set[0])

const clusterPowerset = (cluster) => cluster.reduce((result, set) => {
  return result.mul(powerset(set))
}, new Polynomial(1))

const waysToRoll = (target, set) => {
  if (target > set[0] * set[1] || target < set[1]) {
    return 0
  }
  if (target == set[0] * set[1] || target == set[1]) {
    return 1
  }
  return powerset(set).coeff[target]
}
const waysToRollCluster = (target, cluster) => clusterPowerset(cluster).coeff[target]

const pOfRolling = (target, set) => waysToRoll(target, set) / Math.pow(set[1], set[0])

const clusterPDistribution = (cluster) => {
  const totalPossibilities = cluster.reduce((total, set) => {
    const power = Math.pow(set[1], set[0])
    return total * power
  }, 1)
  const normalisedPossibilities = clusterPowerset(cluster)
  Object.entries(normalisedPossibilities.coeff).forEach(([exp, coeff]) => normalisedPossibilities.coeff[exp] = coeff / totalPossibilities)
  return normalisedPossibilities
}

const pOfRollingCluster = (target, cluster) => {
  return clusterPDistribution(cluster).coeff[target]
}

export { clusterPDistribution }