import copy
import json
from tests.direct.test_delegation_tree import deploy, make_mandate, mandate_key, address, SCOPE_PROMPT, ACTION_PROMPT, sibling_response


def test_creator_capacity_and_names_are_isolated(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    for index in range(20):
        key = contract.create_mandate(f"mandate_{index}", "Library improvements.", 100)
        contract.close_mandate(key)
    with direct_vm.expect_revert("creator_mandate_limit_reached"):
        contract.create_mandate("overflow", "Library improvements.", 100)
    direct_vm.sender = direct_bob
    own = contract.create_mandate("mandate_0", "Independent owner.", 100)
    assert contract.get_mandate(own)["creator"] == address(direct_bob)
    original = address(direct_alice) + "|mandate_0"
    assert contract.get_mandate(original)["status"] == "CLOSED"
    with direct_vm.expect_revert("invalid_mandate_id"):
        contract.create_mandate(original, "Cannot impersonate.", 100)
    with direct_vm.expect_revert("only_mandate_creator"):
        contract.close_mandate(original)


def test_action_capacity_and_ids_are_per_node(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    key = mandate_key(direct_alice)
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(key, "1", address(direct_bob), "Library signage only.", 40)
    direct_vm.sender = direct_bob
    for index in range(20):
        contract.submit_action(key, "2", f"action_{index}", "Install a library sign.", 1)
    with direct_vm.expect_revert("node_action_limit_reached"):
        contract.submit_action(key, "2", "overflow", "Install another sign.", 1)
    direct_vm.sender = direct_alice
    result = contract.submit_action(key, "1", "action_0", "Install shelving.", 1)
    assert result == "1:action_0"
    assert contract.get_action(key, "2:action_0")["submitter"] == address(direct_bob)
    assert contract.get_action(key, result)["submitter"] == address(direct_alice)
    state = contract.get_mandate(key)
    assert state["nodes"]["2"]["pending"] == 20
    assert state["nodes"]["1"]["pending"] == 1


def test_closed_mandate_cannot_be_mutated(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    key = mandate_key(direct_alice)
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(key, "1", address(direct_bob), "Library signage only.", 40)
    contract.close_mandate(key)
    before = contract.get_mandate(key)
    with direct_vm.expect_revert("mandate_not_active"):
        contract.revoke_unused_branch(key, "1", "2")
    with direct_vm.expect_revert("mandate_not_active"):
        contract.submit_action(key, "1", "late", "Install shelving.", 1)
    with direct_vm.expect_revert("mandate_not_active"):
        contract.assess_action(key, "1:late")
    assert contract.get_mandate(key) == before


def test_validator_rejects_forged_containment(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    key = mandate_key(direct_alice)
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(key, "1", address(direct_bob), "Library signage only.", 40)
    forged = copy.deepcopy(direct_vm._captured_validators[-1][0])
    forged["contained"] = "NO"
    assert direct_vm.run_validator(leader_result=forged) is False


def test_child_cannot_consume_parent_reserved_node_slots(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_deploy)
    make_mandate(contract, direct_vm, direct_alice)
    key = mandate_key(direct_alice)
    direct_vm.mock_llm(SCOPE_PROMPT, sibling_response())
    contract.delegate(key, "1", address(direct_bob), "Library signage only.", 40, 2)
    direct_vm.sender = direct_bob
    contract.delegate(key, "2", address(direct_charlie), "Entrance signage only.", 10)
    with direct_vm.expect_revert("parent_node_slots_exceeded"):
        contract.delegate(key, "2", address(bytes.fromhex("44" * 20)), "Interior signage only.", 10)
    direct_vm.sender = direct_alice
    direct_vm.clear_mocks()
    direct_vm.mock_llm(SCOPE_PROMPT, json.dumps({"contained": "YES", "siblings": [{"node": "2", "relation": "DISJOINT"}]}))
    contract.delegate(key, "1", address(bytes.fromhex("55" * 20)), "Library shelving only.", 20)
    state = contract.get_mandate(key)
    assert state["nodes"]["1"]["allocated_node_slots"] == 3
    assert state["nodes"]["2"]["allocated_node_slots"] == 1
