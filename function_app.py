
import azure.functions as func
import logging
import json
import math

from aqi import kategori_pm25

app = func.FunctionApp(
    http_auth_level=func.AuthLevel.ANONYMOUS
)


@app.route(route="kategori", methods=["GET", "POST"])
def kategori(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("PM2.5 classification request received.")

    # 1. Ambil parameter dari URL
    pm25_input = req.params.get("pm25")

    # 2. Jika tidak ada, coba ambil dari JSON body
    if pm25_input is None:
        try:
            body = req.get_json()
        except ValueError:
            body = {}

        if isinstance(body, dict):
            pm25_input = body.get("pm25")

    # 3. Validasi parameter
    if pm25_input is None:
        return func.HttpResponse(
            json.dumps({
                "error": "Parameter pm25 wajib diberikan."
            }),
            status_code=400,
            mimetype="application/json"
        )

    # 4. Konversi ke angka
    try:
        pm25 = float(pm25_input)
    except (ValueError, TypeError):
        return func.HttpResponse(
            json.dumps({
                "error": "Nilai pm25 harus berupa angka."
            }),
            status_code=400,
            mimetype="application/json"
        )

    if not math.isfinite(pm25):
        return func.HttpResponse(
            json.dumps({
                "error": "Nilai pm25 harus berupa angka yang valid."
            }),
            status_code=400,
            mimetype="application/json"
        )

    # 5. Klasifikasi PM2.5
    try:
        hasil = kategori_pm25(pm25)
    except ValueError as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )

    # 6. Kirim hasil dalam format JSON
    response = {
        "pm25": pm25,
        "kategori": hasil
    }

    return func.HttpResponse(
        json.dumps(response, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )
