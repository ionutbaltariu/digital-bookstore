package com.example.pos.stateless.endpoints

import io.spring.guides.gs_producing_web_service.AddRequest
import io.spring.guides.gs_producing_web_service.AddResponse
import org.springframework.ws.server.endpoint.annotation.Endpoint
import org.springframework.ws.server.endpoint.annotation.PayloadRoot
import org.springframework.ws.server.endpoint.annotation.RequestPayload
import org.springframework.ws.server.endpoint.annotation.ResponsePayload

@Endpoint
class CalculatorEndpoint {
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "addRequest")
    @ResponsePayload
    fun add(@RequestPayload input: AddRequest): AddResponse {
        val result = AddResponse()
        result.result = input.param1.add(input.param2)
        return result
    }

    companion object {
        private const val NAMESPACE_URI = "http://pos.examples.soap.stateless/Calculator"
    }
}