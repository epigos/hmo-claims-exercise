from flask.testing import FlaskClient

from app.claim import Claim


def test_can_create_new_claim(
    client: FlaskClient, new_user, claim_data, services_data
) -> None:
    url = "/claims/add"
    resp = client.get(url)
    assert resp.status_code == 200
    assert "Create Claim" in resp.text
    assert "Patient Information" in resp.text
    assert "Service Section" in resp.text
    assert "Total" in resp.text

    payload = {
        "user_id": new_user.id,
        "age": new_user.get_age(),
        **claim_data,
    }
    for idx, service in enumerate(services_data):
        for k, v in service.items():
            payload[f"services-{idx}-{k}"] = v

    add_resp = client.post(url, data=payload, follow_redirects=True)
    assert add_resp.status_code == 200
    assert "All Claims" in add_resp.text

    assert new_user.name in add_resp.text
    assert payload["hmo"] in add_resp.text
    assert str(payload["final_cost"]) in add_resp.text

    claim = Claim.query.filter_by(user_id=new_user.id).first()
    assert len(claim.services) == len(services_data)


def test_can_list_claims(client: FlaskClient, new_claim: Claim) -> None:
    resp = client.get("/claims/")
    assert resp.status_code == 200
    assert "All Claims" in resp.text

    assert new_claim.user.name in resp.text
    assert new_claim.hmo in resp.text
    assert str(new_claim.final_cost) in resp.text
    assert new_claim.status.value in resp.text


def test_can_delete_claim(client: FlaskClient, new_claim: Claim) -> None:
    # test claims not found raises 404
    resp = client.post(f"/claims/foo/delete")
    assert resp.status_code == 404

    url = f"/claims/{new_claim.id}/delete"

    delete_resp = client.post(url, follow_redirects=True)
    assert delete_resp.status_code == 200
    assert "Claim deleted successfully" in delete_resp.text
