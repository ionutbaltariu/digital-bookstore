package pos.auth.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.DTO.UserDTO;
import pos.auth.Jwt.JwtTokenUtil;
import pos.auth.Jwt.JwtUserDetailsService;
import pos.auth.soap.LoginRequest;
import pos.auth.soap.LoginResponse;
import org.springframework.security.crypto.bcrypt.BCrypt;

@Endpoint
public class AuthService {
    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    @Autowired
    private JwtUserDetailsService userDetailsService;

    private static final String NAMESPACE_URI = "http://pos.examples.soap.stateless/Auth";

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
