import json
from pathlib import Path


CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "delegation_tree.py"
SCOPE_PROMPT = "Review a proposed delegated scope"
ACTION_PROMPT = "Determine whether the requested action clearly fits"
def address(account):
    return "0x" + account.hex()


def deploy(direct_deploy):
    return direct_deploy(str(CONTRACT), sdk_version="v0.2.16")


def mandate_key(account):
    return address(account) + "|community_grants"


def make_mandate(contract, vm, alice):
    vm.sender = alice
    contract.create_mandate(
        "community_grants",
        "Authorize small public library improvements, such as shelving, lighting, and accessible signage. Do not authorize staff hiring or building construction.",
        100,
    )


def sibling_response():
    return json.dumps({"contained": "YES", "siblings": []})


def test_nested_quota_and_action_require_independent_scope_agreement(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(mandate_key(direct_alice), "1", address(direct_bob), "Authorize accessible signage improvements at public libraries.", 40)
    state = contract.get_mandate(mandate_key(direct_alice))
    child_id = state["nodes"]["1"].get("children", ["2"])[0]
    assert state["nodes"]["1"]["reserved"] == 40

    direct_vm.sender = direct_bob
    contract.submit_action(mandate_key(direct_alice), child_id, "large_sign", "Install accessible entrance signs at the central public library.", 15)
    direct_vm.mock_llm(ACTION_PROMPT, json.dumps({"status": "WITHIN_SCOPE"}))
    contract.assess_action(mandate_key(direct_alice), "2:large_sign")
    assert contract.get_action(mandate_key(direct_alice), "2:large_sign")["status"] == "APPROVED"
    assert contract.get_mandate(mandate_key(direct_alice))["nodes"][child_id]["spent"] == 15
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_quota_reservation_and_wrong_delegate_are_enforced(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(mandate_key(direct_alice), "1", address(direct_bob), "Authorize accessible signage improvements at public libraries.", 60)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(SCOPE_PROMPT, json.dumps({"contained": "YES", "siblings": [{"node": "2", "relation": "DISJOINT"}]}))
    with direct_vm.expect_revert("parent_quota_exceeded"):
        contract.delegate(mandate_key(direct_alice), "1", address(direct_charlie), "Authorize shelving upgrades at public libraries.", 50)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_assigned_delegate"):
        contract.submit_action(mandate_key(direct_alice), "2", "unauthorized", "Install a sign.", 1)


def test_overlapping_sibling_scope_fails_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(mandate_key(direct_alice), "1", address(direct_bob), "Authorize accessible signage improvements at public libraries.", 40)
    direct_vm.clear_mocks()
    direct_vm.mock_llm(
        SCOPE_PROMPT,
        json.dumps({"contained": "YES", "siblings": [{"node": "2", "relation": "OVERLAP"}]}),
    )
    with direct_vm.expect_revert("sibling_scope_overlap_or_uncertain"):
        contract.delegate(mandate_key(direct_alice), "1", address(bytes.fromhex("44" * 20)), "Authorize signs and entrance accessibility changes at libraries.", 20)
    assert len(contract.get_mandate(mandate_key(direct_alice))["nodes"]) == 2
    assert contract.get_mandate(mandate_key(direct_alice))["nodes"]["1"]["reserved"] == 40


def test_scope_uncertainty_does_not_consume_budget(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(mandate_key(direct_alice), "1", address(direct_bob), "Authorize accessible signage improvements at public libraries.", 40)
    direct_vm.sender = direct_bob
    contract.submit_action(mandate_key(direct_alice), "2", "unclear", "Fund a project that may include a new staff position.", 10)
    direct_vm.mock_llm(ACTION_PROMPT, json.dumps({"status": "UNCERTAIN"}))
    contract.assess_action(mandate_key(direct_alice), "2:unclear")
    assert contract.get_action(mandate_key(direct_alice), "2:unclear")["status"] == "UNRESOLVED"
    assert contract.get_mandate(mandate_key(direct_alice))["nodes"]["2"]["spent"] == 0


def test_pending_actions_reserve_units_before_anyone_assesses_them(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(mandate_key(direct_alice), "1", address(direct_bob), "Authorize accessible signage improvements at public libraries.", 40)
    direct_vm.sender = direct_bob
    contract.submit_action(mandate_key(direct_alice), "2", "request_one", "Install accessible signs at a public library entrance.", 25)
    with direct_vm.expect_revert("node_quota_exceeded"):
        contract.submit_action(mandate_key(direct_alice), "2", "request_two", "Install more signs at another public library.", 20)
    state = contract.get_mandate(mandate_key(direct_alice))
    assert state["nodes"]["2"]["pending"] == 25
    assert "2:request_two" not in state["actions"]


def test_empty_unused_branch_can_be_revoked_and_capacity_released(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(mandate_key(direct_alice), "1", address(direct_bob), "Authorize accessible signage improvements at public libraries.", 40)
    contract.revoke_unused_branch(mandate_key(direct_alice), "1", "2")
    state = contract.get_mandate(mandate_key(direct_alice))
    assert state["nodes"]["2"]["status"] == "REVOKED"
    assert state["nodes"]["1"]["reserved"] == 0

