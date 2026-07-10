def series_query_params(request):
    return {
        "patient_id": request.query_params.get("patient_id", ""),
        "patient_code": request.query_params.get("patient_code", ""),
        "test_code": request.query_params.get("test_code", ""),
    }
