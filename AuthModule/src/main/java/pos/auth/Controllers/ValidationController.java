package pos.auth.Controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.Model.JwtTokenUtil;
import pos.auth.View.Validate.ValidateRequest;
import pos.auth.View.Validate.ValidateResponse;

@Endpoint
public class ValidationController {
    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    private static final String NAMESPACE_URI = "http://pos.examples.soap.stateless/validate";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "validateRequest")
    @ResponsePayload
    public ValidateResponse validateToken(@RequestPayload ValidateRequest input) throws Exception {
            ValidateResponse r = new ValidateResponse();

            try{
                if(jwtTokenUtil.validateToken(input.getToken())){
                    r.setStatus("VALID");
                    r.setRole(jwtTokenUtil.getRoleFromToken(input.getToken()));
                    r.setId(jwtTokenUtil.getIdFromToken(input.getToken()));
                }
            }
            catch(Exception e){
                r.setStatus("INVALID");
            }

            return r;
        }
}
