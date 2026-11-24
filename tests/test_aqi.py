import pytest

from aqi import kategori_pm25


@pytest.mark.parametrize(
    ("nilai", "expected"),
    [
        (0, "baik"),
        (10, "baik"),
        (15.5, "baik"),
        (15.6, "sedang"),
        (30, "sedang"),
        (55.4, "sedang"),
        (55.5, "tidak sehat"),
        (100, "tidak sehat"),
        (150.4, "tidak sehat"),
        (150.5, "sangat tidak sehat"),
        (200, "sangat tidak sehat"),
    ],
)
def test_kategori_pm25(nilai, expected):
    assert kategori_pm25(nilai) == expected


@pytest.mark.parametrize("nilai", [-0.1, -1, -100])
def test_pm25_negatif_menghasilkan_value_error(nilai):
    with pytest.raises(ValueError, match="PM2.5 tidak boleh negatif"):
        kategori_pm25(nilai)
