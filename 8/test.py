from main import (
    decode_stream,
    count_zeros,
    render_img
)

def test_decode_stream():
    img_stream = "123456789012"
    img = decode_stream(img_stream, 3, 2)
    assert len(img) == 2
    assert img[0] == [1, 2, 3, 4, 5, 6]
    assert img[1] == [7, 8, 9, 0, 1, 2]

def test_count_zeros():
    img_stream = "123456789012"
    img = decode_stream(img_stream, 3, 2)
    zeros = count_zeros(img)
    assert len(img) == 2
    assert img[0] == [1, 2, 3, 4, 5, 6]
    assert img[1] == [7, 8, 9, 0, 1, 2]
    assert zeros == 0

def test_render_img():
    img_stream = "0222112222120000"
    img = decode_stream(img_stream, 2, 2)
    out = render_img(img, 2, 2)
    assert out == "01\n10"