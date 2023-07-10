import pytest

@pytest.mark.order(1)
def test_post_ofertas(api_client_user1):
    response = api_client_user1.get(
        "/emprestimos/",
        params={"cpf": "10952493470", "parcelas": 12, "valor": 1000},
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["parcelas"] <= 12
    assert result["valor"] <= 1000

@pytest.mark.order(2)
def test_post_ofertas_no_offer(api_client_user1):
    response = api_client_user1.get(
        "/emprestimos/",
        params={"cpf": "10952493470", "parcelas": 0, "valor": 0}
    )
    assert response.status_code == 204