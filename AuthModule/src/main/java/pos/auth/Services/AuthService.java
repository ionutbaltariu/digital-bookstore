package pos.auth.Services;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.soap.LoginRequest;
import pos.auth.soap.LoginResponse;

@Endpoint
public class AuthService {
    private static final String NAMESPACE_URI = "http://pos.examples.soap.stateless/Auth";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "loginRequest")
    @ResponsePayload
    public LoginResponse login(@RequestPayload LoginRequest input){
        LoginResponse r = new LoginResponse();
        r.setToken("mock_token");
        return r;
    }
}
