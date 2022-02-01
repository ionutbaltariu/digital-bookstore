import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from view import LoginResponse, RegisterResponse, ValidateResponse, LoginRequest, RegisterRequest, ValidateRequest
import requests
from fastapi.middleware.cors import CORSMiddleware
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json

origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login",
          response_model=LoginResponse
          )
async def login(login_request: LoginRequest):
    """
    Method that's used to login the user into the digital bookstore.

    :param login_request: Classical username-password request
    :return: JWT if credentials are valid
    """
    body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                                  xmlns:gs="http://pos.examples.soap.stateless/login">">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <gs:loginRequest>
                        <gs:name>{login_request.username}</gs:name>
                        <gs:password>{login_request.password}</gs:password>
                      </gs:loginRequest>
                   </soapenv:Body>
                </soapenv:Envelope>"""
    headers = {'content-type': 'text/xml'}

    response = requests.post("http://auth-module.dev:8080/login",
                             data=body,
                             headers=headers)

    response_payload_node = ET.fromstring(response.content)[1][0][0]

    received = response_payload_node.tag.split('}')[1]

    if received == "errorMessage":
        status_code = 403
        response_body = {'errorMessage': response_payload_node.text}
    elif received == "token":
        status_code = 200
        response_body = {'token': response_payload_node.text}

    return JSONResponse(status_code=status_code, content=response_body)


@app.post("/register",
          response_model=RegisterResponse)
async def register(register_request: RegisterRequest):
    """
    Method that's used to register a user.

    :param register_request: Classical username-password request
    :return: 201 Created with empty body or 406 with error message
    """
    body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                                  xmlns:gs="http://pos.examples.soap.stateless/register">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <gs:registerRequest>
                        <gs:firstname>{register_request.firstname}</gs:firstname>
                        <gs:lastname>{register_request.lastname}</gs:lastname>
                        <gs:email>{register_request.email}</gs:email>
                        <gs:address>{register_request.address}</gs:address>
                        <gs:birthday>{str(register_request.birthday)}</gs:birthday>
                        <gs:name>{register_request.username}</gs:name>
                        <gs:password>{register_request.password}</gs:password>
                      </gs:registerRequest>
                   </soapenv:Body>
                </soapenv:Envelope>"""
    headers = {'content-type': 'text/xml'}

    response = requests.post("http://auth-module.dev:8080/register",
                             data=body,
                             headers=headers)

    xml = BeautifulSoup(response.content, 'xml')
    status_node = xml \
        .find('SOAP-ENV:Envelope') \
        .find('SOAP-ENV:Body') \
        .find('ns2:loginResponse') \
        .find('ns2:status')
    error_message_node = xml \
        .find('SOAP-ENV:Envelope') \
        .find('SOAP-ENV:Body') \
        .find('ns2:loginResponse') \
        .find('ns2:errorMessage')

    if error_message_node:
        status_code = 406
        response_body = {
            'status': status_node.text,
            'errorMessage': error_message_node.text
        }
    else:
        status_code = 201
        response_body = {}

    return JSONResponse(status_code=status_code, content=response_body)


@app.post("/validate",
          response_model=ValidateResponse
          )
async def validate(validate_request: ValidateRequest):
    """
    Method that's used to validate the token of a user.

    :param validate_request: Dict that contains the token
    :return: 200 with the client's role, 401 if invalid, 500 in case of server exception
    """
    body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                                  xmlns:gs="http://pos.examples.soap.stateless/validate">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <gs:validateRequest>
                        <gs:token>{validate_request.token}</gs:token>
                      </gs:validateRequest>
                   </soapenv:Body>
                </soapenv:Envelope>"""
    headers = {'content-type': 'text/xml'}

    response = requests.post("http://auth-module.dev:8080/validate",
                             data=body,
                             headers=headers)
    xml = BeautifulSoup(response.content, 'xml')
    status_node = xml \
        .find('SOAP-ENV:Envelope') \
        .find('SOAP-ENV:Body') \
        .find('ns2:validateResponse') \
        .find('ns2:status')
    role_node = xml \
        .find('SOAP-ENV:Envelope') \
        .find('SOAP-ENV:Body') \
        .find('ns2:validateResponse') \
        .find('ns2:role')
    id_node = xml \
        .find('SOAP-ENV:Envelope') \
        .find('SOAP-ENV:Body') \
        .find('ns2:validateResponse') \
        .find('ns2:id')

    if status_node.text == "INVALID":
        status_code = 401
        response_body = {
            'status': "Token is either expired or invalid.",
        }
    elif status_node.text == "VALID":
        status_code = 200
        response_body = {
            'status': status_node.text,
            'role': role_node.text,
            'id': int(id_node.text)
        }
    else:
        status_code = 500
        response_body = {
            'status': 'Unexpected server error.'
        }

    return JSONResponse(status_code=status_code, content=response_body)


@app.post("/orders")
async def make_order(request: Request):
    req_body = await request.json()
    token = request.headers.get('Authorization').split()[1]
    validate_req = ValidateRequest(token=token)
    validate_response = await validate(validate_req)
    status_code = 201
    response_body = {}

    if validate_response.status_code == 200:
        resp_body = json.loads(validate_response.body)
        role = resp_body["role"]
        user_id = resp_body["id"]

        if role != "User":
            status_code = 403
            response_body["errorReason"] = "An administrator can not place orders. Please use a normal user account."
        else:
            headers = {'content-type': 'application/json'}
            ordered_books = req_body["books"]
            orders_request = requests.post("http://order-module.dev:8001/api/orders",
                                           data=json.dumps({
                                               'user_id': user_id,
                                               'books': ordered_books
                                           }),
                                           headers=headers)
            status_code = orders_request.status_code
            response_body = orders_request.json()
    else:
        status_code = 401
        response_body["errorReason"] = "Authorization of your account failed. Please log in again."

    return JSONResponse(status_code=status_code, content=response_body)


@app.get("/books")
async def get_all_books(genre: str = None, year_of_publishing: int = None,
                        page: int = None, items_per_page: int = None):
    query_param_arr = [genre, year_of_publishing, page, items_per_page]
    query_param_str = ""
    for query_param in query_param_arr:
        if query_param is not None:
            query_param_str += query_param + '&'

    if len(query_param_str) > 0:
        query_param_str = '?' + query_param_str

    endpoint = f"http://book-module.dev:8000/api/bookcollection/books/{query_param_str}"
    all_books_response = requests.get(endpoint)

    return JSONResponse(status_code=all_books_response.status_code, content=all_books_response.json())


if __name__ == "__main__":
    uvicorn.run("controller:app", host='0.0.0.0', port=8002, reload=True, debug=True)
