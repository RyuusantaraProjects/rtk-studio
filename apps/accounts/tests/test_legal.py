from django.test import RequestFactory

from apps.accounts import views_legal


class TestLegalPages:
    def test_terms_of_service_page_accessible(self):
        rf = RequestFactory()
        request = rf.get("/terms/")
        response = views_legal.terms_view(request)
        assert response.status_code == 200
        assert "Ketentuan Layanan" in response.content.decode("utf-8")

    def test_privacy_policy_page_accessible(self):
        rf = RequestFactory()
        request = rf.get("/privacy/")
        response = views_legal.privacy_view(request)
        assert response.status_code == 200
        assert "Kebijakan Privasi" in response.content.decode("utf-8")

    def test_data_deletion_page_accessible(self):
        rf = RequestFactory()
        request = rf.get("/data-deletion/")
        response = views_legal.data_deletion_view(request)
        assert response.status_code == 200
        assert "Penghapusan Data" in response.content.decode("utf-8")

    def test_meta_data_deletion_callback_post(self):
        rf = RequestFactory()
        request = rf.post("/data-deletion/", {"signed_request": "dummy.payload"})
        response = views_legal.data_deletion_view(request)
        assert response.status_code == 200
        import json

        data = json.loads(response.content.decode("utf-8"))
        assert "confirmation_code" in data
        assert "url" in data

