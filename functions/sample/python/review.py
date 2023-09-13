from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(param_dict: dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """
    api_key = param_dict.get("api_key")
    url = param_dict.get("url")
    authenticator = IAMAuthenticator(api_key)
    service = CloudantV1(authenticator=authenticator)

    service.set_service_url(url)

    param_dict.pop("api_key")
    param_dict.pop("url")
    db = "reviews"
    if "review" in param_dict.keys():
        body = post_review(service, db, param_dict.get("review"))
    if param_dict:
        body = get_specific_doc(service, db, param_dict)
    else:
        body = get_all_docs(service, db)

    if not body:
        return {"body": {}, "headers": {"status_code": 404}}

    return {"body": body}


def post_review(service: CloudantV1, db: str, document: dict) -> dict:
    result = service.post_document(db, document)
    return result._to_dict().get("result")


def get_all_docs(service: CloudantV1, db: str) -> list:
    result = service.post_all_docs(db, limit=10, include_docs=True)
    body = result._to_dict().get("result", {}).get("rows", [{}])
    body = [item.get("doc") for item in body]
    return body


def get_specific_doc(service: CloudantV1, db: str, param_dict: dict) -> list:
    fields = [
        "id",
        "name",
        "dealership",
        "review",
        "purchase",
        "purchase_date",
        "car_make",
        "car_model",
        "car_year",
    ]
    result = service.post_find(
        db=db,
        selector={"dealership": {"$eq": int(param_dict.get("dealerId", 0))}},
        fields=fields,
        limit=param_dict.get("limit", 5),
    )
    body = result._to_dict().get("result", {}).get("docs", [])
    return body


main(
    {
        "api_key": "BdAvzW9H0NRivq0y0gz7zDix4WvcUyCPWiQzAzyguBYT",
        "url": "https://ca869065-5aa7-4f02-9dc6-739f6a5ea587-bluemix.cloudantnosqldb.appdomain.cloud",
        "review": {
            "id": 1114,
            "name": "Upkar Lidder",
            "dealership": 15,
            "review": "Great service!",
            "purchase": False,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021,
        },
    }
)
