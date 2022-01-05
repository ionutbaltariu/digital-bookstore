package pos.auth.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.Jwt.JwtTokenUtil;
import pos.auth.soap.ValidateRequest;
import pos.auth.soap.ValidateResponse;

@Endpoint
public class ValidationService {
    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    private static final String NAMESPACE_URI = "http://pos.examples.soap.stateless/Auth";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "validateRequest")
    @ResponsePayload
    public ValidateResponse validateToken(@RequestPayload ValidateRequest input) throws Exception {
            ValidateResponse r = new ValidateResponse();

            try{
                if(jwtTokenUtil.validateToken(input.getToken())){
                    r.setStatus("VALID");
                }
            }
            catch(Exception e){
                r.setStatus("INVALID");
            }

            return r;
        }
}
