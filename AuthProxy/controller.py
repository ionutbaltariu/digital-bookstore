import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from view import LoginResponse, RegisterResponse, ValidateResponse, LoginRequest, RegisterRequest, ValidateRequest
import requests
import datetime
from fastapi.middleware.cors import CORSMiddleware
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

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
          response_model=LoginResponse
          )
async def register(register_request: RegisterRequest):
    body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                                  xmlns:gs="http://pos.examples.soap.stateless/register">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <gs:registerRequest>
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
        status_code = 200
        response_body = {
            'status': status_node.text
        }

    return JSONResponse(status_code=status_code, content=response_body)


@app.post("/validate",
          response_model=ValidateResponse
          )
async def validate(validate_request: ValidateRequest):
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

    if status_node.text == "INVALID":
        status_code = 401
        response_body = {
            'status': "Token is either expired or invalid.",
        }
    elif status_node.text == "VALID":
        status_code = 200
        response_body = {
            'status': status_node.text,
            'role': role_node.text
        }
    else:
        status_code = 500
        response_body = {
            'status': 'Unexpected server error.'
        }

    return JSONResponse(status_code=status_code, content=response_body)


if __name__ == "__main__":
    uvicorn.run("controller:app", host='0.0.0.0', port=8002, reload=True, debug=True)
