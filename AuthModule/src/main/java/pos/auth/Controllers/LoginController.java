package pos.auth.Controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.Model.DTO.UserDTO;
import pos.auth.Model.JwtTokenUtil;
import pos.auth.Model.JwtUserDetailsService;
import pos.auth.View.Login.LoginRequest;
import pos.auth.View.Login.LoginResponse;
import org.springframework.security.crypto.bcrypt.BCrypt;

@Endpoint
public class LoginController {
    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    @Autowired
    private JwtUserDetailsService userDetailsService;

    private static final String NAMESPACE_URI = "http://pos.examples.soap.stateless/login";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "loginRequest")
    @ResponsePayload
    public LoginResponse login(@RequestPayload LoginRequest input) throws Exception {
        final UserDTO userDetails = userDetailsService
                .loadUserByUsername(input.getName());
        LoginResponse r = new LoginResponse();
        if(!BCrypt.checkpw(input.getPassword(), userDetails.getPassword())){
            throw new Exception("WRONG_PASSWORD");
        }
        else{
            final String token = jwtTokenUtil.generateToken(userDetails);
            r.setToken(token);
            return r;
        }
    }
}
