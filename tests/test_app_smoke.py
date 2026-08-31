from app import create_demo


def test_gradio_app_builds() -> None:
    demo = create_demo()
    assert demo is not None
