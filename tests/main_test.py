from main import main


def test_main_no_args(mock_mainloop):
    main([__file__])
    assert not mock_mainloop.did_call


def test_main_unknown_arg(mock_mainloop):
    main([__file__, "unknown"])
    assert not mock_mainloop.did_call


def test_main_known_arg(mock_mainloop):
    main([__file__, "image_app"])
    assert mock_mainloop.did_call
