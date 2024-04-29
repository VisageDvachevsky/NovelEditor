from app.visual import run


def test_run_known(mock_mainloop):
    run("image_app")
    assert mock_mainloop.did_call


def test_run_unknown(mock_mainloop):
    run(None)
    assert not mock_mainloop.did_call
