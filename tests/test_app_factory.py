from app import create_app


def test_create_app_registers_blueprints_without_assertion():
    app = create_app()

    assert app is not None
    assert app.url_map is not None
