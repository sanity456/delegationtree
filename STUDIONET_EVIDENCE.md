# StudioNet evidence

## Corrected release status

The contract source now includes per-creator mandate namespaces and lifetime allowances, parent-reserved descendant-node capacity, per-node action limits and IDs, and closed-mandate mutation guards. It has passed local GenVM lint/SDK validation and 11 direct tests. The corrected source has **not yet been deployed or tested on StudioNet**. Do not submit the deployment below as evidence for the corrected source.

## Obsolete deployment (do not submit)

- Address: `0x0a3Ed4cDc845B42f4c982610681bcFeDDFFf1A5C`
- Deployment transaction: `0xc4320389644748734976b51368e0ef47339274f8325c2144bb9559b031be99fa`
- It runs the earlier contract with a shared deployment-wide mandate limit and no reserved child node slots. It does not match current `contracts/delegation_tree.py`.
- Earlier successful mandate, delegation, and action transactions prove only that earlier code path; they do not prove creator or branch capacity isolation.

## Required evidence before submission

Deploy the pushed corrected source. Record the new deployment receipt and execution result, public source commit and raw source hash, and compare deployed source bytes against the Git blob. On StudioNet, show that creator A's full mandate allowance does not consume creator B's capacity, a child cannot exceed descendant slots reserved by its parent, node-scoped action IDs/caps remain independent, closed mandates reject mutations, and a valid nested delegation/action succeeds. Record each transaction's final status and execution result, expected failures, and state read-backs. Replace this file and the release manifest only with verified output.
