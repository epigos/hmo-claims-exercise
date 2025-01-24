from datetime import date

from flask.testing import FlaskClient

from app.claim import Claim
from app.claim.forms import HMO_CHOICES, SERVICE_TYPE_CHOICES
from app.claim.models import StatusEnum


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
    assert new_claim.status.value.replace("_", " ") in resp.text


def test_can_delete_claim(client: FlaskClient, new_claim: Claim) -> None:
    # test claims not found raises 404
    resp = client.post(f"/claims/foo/delete")
    assert resp.status_code == 404

    url = f"/claims/{new_claim.id}/delete"

    delete_resp = client.post(url, follow_redirects=True)
    assert delete_resp.status_code == 200
    assert "Claim deleted successfully" in delete_resp.text


def test_can_view_claim(client: FlaskClient, new_claim: Claim) -> None:
    # test claims not found raises 404
    resp = client.post(f"/claims/foo")
    assert resp.status_code == 404

    url = f"/claims/{new_claim.id}"

    resp = client.get(url)
    assert resp.status_code == 200
    assert "Claim Details" in resp.text
    assert new_claim.user.name in resp.text
    assert new_claim.hmo in resp.text
    assert str(new_claim.final_cost) in resp.text


def test_can_edit_claim(client: FlaskClient, new_claim: Claim) -> None:
    # test claims not found raises 404
    resp = client.post(f"/claims/foo/edit")
    assert resp.status_code == 404

    url = f"/claims/{new_claim.id}/edit"
    payload = dict(
        user_id=new_claim.user.id,
        age=new_claim.age,
        diagnosis=new_claim.diagnosis,
        hmo=HMO_CHOICES[2][0],  # change hmo
        service_charge=new_claim.service_charge,
        total_cost=new_claim.total_cost,
        final_cost=new_claim.final_cost,
        status=StatusEnum.paid.value,
    )
    service_fields = ["service_name", "provider_name", "source", "cost_of_service"]
    new_date = date.today().strftime(format="%Y-%m-%d")
    for idx, service in enumerate(new_claim.services):
        for k in service_fields:
            payload[f"services-{idx}-{k}"] = getattr(service, k)
        payload[f"services-{idx}-service_date"] = new_date  # change service type
        payload[f"services-{idx}-service_type"] = SERVICE_TYPE_CHOICES[
            1
        ]  # change service type

    resp = client.post(url, data=payload, follow_redirects=True)
    assert resp.status_code == 200
    assert "Claim updated successfully" in resp.text

    assert new_claim.user.name in resp.text
    assert new_claim.hmo in resp.text
    assert str(new_claim.final_cost) in resp.text

    updated_claim = Claim.query.get(new_claim.id)
    updated_claim.status = StatusEnum.paid.value
    updated_claim.hmo = HMO_CHOICES[2][0]

    assert len(updated_claim.services) == len(new_claim.services)
    for service in updated_claim.services:
        assert service.type == SERVICE_TYPE_CHOICES[1]
        assert service.service_date.strftime(format="%Y-%m-%d") == new_date
